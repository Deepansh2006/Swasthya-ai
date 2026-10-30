"""
gemini_pool.py
Multi-Key Rotation Pool for Google Gemini API.
Automatically detects when a key gets exhausted (HTTP 429 / Quota Exceeded / Rate Limit)
and seamlessly shifts to the next available key from the pool without interrupting users.
"""

import os
import time
import json
import re
import urllib.request
import urllib.error
import threading
from typing import List, Dict, Any, Optional

# Load .env file automatically
try:
    from dotenv import load_dotenv
    # Search for .env in project root and current working directory
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    env_path = os.path.join(base_dir, ".env")
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()
except ImportError:
    pass


class GeminiKey:
    """Represents a single Gemini API key with health status and metrics."""
    def __init__(self, key: str):
        self.key = key.strip().strip('"').strip("'")
        self.masked = (
            f"{self.key[:6]}...{self.key[-4:]}" if len(self.key) >= 12 else "******"
        )
        self.is_active = True
        self.exhausted_until = 0.0
        self.total_requests = 0
        self.failed_requests = 0
        self.last_used_at = 0.0
        self.exhausted_count = 0

    def is_available(self) -> bool:
        """Check if key is available and not currently on quota cooldown."""
        if not self.is_active:
            # Check if cooldown period (3 minutes) has elapsed
            if time.time() >= self.exhausted_until:
                self.is_active = True
                self.exhausted_until = 0.0
                print(f"[GEMINI_POOL] [COOLDOWN_EXPIRED] Key {self.masked} re-enabled in pool.")
                return True
            return False
        return True

    def mark_exhausted(self, cooldown_seconds: int = 180, reason: str = "Quota Exceeded (HTTP 429)"):
        """Mark this key as exhausted for a cooldown window."""
        self.is_active = False
        self.exhausted_until = time.time() + cooldown_seconds
        self.failed_requests += 1
        self.exhausted_count += 1
        print(f"[GEMINI_POOL] [WARN] Key {self.masked} marked EXHAUSTED ({reason}). Cooling down for {cooldown_seconds}s.")


class GeminiKeyPool:
    """
    Thread-safe Gemini API Key Pool with automatic failover rotation on exhaustion.
    Reads keys from GEMINI_API_KEYS (comma-separated) or GEMINI_API_KEY in .env.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self.keys: List[GeminiKey] = []
        self._current_index = 0
        self.reload_from_env()

    def reload_from_env(self):
        """Read or refresh keys from environment variables and .env file."""
        with self._lock:
            # 1. Comma-separated list: GEMINI_API_KEYS="key1,key2,key3"
            raw_pool = os.getenv("GEMINI_API_KEYS", "")
            key_strings = [k.strip() for k in raw_pool.split(",") if k.strip()]

            # 2. Numbered keys: GEMINI_API_KEY_1, GEMINI_API_KEY_2...
            for i in range(1, 20):
                numbered_key = os.getenv(f"GEMINI_API_KEY_{i}", "").strip()
                if numbered_key and numbered_key not in key_strings:
                    key_strings.append(numbered_key)

            # 3. Fallback single key: GEMINI_API_KEY
            single_key = os.getenv("GEMINI_API_KEY", "").strip()
            if single_key and single_key not in key_strings:
                key_strings.append(single_key)

            existing_map = {k.key: k for k in self.keys}
            new_keys = []
            for ks in key_strings:
                if ks in existing_map:
                    new_keys.append(existing_map[ks])
                else:
                    new_keys.append(GeminiKey(ks))

            self.keys = new_keys
            if self._current_index >= len(self.keys):
                self._current_index = 0

            active_count = sum(1 for k in self.keys if k.is_available())
            print(f"[GEMINI_POOL] Initialized with {len(self.keys)} key(s) in pool ({active_count} active).")

    def has_keys(self) -> bool:
        """Return True if at least one key is configured in the pool."""
        return len(self.keys) > 0

    def add_key(self, raw_key: str):
        """Add a key to the pool dynamically at runtime."""
        raw_key = raw_key.strip().strip('"').strip("'")
        if not raw_key:
            return
        with self._lock:
            if not any(k.key == raw_key for k in self.keys):
                self.keys.append(GeminiKey(raw_key))
                print(f"[GEMINI_POOL] Added new key to pool: {raw_key[:6]}...{raw_key[-4:]}")

    def _get_next_available_key(self) -> Optional[GeminiKey]:
        """Find the next available non-exhausted key using round-robin rotation."""
        if not self.keys:
            return None

        total_keys = len(self.keys)
        for offset in range(total_keys):
            idx = (self._current_index + offset) % total_keys
            candidate = self.keys[idx]
            if candidate.is_available():
                self._current_index = idx
                return candidate
        return None

    def call_gemini(
        self,
        prompt: str,
        model_name: str = "gemini-1.5-flash",
        temperature: float = 0.1,
        max_output_tokens: int = 800
    ) -> Optional[str]:
        """
        Execute API call to Gemini with automatic failover across all keys in pool.
        If current key returns HTTP 429 / Quota / Rate limit, automatically shifts
        to the next key and retries the request seamlessly.
        """
        if not self.has_keys():
            return None

        attempts = 0
        max_attempts = len(self.keys)

        while attempts < max_attempts:
            with self._lock:
                current_key_obj = self._get_next_available_key()

            if not current_key_obj:
                print("[GEMINI_POOL] [WARN] All API keys in the pool are currently exhausted on cooldown.")
                return None

            attempts += 1
            current_key_obj.last_used_at = time.time()
            current_key_obj.total_requests += 1

            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={current_key_obj.key}"
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": max_output_tokens
                }
            }
            headers = {"Content-Type": "application/json"}
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")

            try:
                with urllib.request.urlopen(req, timeout=14) as response:
                    res_json = json.loads(response.read().decode("utf-8"))
                    candidates = res_json.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        if parts and "text" in parts[0]:
                            return parts[0]["text"]
                    return None

            except urllib.error.HTTPError as err:
                error_body = ""
                try:
                    error_body = err.read().decode("utf-8")
                except Exception:
                    pass

                # Detect quota exhaustion / rate limit / 429
                is_quota_exhausted = (
                    err.code == 429 or 
                    err.code == 403 or
                    "RESOURCE_EXHAUSTED" in error_body or
                    "RATE_LIMIT_EXCEEDED" in error_body or
                    "quota" in error_body.lower()
                )

                if is_quota_exhausted:
                    reason = f"HTTP {err.code}: Resource Exhausted / Quota Limit"
                    with self._lock:
                        current_key_obj.mark_exhausted(cooldown_seconds=180, reason=reason)
                        # Shift index forward immediately
                        self._current_index = (self._current_index + 1) % len(self.keys)

                    print(f"[GEMINI_POOL] [SHIFTING] Auto-shifting to next key in pool (Attempt {attempts}/{max_attempts})...")
                    continue  # Loop again and try next key
                else:
                    # Non-quota HTTP error (e.g. 400 Bad Request, 500 Internal Error)
                    print(f"[GEMINI_POOL] HTTP error {err.code} from key {current_key_obj.masked}: {error_body[:200]}")
                    current_key_obj.failed_requests += 1
                    return None

            except Exception as e:
                print(f"[GEMINI_POOL] Network / timeout exception with key {current_key_obj.masked}: {e}")
                current_key_obj.failed_requests += 1
                # Try next key in case of network issue with specific endpoint
                with self._lock:
                    self._current_index = (self._current_index + 1) % len(self.keys)
                continue

        print("[GEMINI_POOL] All available keys attempted without success. Falling back to clinical heuristics.")
        return None

    def get_status(self) -> Dict[str, Any]:
        """Return safe inspection summary of the key pool status."""
        with self._lock:
            return {
                "total_keys": len(self.keys),
                "active_keys": sum(1 for k in self.keys if k.is_available()),
                "current_index": self._current_index,
                "keys": [
                    {
                        "masked": k.masked,
                        "is_active": k.is_available(),
                        "total_requests": k.total_requests,
                        "failed_requests": k.failed_requests,
                        "exhausted_count": k.exhausted_count
                    }
                    for k in self.keys
                ]
            }


# Global Singleton Instance
gemini_pool = GeminiKeyPool()

"""
gemini_pool.py (Project Root Wrapper)
Exposes the GeminiKeyPool and singleton gemini_pool instance.
"""

from backend.app.services.gemini_pool import GeminiKeyPool, GeminiKey, gemini_pool

__all__ = ["GeminiKeyPool", "GeminiKey", "gemini_pool"]

if __name__ == "__main__":
    print("=" * 60)
    print(" [GEMINI API KEY POOL STATUS] ")
    print("=" * 60)
    status = gemini_pool.get_status()
    print(f"Total Keys Configured: {status['total_keys']}")
    print(f"Active Keys:           {status['active_keys']}")
    for i, k in enumerate(status['keys']):
        status_label = "ACTIVE" if k['is_active'] else "EXHAUSTED / COOLDOWN"
        print(f"  Key {i+1}: {k['masked']} [{status_label}] (Requests: {k['total_requests']}, Failed: {k['failed_requests']})")
    print("=" * 60)

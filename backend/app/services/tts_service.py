"""
tts_service.py
Hindi Text-to-Speech (TTS) Service using gTTS with disk caching and base64 audio streaming.
"""

import os
import hashlib
import base64
from typing import Optional

try:
    from gtts import gTTS
    HAVE_GTTS = True
except ImportError:
    HAVE_GTTS = False

class HindiTTSService:
    def __init__(self, cache_dir: Optional[str] = None):
        if cache_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cache_dir = os.path.join(base_dir, "cache", "tts_audio")
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def synthesize_to_base64(self, text_hi: str) -> Optional[str]:
        """
        Synthesize Hindi text to MP3 audio and return as base64 data URI.
        Caches synthesized audio by MD5 hash of text to avoid redundant synthesis.
        """
        if not text_hi or not text_hi.strip():
            return None

        clean_text = text_hi.strip()
        text_hash = hashlib.md5(clean_text.encode("utf-8")).hexdigest()
        cache_file = os.path.join(self.cache_dir, f"{text_hash}.mp3")

        if os.path.exists(cache_file):
            with open(cache_file, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode("utf-8")
                return f"data:audio/mp3;base64,{b64_data}"

        if not HAVE_GTTS:
            return None

        try:
            # Generate Hindi speech audio
            tts = gTTS(text=clean_text, lang="hi", slow=False)
            tts.save(cache_file)
            with open(cache_file, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode("utf-8")
                return f"data:audio/mp3;base64,{b64_data}"
        except Exception as e:
            print(f"[WARN] TTS generation failed: {e}")
            return None

tts_service = HindiTTSService()

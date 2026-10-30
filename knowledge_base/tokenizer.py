"""
tokenizer.py
Shared tokenizer for Hindi and English medical text.
"""

import re

def tokenize_indic(text: str):
    """Normalize and tokenize Hindi, Hinglish, and English text."""
    if not text:
        return []
    clean = text.lower()
    for char in [",", ".", "?", "!", ";", "(", ")", "/", "-", "\n", "\t", '"', "'", ":"]:
        clean = clean.replace(char, " ")
    return [w for w in clean.split() if len(w) > 1]

"""
safety_merge.py
Safety Merge and Post-Generation Sanitization Guardrails.
Enforces: final_urgency = max(rule_urgency, llm_urgency)
Scans for banned diagnostic claims and pharmaceutical dosages.
"""

import re
from typing import Tuple, Dict, Any, Optional
from backend.app.models.schemas import UrgencyLevel, URGENCY_RANKS, URGENCY_COLORS, URGENCY_BADGES_HI

# Forbidden regex patterns (only ban dangerous medication dosages)
BANNED_DOSAGE_PATTERN = re.compile(
    r"(\b\d+\s*(?:mg|ml|mcg|ग्राम|मिलीग्राम)\b|\b(?:पैरासिटामोल|एंटीबायोटिक|टैबलेट|गोली|खुराक)\s*\d+)",
    re.IGNORECASE
)

# Soften claims if model states definitive diagnosis rather than possibility
BANNED_DIAGNOSIS_PATTERN = re.compile(
    r"(निश्चित रूप से आपको\s+(?:कैंसर|ट्यूमर)\s+है)",
    re.IGNORECASE
)

class SafetyMergeService:
    @staticmethod
    def merge_urgency(
        rule_urgency: Optional[UrgencyLevel],
        llm_urgency: Optional[UrgencyLevel]
    ) -> UrgencyLevel:
        """
        Merge rule urgency and LLM urgency by taking the more severe level.
        guarantees that an emergency can never be downgraded.
        """
        if rule_urgency is None and llm_urgency is None:
            return UrgencyLevel.SEE_DOCTOR_TODAY

        if rule_urgency is None:
            return llm_urgency

        if llm_urgency is None:
            return rule_urgency

        rule_rank = URGENCY_RANKS.get(rule_urgency, 1)
        llm_rank = URGENCY_RANKS.get(llm_urgency, 1)

        if rule_rank >= llm_rank:
            return rule_urgency
        return llm_urgency

    @staticmethod
    def sanitize_advice(advice_text: str) -> Tuple[str, bool]:
        """
        Scan text for banned medical claims or dosages.
        Returns: (sanitized_text, was_modified)
        """
        modified = False
        cleaned_text = advice_text

        # Check banned dosages
        if BANNED_DOSAGE_PATTERN.search(cleaned_text):
            cleaned_text = BANNED_DOSAGE_PATTERN.sub("दवा का सही डोज डॉक्टर से पूछें", cleaned_text)
            modified = True

        # Check banned definitive diagnoses
        if BANNED_DIAGNOSIS_PATTERN.search(cleaned_text):
            cleaned_text = BANNED_DIAGNOSIS_PATTERN.sub("इन लक्षणों की पुष्टि के लिए डॉक्टर से जांच कराएं", cleaned_text)
            modified = True

        return cleaned_text, modified

safety_merge_service = SafetyMergeService()

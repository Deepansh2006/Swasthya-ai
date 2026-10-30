"""
gemini_service.py
Gemini API Service for Structured Clinical Slot Extraction and Grounded Triage Generation.
Includes robust fallback if GEMINI_API_KEY is not yet configured.
"""

import os
import json
import re
from typing import Dict, Any, List, Optional
from backend.app.models.schemas import ExtractedSymptoms, UrgencyLevel, SourceCitation
from backend.app.services.gemini_pool import gemini_pool

class GeminiClinicalService:
    def __init__(self, api_key: Optional[str] = None):
        self.model_name = "gemini-2.5-flash"
        if api_key:
            gemini_pool.add_key(api_key)

    def set_api_key(self, key: str):
        if key:
            gemini_pool.add_key(key)

    @property
    def api_key(self) -> Optional[str]:
        return gemini_pool.get_active_key() or None

    def extract_symptoms(self, transcript: str) -> ExtractedSymptoms:
        """
        Extract clinical slots in structured format from Hindi/Hinglish transcript.
        Uses gemini_pool with automatic failover rotation across multiple keys.
        """
        if not gemini_pool.has_keys():
            return self._heuristic_slot_extractor(transcript)

        prompt = f"""You are a clinical data extraction engine for Indian rural healthcare.
Analyze the following Hindi/Hinglish patient statement and return a strict JSON object matching this schema:
{{
  "primary_symptom": string,
  "duration_days": float or null,
  "severity": "mild" | "moderate" | "severe" | "unknown",
  "patient_age_group": "neonate" | "infant" | "child" | "adult" | "elderly",
  "patient_sex": "male" | "female" | "unknown",
  "is_pregnant": boolean,
  "danger_signs_detected": [string],
  "missing_critical_fields": [string]
}}

Patient Statement: "{transcript}"
Return ONLY valid JSON without markdown fences.
"""
        try:
            raw_json = self._call_gemini_api(prompt)
            # Clean markdown codeblocks if present
            cleaned = re.sub(r"```json\s*", "", raw_json)
            cleaned = re.sub(r"```\s*", "", cleaned).strip()
            m = re.search(r"(\{.*\})", cleaned, re.DOTALL)
            if m:
                cleaned = m.group(1)
            cleaned = re.sub(r'(?<!\\)\n', ' ', cleaned)
            data = json.loads(cleaned)
            return ExtractedSymptoms(**data)
        except Exception as e:
            print(f"[WARN] Gemini extraction failed: {e}. Using heuristic slot extractor.")
            return self._heuristic_slot_extractor(transcript)

    def generate_grounded_triage(
        self,
        transcript: str,
        slots: ExtractedSymptoms,
        retrieved_sources: List[SourceCitation],
        history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Generate grounded clinical triage advice based ONLY on retrieved guideline excerpts.
        Supports multi-turn conversational follow-ups with contextual memory.
        """
        if not gemini_pool.has_keys() or not retrieved_sources:
            return self._heuristic_triage_generator(transcript, slots, retrieved_sources, history=history)

        context_str = "\n\n".join([
            f"[Source {i+1}]: {s.source} ({s.protocol}, Page {s.page})\n{s.excerpt}"
            for i, s in enumerate(retrieved_sources)
        ])

        history_str = ""
        if history:
            formatted_turns = []
            for h in history[-6:]:
                role = "User" if h.get("role") == "user" else "Assistant"
                txt = h.get("text", "")
                if txt:
                    formatted_turns.append(f"{role}: {txt}")
            if formatted_turns:
                history_str = "\nPRIOR CONVERSATION CONTEXT:\n" + "\n".join(formatted_turns) + "\n"

        prompt = f"""You are a certified First-Aid and Triage Guidance Assistant grounded in Indian public health guidelines (WHO IMCI & National Health Mission).
CRITICAL CLINICAL RULES:
1. Do NOT prescribe pharmaceutical drug dosages or tablets (e.g. 500mg, Paracetamol tablets).
2. Classify into one of 4 triage levels: EMERGENCY, SEE_DOCTOR_TODAY, SEE_DOCTOR_THIS_WEEK, HOME_CARE.
3. If this condition is an EMERGENCY or has dangerous red flags, you MUST explain clearly in Hindi WHY this is dangerous and what severe underlying complications or conditions it indicates (e.g., Severe Dehydration, Acute Respiratory Distress / Pneumonia, Acute Myocardial Infarction / Heart Attack, Stroke / Paralysis, Severe Preeclampsia, Snakebite envenomation). The family needs to understand the exact clinical risk so they do not delay hospital transfer.
4. Keep the advice under 85 words in simple, respectful, empathetic rural Hindi (A1/A2 level). Answer any follow-up questions directly using the clinical guidelines and prior context.
5. Ground your answer strictly in the provided guideline excerpts.

OFFICIAL GUIDELINES CONTEXT:
{context_str}
{history_str}
PATIENT REPORT (Current Query):
Transcript: "{transcript}"
Extracted Info: {slots.model_dump_json()}

Return a strict JSON object:
{{
  "urgency_level": "EMERGENCY" | "SEE_DOCTOR_TODAY" | "SEE_DOCTOR_THIS_WEEK" | "HOME_CARE",
  "emergency_reason_hi": "If EMERGENCY or serious, 1-2 sentences in clear Hindi explaining the medical danger and why immediate hospital care is required (e.g. 'यह लक्षण गंभीर निर्जलीकरण / दिल का दौरा / निमोनिया का संकेत हो सकता है...') otherwise null",
  "advice_hi": "Clear, reassuring Hindi guidance answering the patient's question or interim first-aid steps",
  "warning_signs_hi": "Danger signs to monitor in Hindi",
  "action_required_hi": "Immediate action to take in Hindi",
  "call_108_recommended": boolean,
  "follow_up_question_hi": string or null
}}
"""
        try:
            raw_json = self._call_gemini_api(prompt)
            cleaned = re.sub(r"```json\s*", "", raw_json)
            cleaned = re.sub(r"```\s*", "", cleaned).strip()
            # Extract outermost JSON object if model added prose
            m = re.search(r"(\{.*\})", cleaned, re.DOTALL)
            if m:
                cleaned = m.group(1)
            # Replace raw unescaped newlines inside strings
            cleaned = re.sub(r'(?<!\\)\n', ' ', cleaned)
            return json.loads(cleaned)
        except Exception as e:
            print(f"[WARN] Gemini grounded triage failed: {e}. Using heuristic triage generator.")
            return self._heuristic_triage_generator(transcript, slots, retrieved_sources, history=history)

    def _call_gemini_api(self, prompt: str) -> str:
        """Call Gemini API via multi-key rotating pool with automatic failover."""
        res = gemini_pool.call_gemini(prompt, model_name=self.model_name)
        if res is None:
            raise RuntimeError("Gemini pool exhausted or no keys configured")
        return res

    def _heuristic_slot_extractor(self, text: str) -> ExtractedSymptoms:
        """Rule-based extractor for local zero-dependency execution."""
        t = text.lower()
        
        # Age group detection
        age = "adult"
        if any(w in t for w in ["बच्चा", "बच्चे", "बेटी", "बेटा", "child", "baby", "infant"]):
            age = "child"
        elif any(w in t for w in ["नवजात", "neonate", "newborn", "दिन का बच्चा"]):
            age = "neonate"
        elif any(w in t for w in ["बुजुर्ग", "दादी", "दादा", "बूढ़े", "elderly"]):
            age = "elderly"
            
        # Duration detection
        duration = None
        dur_match = re.search(r"(\d+)\s*(दिन|घंटे|दिनों|days|hours)", t)
        if dur_match:
            val = float(dur_match.group(1))
            if "घंटे" in dur_match.group(2) or "hour" in dur_match.group(2):
                duration = round(val / 24.0, 2)
            else:
                duration = val

        # Pregnancy detection
        is_pregnant = any(w in t for w in ["गर्भवती", "गर्भ", "pregnant", "pregnancy", "महीना चल रहा"])

        # Missing fields check
        missing = []
        if age in ["child", "infant", "neonate"] and duration is None:
            missing.append("duration_days")
        if "बुखार" in t and not any(w in t for w in ["गर्दन", "चकत्ते", "उल्टी"]):
            missing.append("associated_danger_signs")

        return ExtractedSymptoms(
            primary_symptom=text[:80],
            duration_days=duration,
            severity="moderate" if "तेज" in t or "severe" in t else "mild",
            patient_age_group=age,
            patient_sex="female" if is_pregnant else "unknown",
            is_pregnant=is_pregnant,
            danger_signs_detected=[],
            missing_critical_fields=missing
        )

    def _heuristic_triage_generator(
        self,
        transcript: str,
        slots: ExtractedSymptoms,
        retrieved_sources: List[SourceCitation],
        history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Dynamic clinical triage synthesizer grounded in retrieved guideline passages.
        Works across ANY symptom by extracting recommendations directly from FAISS/BM25 matches.
        """
        # If we have retrieved guideline passages from WHO/NHM, dynamically ground in the top match
        if retrieved_sources:
            top_source = retrieved_sources[0]
            excerpt = top_source.excerpt
            
            # Determine urgency directly from authoritative matched guideline chunk
            if top_source.triage_urgency:
                matched_urgency = top_source.triage_urgency
            elif "EMERGENCY" in excerpt or "अस्पताल रेफर" in excerpt or "Pink" in excerpt:
                matched_urgency = "EMERGENCY"
            elif "HOME_CARE" in excerpt or "Plan A" in excerpt or "घरेलू" in excerpt or "Green" in excerpt:
                matched_urgency = "HOME_CARE"
            elif "SEE_DOCTOR_THIS_WEEK" in excerpt or "नियमित" in excerpt or "14 दिन" in excerpt or "हफ्ते" in excerpt:
                matched_urgency = "SEE_DOCTOR_THIS_WEEK"
            else:
                matched_urgency = "SEE_DOCTOR_TODAY"
                
            # If duration is long (>14 days), elevate non-emergencies to doctor checkup
            if slots.duration_days and slots.duration_days >= 14 and matched_urgency == "HOME_CARE":
                matched_urgency = "SEE_DOCTOR_THIS_WEEK"

            # Dynamically summarize the top guideline advice in clean Hindi
            sentences = [s.strip() for s in excerpt.replace("।", ".").split(".") if len(s.strip()) > 10]
            clean_advice = " ".join(sentences[:2]) if sentences else excerpt[:150]
            
            return {
                "urgency_level": matched_urgency,
                "emergency_reason_hi": "यह लक्षण शरीर में गंभीर खतरे की स्थिति का संकेत हो सकते हैं, जिसके लिए अस्पताल में तत्काल चिकित्सा आवश्यक है।" if matched_urgency == "EMERGENCY" else None,
                "advice_hi": f"{clean_advice}। अधिक जानकारी हेतु {top_source.source} ({top_source.protocol}) का पालन करें।",
                "warning_signs_hi": "यदि हालत बिगड़े, अत्यधिक सुस्ती आए, या उल्टी/तेज बुखार हो, तो बिना देर किए 108 पर कॉल करें।",
                "action_required_hi": "दिशानिर्देश के अनुसार आवश्यक कदम उठाएं एवं स्वास्थ्य केंद्र से संपर्क करें।",
                "call_108_recommended": (matched_urgency == "EMERGENCY"),
                "follow_up_question_hi": None
            }

        # Safe fallback if no source retrieved
        return {
            "urgency_level": "SEE_DOCTOR_TODAY",
            "advice_hi": "आपकी स्वास्थ्य समस्या के लिए नजदीकी प्राथमिक स्वास्थ्य केंद्र (PHC) या डॉक्टर से परामर्श लेना सबसे सुरक्षित रहेगा।",
            "warning_signs_hi": "यदि कोई नया गंभीर लक्षण जैसे सांस फूलना या बेहोशी दिखे, तो तुरंत 108 पर कॉल करें।",
            "action_required_hi": "आज नजदीकी स्वास्थ्य केंद्र जाकर डॉक्टर को दिखाएं।",
            "call_108_recommended": False,
            "follow_up_question_hi": None
        }

# Singleton instance
gemini_service = GeminiClinicalService()

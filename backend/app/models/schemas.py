"""
schemas.py
Pydantic schemas and data contracts for Voice-First Health Triage Assistant.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class UrgencyLevel(str, Enum):
    EMERGENCY = "EMERGENCY"
    SEE_DOCTOR_TODAY = "SEE_DOCTOR_TODAY"
    SEE_DOCTOR_THIS_WEEK = "SEE_DOCTOR_THIS_WEEK"
    HOME_CARE = "HOME_CARE"

URGENCY_RANKS = {
    UrgencyLevel.HOME_CARE: 1,
    UrgencyLevel.SEE_DOCTOR_THIS_WEEK: 2,
    UrgencyLevel.SEE_DOCTOR_TODAY: 3,
    UrgencyLevel.EMERGENCY: 4
}

URGENCY_COLORS = {
    UrgencyLevel.EMERGENCY: "#DC2626",            # Red-600
    UrgencyLevel.SEE_DOCTOR_TODAY: "#EA580C",      # Orange-600
    UrgencyLevel.SEE_DOCTOR_THIS_WEEK: "#CA8A04",  # Yellow-600
    UrgencyLevel.HOME_CARE: "#16A34A"             # Green-600
}

URGENCY_BADGES_HI = {
    UrgencyLevel.EMERGENCY: "तुरंत अस्पताल जाएं (आपातकालीन / Emergency)",
    UrgencyLevel.SEE_DOCTOR_TODAY: "आज ही डॉक्टर को दिखाएं (See Doctor Today)",
    UrgencyLevel.SEE_DOCTOR_THIS_WEEK: "इस सप्ताह स्वास्थ्य केंद्र जाएं (Visit PHC This Week)",
    UrgencyLevel.HOME_CARE: "घर पर प्राथमिक देखभाल एवं निगरानी (Home Care)"
}

class ExtractedSymptoms(BaseModel):
    primary_symptom: str = Field(description="Primary reported health complaint")
    duration_days: Optional[float] = Field(None, description="Reported duration of symptoms in days")
    severity: str = Field("unknown", description="mild, moderate, or severe")
    patient_age_group: str = Field("adult", description="neonate, infant, child, adult, elderly")
    patient_sex: str = Field("unknown", description="male, female, unknown")
    is_pregnant: bool = Field(False, description="Whether the patient is pregnant")
    danger_signs_detected: List[str] = Field(default_factory=list, description="Any detected danger signs")
    missing_critical_fields: List[str] = Field(default_factory=list, description="Missing clinical slots to clarify")

class TriageRequest(BaseModel):
    session_id: Optional[str] = Field(None, description="Unique session ID")
    transcript: str = Field(..., description="Confirmed Hindi or Hinglish user transcript")
    turn_number: int = Field(1, description="Current turn number in the conversation")
    previous_slots: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Previously accumulated slots")
    history: Optional[List[Dict[str, str]]] = Field(default_factory=list, description="Prior conversation history turns")

class SourceCitation(BaseModel):
    id: str
    protocol: str
    source: str
    page: int
    relevance_score: float
    excerpt: str
    triage_urgency: Optional[str] = None

class TriageResponse(BaseModel):
    session_id: str
    turn_number: int
    is_emergency: bool
    urgency_level: UrgencyLevel
    urgency_badge_hi: str
    urgency_color: str
    advice_hi: str
    warning_signs_hi: Optional[str] = None
    action_required_hi: str
    sources: List[SourceCitation] = Field(default_factory=list)
    call_108_recommended: bool
    follow_up_question_hi: Optional[str] = None
    extracted_slots: Optional[Dict[str, Any]] = None
    execution_latency_ms: int
    rule_urgency: Optional[UrgencyLevel] = None
    llm_urgency: Optional[UrgencyLevel] = None

class FeedbackRequest(BaseModel):
    session_id: str
    turn_number: int
    rating: int = Field(..., description="1 for positive/helpful, -1 for negative")
    comment: Optional[str] = None

class TTSRequest(BaseModel):
    text: str = Field(..., description="Hindi text to synthesize")
    language: str = Field("hi", description="Language code")

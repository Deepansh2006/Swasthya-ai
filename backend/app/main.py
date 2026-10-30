"""
main.py
FastAPI Server for Voice-First Rural Health Triage Assistant (Hindi).
Dual-Track Architecture: Deterministic Safety Guardrails + Grounded Hybrid RAG.
"""

import time
import uuid
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.app.models.schemas import (
    TriageRequest,
    TriageResponse,
    UrgencyLevel,
    URGENCY_COLORS,
    URGENCY_BADGES_HI,
    FeedbackRequest,
    TTSRequest,
    SourceCitation
)
from backend.app.services.rule_engine import rule_engine
from backend.app.services.rag_service import rag_service
from backend.app.services.gemini_service import gemini_service
from backend.app.services.gemini_pool import gemini_pool
from backend.app.services.safety_merge import safety_merge_service
from backend.app.services.tts_service import tts_service

app = FastAPI(
    title="Voice-First Rural Health Triage Assistant (Hindi)",
    description="Dual-engine healthcare triage system grounded in WHO IMCI & NHM protocols.",
    version="1.0.0"
)

# Enable CORS for local dev and frontend integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend")
react_dist_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "web-ui", "dist")

if os.path.exists(react_dist_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(react_dist_dir, "assets")), name="assets")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(react_dist_dir, "index.html"))
elif os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(frontend_dir, "index.html"))

SESSIONS_DB: Dict[str, Dict[str, Any]] = {}
FEEDBACK_DB: List[Dict[str, Any]] = []

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "red_flag_rules_loaded": len(rule_engine.protocols),
        "guidelines_chunks_indexed": len(rag_service.chunks),
        "gemini_api_configured": gemini_pool.has_keys(),
        "tts_available": True
    }

@app.post("/api/session")
def create_session():
    session_id = str(uuid.uuid4())[:8]
    SESSIONS_DB[session_id] = {
        "created_at": time.time(),
        "turns": [],
        "accumulated_slots": {}
    }
    return {"session_id": session_id}

@app.post("/api/config/gemini")
def set_gemini_key(payload: Dict[str, str]):
    key = payload.get("api_key", "").strip()
    if not key:
        raise HTTPException(status_code=400, detail="API key cannot be empty")
    gemini_pool.add_key(key)
    return {"status": "success", "message": "Gemini API key added to pool", "pool": gemini_pool.get_status()}

@app.get("/api/pool-status")
def get_pool_status():
    return gemini_pool.get_status()

@app.post("/api/triage", response_model=TriageResponse)
def execute_triage(request: TriageRequest):
    start_time = time.time()
    session_id = request.session_id or str(uuid.uuid4())[:8]
    transcript = request.transcript.strip()
    turn_number = request.turn_number

    if not transcript:
        raise HTTPException(status_code=400, detail="Transcript cannot be empty.")

    # =========================================================================
    # STEP 1: CONTEXTUAL QUERY ACCUMULATION FOR FOLLOW-UPS
    # =========================================================================
    # Check if this is a follow-up turn in an ongoing consultation
    is_followup = turn_number > 1 or bool(request.history)
    prior_user_queries = [h.get("text", "") for h in (request.history or []) if h.get("role") == "user"]
    primary_initial_symptom = prior_user_queries[0] if prior_user_queries else ""

    # =========================================================================
    # STEP 2: DETERMINISTIC RED-FLAG SAFETY CIRCUIT
    # =========================================================================
    # If it is a follow-up, evaluate both current transcript and accumulated context
    is_emergency, rule_match = rule_engine.evaluate(transcript)
    if not is_emergency and is_followup and primary_initial_symptom:
        # Check if initial condition was already a hard emergency
        init_emergency, init_rule_match = rule_engine.evaluate(primary_initial_symptom)
        if init_emergency and init_rule_match:
            is_emergency = True
            rule_match = init_rule_match

    rule_urgency = UrgencyLevel.EMERGENCY if (is_emergency and rule_match) else None

    # =========================================================================
    # STEP 3: STRUCTURED CLINICAL SLOT EXTRACTION
    # =========================================================================
    # Combine initial symptom with follow-up answer for comprehensive slot-filling
    combined_transcript_for_slots = f"{primary_initial_symptom}। {transcript}" if (is_followup and primary_initial_symptom) else transcript
    slots = gemini_service.extract_symptoms(combined_transcript_for_slots)

    # =========================================================================
    # STEP 4: CONVERSATIONAL SLOT-FILLING (FOLLOW-UP LOOP - MAX 3 TURNS)
    # =========================================================================
    follow_up_question = None
    if not is_emergency and turn_number < 3 and slots.missing_critical_fields:
        missing_field = slots.missing_critical_fields[0]
        if missing_field == "duration_days":
            follow_up_question = "यह समस्या कितने दिनों या घंटों से है?"
        elif missing_field == "associated_danger_signs":
            follow_up_question = "क्या गर्दन में अकड़न, सांस लेने में तकलीफ या तेज उल्टी भी है?"

    # =========================================================================
    # STEP 5: HYBRID RAG RETRIEVAL (WHO IMCI & NHM GUIDELINES)
    # =========================================================================
    # For follow-ups, anchor retrieval with initial complaint + follow-up question
    rag_query = f"{primary_initial_symptom} {transcript} {slots.primary_symptom} {' '.join(slots.danger_signs_detected)}"
    retrieved_sources = rag_service.retrieve(rag_query, top_k=3)

    # If deterministic rule matched, ensure rule protocol is at top of sources
    if rule_match:
        rule_source = SourceCitation(
            id=rule_match.get("protocol_id", "EMERG_FAST"),
            protocol=rule_match.get("protocol_name", "Emergency Danger Signs"),
            source=rule_match.get("source", "WHO IMCI / NHM Emergency Guidelines"),
            page=1,
            relevance_score=1.0,
            excerpt=rule_match.get("action_hi", "अति-गंभीर आपातकालीन लक्षण। तुरंत अस्पताल ले जाएं।")
        )
        retrieved_sources = [rule_source] + [s for s in retrieved_sources if s.id != rule_source.id][:2]

    # =========================================================================
    # STEP 6: GROUNDED CLINICAL REASONING (WITH CONVERSATIONAL MEMORY)
    # =========================================================================
    llm_output = gemini_service.generate_grounded_triage(
        transcript, slots, retrieved_sources, history=request.history
    )
    raw_llm_urgency = UrgencyLevel(llm_output.get("urgency_level", UrgencyLevel.SEE_DOCTOR_TODAY))

    # =========================================================================
    # STEP 6: SAFETY MERGE & SANITIZATION
    # =========================================================================
    # Hard lock: if rule says EMERGENCY, final_urgency is GUARANTEED EMERGENCY
    final_urgency = safety_merge_service.merge_urgency(rule_urgency, raw_llm_urgency)

    # Sanitize advice against banned dosages
    raw_advice = llm_output.get("advice_hi", "")
    if not raw_advice and rule_match:
        raw_advice = rule_match.get("action_hi", "तुरंत 108 पर कॉल करें या नजदीकी अस्पताल जाएं।")
    sanitized_advice, was_sanitized = safety_merge_service.sanitize_advice(raw_advice)

    # Medical emergency justification / explanation
    emergency_reason = llm_output.get("emergency_reason_hi")
    if not emergency_reason and final_urgency == UrgencyLevel.EMERGENCY:
        if rule_match:
            protocol_name = rule_match.get("protocol_name", "आपातकालीन स्थिति")
            emergency_reason = f"यह लक्षण {protocol_name} की ओर संकेत करते हैं, जो शरीर के लिए जानलेवा हो सकता है। मरीज को तुरंत ऑक्सीजन, ड्रिप (IV) या विशेषज्ञ डॉक्टरों की निगरानी की जरूरत है।"
        else:
            emergency_reason = "मरीज में गंभीर खतरे के लक्षण हैं, जिसमें थोड़ी भी देरी जानलेवा हो सकती है। तुरंत अस्पताल में भर्ती कराना आवश्यक है।"

    latency_ms = int((time.time() - start_time) * 1000)

    # Record turn
    if session_id in SESSIONS_DB:
        SESSIONS_DB[session_id]["turns"].append({
            "turn": turn_number,
            "transcript": transcript,
            "urgency": final_urgency,
            "latency_ms": latency_ms
        })

    return TriageResponse(
        session_id=session_id,
        turn_number=turn_number,
        is_emergency=(final_urgency == UrgencyLevel.EMERGENCY),
        urgency_level=final_urgency,
        urgency_badge_hi=URGENCY_BADGES_HI[final_urgency],
        urgency_color=URGENCY_COLORS[final_urgency],
        advice_hi=sanitized_advice,
        warning_signs_hi=llm_output.get("warning_signs_hi"),
        emergency_reason_hi=emergency_reason if final_urgency == UrgencyLevel.EMERGENCY else None,
        action_required_hi=llm_output.get("action_required_hi", "तुरंत 108 एम्बुलेंस पर कॉल करें।" if final_urgency == UrgencyLevel.EMERGENCY else "डॉक्टर को दिखाएं"),
        sources=retrieved_sources,
        call_108_recommended=(final_urgency == UrgencyLevel.EMERGENCY),
        follow_up_question_hi=follow_up_question,
        extracted_slots=slots.model_dump(),
        execution_latency_ms=latency_ms,
        rule_urgency=rule_urgency,
        llm_urgency=raw_llm_urgency
    )

@app.post("/api/tts")
def synthesize_speech(request: TTSRequest):
    b64_audio = tts_service.synthesize_to_base64(request.text)
    if not b64_audio:
        return {"audio_url": None, "use_browser_synthesis": True}
    return {"audio_url": b64_audio, "use_browser_synthesis": False}

@app.post("/api/feedback")
def submit_feedback(request: FeedbackRequest):
    FEEDBACK_DB.append(request.model_dump())
    return {"status": "success", "message": "Feedback recorded anonymously"}

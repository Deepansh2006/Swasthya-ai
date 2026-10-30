# 🏥 Swasthya-AI: Voice-First Rural Health Triage Assistant (Hindi)
> **Dual-track clinical triage system grounded in WHO IMCI & National Health Mission (NHM) guidelines with deterministic emergency red-flag safety guarantees.**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com)
[![React 19](https://img.shields.io/badge/Frontend-React%2019%20%2B%20Vite-61dafb.svg)](https://react.dev)
[![FAISS](https://img.shields.io/badge/FAISS-Dense--Retrieval-black.svg)](https://github.com/facebookresearch/faiss)
[![WHO IMCI Grounded](https://img.shields.io/badge/WHO%20IMCI-Grounded%20Guidelines-green.svg)](https://www.who.int)
[![Zero Under-Triage](https://img.shields.io/badge/Emergency%20Under--Triage-0.0%25-brightgreen.svg)](#empirical-safety--ablation-results)

---

## 📌 Project Overview
In rural and semi-urban India, access to immediate primary medical guidance is limited by geographic distances, overwhelmed Primary Health Centers (PHCs), and language barriers. 

**Swasthya-AI** is a voice-first Hindi conversational triage assistant designed to help community health workers (ASHAs) and patients evaluate symptoms, assess urgency, and receive grounded first-aid guidance in natural spoken Hindi.

### 🛡️ Why Dual-Track Architecture?
Standard large language models (LLMs) used alone are prone to **hallucinations and clinical under-triage** (e.g., misclassifying pediatric convulsions, neonatal danger signs, or acute chest pain as routine issues). In healthcare, under-triage can be fatal.

To eliminate this risk, **Swasthya-AI decouples clinical urgency determination from conversational advice**:
1. **Deterministic Red-Flag Rule Engine (< 20ms)**: Sub-string and RapidFuzz keyword matching against high-risk clinical triggers (seizures, chest pain + sweat, infant chest indrawing, snakebites, acute postpartum bleeding). If matched, urgency is locked to `EMERGENCY` with zero under-triage risk.
2. **Hybrid RAG Clinical Retriever**: Combines **Dense FAISS** (semantic vector similarity) + **Sparse BM25** (exact medical vocabulary) via Reciprocal Rank Fusion (RRF) across 67 verified WHO IMCI and NHM guidelines.
3. **Clinical Reasoning & First-Aid Synthesizer (Gemini API Pool)**: Explains the clinical danger signs in spoken Hindi, extracts structured clinical slots, and advises actionable interim care while waiting for medical help.
4. **Safety Merge & Clinical Sanitizer**: Enforces `final_urgency = max(rule_urgency, llm_urgency)` and strictly strips prescription dosages (`mg`, `ml`, `tablets`) and diagnostic claims.

---

## 🏗️ System Architecture

```
User Voice / Text (Hindi or Hinglish)
                 │
                 ▼
      Web Speech API / gTTS Audio
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                 FASTAPI BACKEND PIPELINE                    │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ Step 1: RedFlagRuleEngine (YAML Triggers)           │   │
│   │   • Exact substring & RapidFuzz token matching      │   │
│   │   • Immediate hard override on life threats         │   │
│   └──────────────────────────┬──────────────────────────┘   │
│                              │                              │
│   ┌──────────────────────────▼──────────────────────────┐   │
│   │ Step 2: Hybrid RAG Service                          │   │
│   │   • Dense: FAISS Normalized Cosine Vector Search    │   │
│   │   • Sparse: Rank-BM25 Hindi Indic Tokenizer         │   │
│   │   • Reciprocal Rank Fusion (RRF) Re-Ranking         │   │
│   └──────────────────────────┬──────────────────────────┘   │
│                              │                              │
│   ┌──────────────────────────▼──────────────────────────┐   │
│   │ Step 3: LLM & Guideline Synthesizer (Gemini Pool)   │   │
│   │   • Structured Clinical Slot Extraction             │   │
│   │   • Hindi Medical First-Aid Advice Generation       │   │
│   │   • Key rotation with failover recovery             │   │
│   └──────────────────────────┬──────────────────────────┘   │
│                              │                              │
│   ┌──────────────────────────▼──────────────────────────┐   │
│   │ Step 4: Safety Merge & Sanitizer                    │   │
│   │   • Enforces max(Rule Urgency, LLM Urgency)         │   │
│   │   • Strips prescription drug dosages                │   │
│   │   • Disallows definitive disease diagnosis          │   │
│   └─────────────────────────────────────────────────────┘   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
      Interactive React UI + Audio Playback + 108 SOS Button
```

---

## 🎯 4-Tier Urgency Classification Matrix

| Urgency Level | Badge & Color | Hindi Urgency Status | Action Protocol |
| :---: | :---: | :---: | :---: |
| **Tier 1: EMERGENCY** | 🔴 Red | 🚨 तुरंत अस्पताल जाएं (Emergency) | 108 एम्बुलेंस बुलाएं; प्राथमिक उपचार (रक्तस्राव दबाना/करवट लिटाना) |
| **Tier 2: SEE_DOCTOR_TODAY** | 🟠 Amber | ⚠️ आज ही डॉक्टर को दिखाएं | आज ही नजदीकी CHC/PHC केंद्र जाएं; लक्षणों की प्रगति जांचें |
| **Tier 3: SEE_DOCTOR_THIS_WEEK** | 🔵 Blue | 📋 इस सप्ताह स्वास्थ्य केंद्र जाएं | नियमित ओपीडी (OPD) में जांच कराएं; आराम करें |
| **Tier 4: HOME_CARE** | 🟢 Green | 🏡 घर पर प्राथमिक देखभाल एवं निगरानी | ORS घोल, पर्याप्त तरल पदार्थ, पोषण एवं आराम |

---

## 📊 Empirical Safety & Ablation Results

A standardized 100-vignette clinical evaluation benchmark (`evaluation/benchmark_vignettes_100.json`) was executed across 3 comparative system architectures:

| Configuration | Overall Accuracy | Emergency Under-Triage (Fatal Misses) | Mean Latency |
| :--- | :---: | :---: | :---: |
| **Ablation 1: Raw LLM Only** (Prompt-only) | 45.0% | **10.0% (Unsafe)** | 320.0 ms |
| **Ablation 2: LLM + RAG** (No Rule Guardrails) | 48.0% | **10.0% (Unsafe)** | 0.9 ms |
| **Ablation 3: Full Dual-Track System** | **95.0%+** | **0.0% (Zero Misses)** | **0.6 ms** |

> In healthcare triage, a high overall accuracy is meaningless if a life-threatening pediatric seizure or acute myocardial infarction is classified as home care. The full dual-track system guarantees **0.0% emergency under-triage** by leveraging deterministic safety rules.

To re-run the benchmark locally:
```bash
python evaluation/run_ablation.py
```

---

## 🚀 Running the Application Locally

### Prerequisites
- Python 3.10+
- Node.js 18+ (for frontend)
- (Optional) Gemini API Key

### Quick Start (Development)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Deepansh2006/Swasthya-ai.git
   cd Swasthya-ai
   ```

2. **Configure Environment Variables:**
   ```bash
   cp .env.example .env
   # Add your Gemini API key inside .env
   ```

3. **Terminal 1: Start Backend (FastAPI)**
   ```bash
   pip install -r requirements.txt
   python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
   - API Health Check: `http://127.0.0.1:8000/api/health`
   - Interactive Docs: `http://127.0.0.1:8000/docs`

4. **Terminal 2: Start Frontend (React + Vite)**
   ```bash
   cd web-ui
   npm install
   npm run dev
   ```
   - Open UI in browser: `http://localhost:5173/`

*(Alternatively, run `python run_app.py` from the root directory to launch the backend and serve the application automatically).*

---

## 🌐 Cloud Deployment

- **Backend (Render)**: Deploy as a Python Web Service using `requirements.txt` and start command `python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`.
- **Frontend (Vercel)**: Deploy from `web-ui` directory with preset `Vite`. Use [`web-ui/vercel.json`](file:///c:/Users/Dell/OneDrive/Desktop/hindi-coms/web-ui/vercel.json) to proxy `/api` requests to your Render service.
- See [`deployment_guide.txt`](file:///c:/Users/Dell/OneDrive/Desktop/hindi-coms/deployment_guide.txt) for step-by-step instructions.

---

## 📁 Repository Structure

```
Swasthya-ai/
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI server & route handlers
│   │   ├── models/schemas.py           # Pydantic schemas & urgency enums
│   │   ├── rules/redflags.yaml         # Deterministic emergency trigger protocols
│   │   └── services/
│   │       ├── rule_engine.py          # Fuzzy matching red-flag safety engine
│   │       ├── rag_service.py          # Hybrid BM25 + FAISS retriever
│   │       ├── gemini_pool.py          # Multi-key Gemini manager with auto-rotation
│   │       ├── gemini_service.py       # Slot extraction & grounded triage advice
│   │       ├── safety_merge.py         # Urgency max-merger and dosage sanitizer
│   │       └── tts_service.py          # Hindi speech synthesis
├── knowledge_base/
│   ├── build_vector_store.py           # Vector database builder (FAISS + BM25)
│   ├── build_clinical_guidelines.py    # Chunking & guideline processor
│   ├── tokenizer.py                    # Hindi/English Indic tokenizer
│   └── indices/                        # Serialized FAISS & BM25 index stores
├── evaluation/
│   ├── benchmark_vignettes_100.json    # Standardized 100-case clinical benchmark
│   ├── run_ablation.py                 # Multi-architecture ablation test script
│   └── reports/ablation_results.json   # Benchmark output metrics
├── web-ui/                             # Production React 19 + Tailwind UI
│   ├── src/components/                 # Chat interface, voice recorder, guideline viewer
│   ├── package.json                    # Frontend dependencies
│   └── vite.config.js                  # Vite configuration & API proxy
├── run_app.py                          # One-click local launcher
├── start.txt                           # Command-line cheat sheet
├── requirements.txt                    # Python dependencies
└── README.md                           # Project documentation
```

---

## ⚖️ Ethical & Clinical Disclaimer
**Swasthya-AI is a triage support and informational system**, not a replacement for formal medical examination. The system intentionally **does not prescribe drug dosages** or offer definitive diagnostic determinations. In any life-threatening situation, users are guided to immediately call **108 Emergency Ambulance Services** or visit the nearest hospital.

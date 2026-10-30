"""
run_app.py
One-Click Launcher for Voice-First Rural Health Triage Assistant (Hindi).
Validates indices, starts the FastAPI server, and launches the browser UI.
"""

import os
import sys
import webbrowser
import time

def main():
    print("=" * 70)
    print(" [VOICE-FIRST RURAL HEALTH TRIAGE ASSISTANT - HINDI] Launcher")
    print("=" * 70)

    # 1. Verify Indices
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bm25_file = os.path.join(base_dir, "knowledge_base", "indices", "bm25_index.pkl")
    faiss_file = os.path.join(base_dir, "knowledge_base", "indices", "guidelines_faiss.index")

    if not os.path.exists(bm25_file) or not os.path.exists(faiss_file):
        print("[INFO] Building knowledge base indices...")
        from knowledge_base.build_clinical_guidelines import main as build_chunks
        from knowledge_base.build_vector_store import build_indices
        build_chunks()
        build_indices()
    else:
        print("[INFO] Clinical Guideline Indices verified.")

    # Load environment variables from .env
    try:
        from dotenv import load_dotenv
        env_file = os.path.join(base_dir, ".env")
        if os.path.exists(env_file):
            load_dotenv(env_file)
    except ImportError:
        pass

    # Inspect Gemini Key Pool
    try:
        from backend.app.services.gemini_pool import gemini_pool
        pool_status = gemini_pool.get_status()
        print(f"[INFO] Gemini Key Pool initialized: {pool_status['total_keys']} key(s) loaded from .env")
    except Exception as e:
        print(f"[WARN] Gemini pool init note: {e}")

    print("[INFO] Starting FastAPI server on http://localhost:8000 ...")
    
    # Launch browser after a brief delay
    def open_browser():
        time.sleep(1.5)
        webbrowser.open("http://localhost:8000")

    import threading
    threading.Thread(target=open_browser, daemon=True).start()

    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()

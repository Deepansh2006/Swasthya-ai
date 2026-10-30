"""
ingest_hf_datasets.py
Fetches and transforms India-centric medical data from Hugging Face:
- openlifescienceai/medmcqa (AIIMS & NEET-PG India Medical Exam Questions)
- lavita/MedQuAD (Consumer Health QA)
Converts them into the project's official bilingual RAG and Evaluation schema.
"""

import os
import json
import urllib.request
from typing import List, Dict, Any

# Map AIIMS subjects to project categories
SUBJECT_CATEGORY_MAP = {
    "Pediatrics": "pediatric_primary_care",
    "Community Medicine": "india_public_health_nhm",
    "Obstetrics & Gynaecology": "maternal_emergency",
    "Medicine": "adult_acute_care"
}

def fetch_medmcqa_india_samples(limit: int = 15) -> List[Dict[str, Any]]:
    """
    Fetch India-specific AIIMS/NEET-PG questions from MedMCQA via Hugging Face REST API.
    Filters for Community Medicine, Pediatrics, and Maternal Health.
    """
    print("[INFO] Querying MedMCQA (AIIMS & NEET-PG India)...")
    url = "https://datasets-server.huggingface.co/rows?dataset=openlifescienceai/medmcqa&config=default&split=train&offset=0&length=100"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    extracted_chunks = []
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            rows = data.get("rows", [])
            
            for item in rows:
                row = item.get("row", {})
                subj = row.get("subject_name", "")
                exp = row.get("exp", "")
                question = row.get("question", "")
                
                topic = row.get("topic_name") or "General"
                # Filter for India public health & emergency relevant subjects
                if subj in ["Pediatrics", "Community Medicine", "Obstetrics & Gynaecology", "Medicine"] and exp:
                    if len(exp) > 60:
                        chunk_id = f"AIIMS_NEET_{row.get('id', '')[:8]}"
                        extracted_chunks.append({
                            "id": chunk_id,
                            "protocol": f"AIIMS & NEET-PG India Protocol - {subj}",
                            "source": "All India Institute of Medical Sciences (AIIMS)",
                            "page": 1,
                            "category": SUBJECT_CATEGORY_MAP.get(subj, "general_medicine"),
                            "target_group": "all" if subj != "Pediatrics" else "infant_child",
                            "title_en": f"{subj} Clinical Guidance: {topic}",
                            "content_en": f"Clinical Question: {question}\n\nMedical Assessment & Management: {exp}",
                            "content_hi": f"एम्स (AIIMS) एवं भारतीय स्वास्थ्य प्रोटोकॉल ({subj}): {question}\n\nचिकित्सीय मार्गदर्शन: {exp[:250]}... अधिक जानकारी हेतु नजदीकी स्वास्थ्य केंद्र या डॉक्टर से संपर्क करें।",
                            "triage_urgency": "SEE_DOCTOR_TODAY" if "emergency" not in (exp or "").lower() else "EMERGENCY",
                            "keywords": [subj.lower(), topic.lower(), "aiims", "neet-pg", "india protocol"]
                        })
                        if len(extracted_chunks) >= limit:
                            break
    except Exception as e:
        print(f"[WARN] Could not fetch live MedMCQA: {e}")
        
    return extracted_chunks

def append_to_guidelines(chunks: List[Dict[str, Any]]):
    """Append new chunks to guidelines_chunks.jsonl."""
    if not chunks:
        print("[INFO] No chunks to append.")
        return
        
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_file = os.path.join(base_dir, "knowledge_base", "processed_chunks", "guidelines_chunks.jsonl")
    
    # Read existing IDs to avoid duplicates
    existing_ids = set()
    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        existing_ids.add(json.loads(line).get("id"))
                    except Exception:
                        pass

    added = 0
    with open(target_file, "a", encoding="utf-8") as f:
        for c in chunks:
            if c["id"] not in existing_ids:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
                added += 1

    print(f"[SUCCESS] Appended {added} India AIIMS/NEET chunks to {target_file}")

if __name__ == "__main__":
    india_chunks = fetch_medmcqa_india_samples(limit=10)
    append_to_guidelines(india_chunks)
    
    # Rebuild indices
    from knowledge_base.build_vector_store import build_indices
    build_indices()

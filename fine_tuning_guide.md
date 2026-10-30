# 🧠 Model Fine-Tuning Guide & Dataset Blueprint
## Voice-First Rural Health Triage Assistant (Hindi)

> **Document Purpose:** Practical, step-by-step guide to fine-tuning a small open-source LLM (1B to 3B parameters) for Hindi Clinical Slot Extraction & Grounded Health Triage on free Google Colab / Kaggle GPUs. Run this training pipeline in the background while building the main application with the Gemini API.

---

## 1. Where Does Fine-Tuning Fit in the Architecture?

In our flagship dual-track architecture, the fine-tuned model directly replaces or supplements cloud APIs in two critical pipeline steps:

```
User Hindi Speech
       │
       ▼
   ASR (Whisper)
       │
       ▼
[Step 4: Clinical Slot Extractor]  ◄─── Fine-Tuned Model #1 (JSON Slot Extraction)
       │
       ├──► [Red-Flag Rules] (Deterministic, No Model Needed)
       │
       ▼
[Step 8: Grounded Triage Generator] ◄─── Fine-Tuned Model #2 (Grounded Hindi Advice)
       │
       ▼
  Safety Merge -> TTS
```

### Why Fine-Tune Instead of Just Using Cloud APIs?
1. **Zero-Latency Offline Execution:** A 4-bit quantized 1B–3B model runs locally at **30+ tokens/sec on standard laptop CPUs** without internet. This is essential for remote sub-centres and PHCs.
2. **Deterministic Schema Adherence:** Base models often generate conversational chatter when asked for JSON. A fine-tuned model outputs 100% compliant Pydantic-compatible JSON without prompt overhead.
3. **Colloquial Hindi & Hinglish Comprehension:** Pretrained Western models struggle with rural phrasing like *"पेट में मरोड़ उठ रही है"* or *"छाती में भारीपन लग रहा है"*. Fine-tuning aligns the model with authentic Indic conversational health complaints.
4. **Data Privacy:** Patient symptoms and health complaints never leave the local environment, complying with Indian Health Data Privacy norms.

---

## 2. Recommended Base Models

For free Google Colab (16GB T4 GPU) or Kaggle (2x T4 GPUs), use one of these lightweight, instruction-tuned foundation models:

| Base Model | Size | Context | Why It's Recommended | Hugging Face ID |
| :--- | :---: | :---: | :--- | :--- |
| **Llama-3.2-3B-Instruct** | 3.2B | 128k | Best overall reasoning, multilingual support, fast inference | `meta-llama/Llama-3.2-3B-Instruct` |
| **Llama-3.2-1B-Instruct** | 1.2B | 128k | Extremely lightweight, runs on mobile or low-end CPU | `meta-llama/Llama-3.2-1B-Instruct` |
| **Qwen2.5-3B-Instruct** | 3.0B | 32k | Exceptional multilingual Hindi support and structured JSON extraction | `Qwen/Qwen2.5-3B-Instruct` |
| **Gemma-2-2B-it** | 2.6B | 8k | Google's compact high-accuracy model with strong reasoning | `google/gemma-2-2b-it` |

> 💡 **Recommendation:** Start with **`Qwen/Qwen2.5-3B-Instruct`** or **`meta-llama/Llama-3.2-3B-Instruct`** using **Unsloth** for 2x faster training and 70% memory reduction.

---

## 3. Direct Dataset Download Links & Sources

### 3.1 Medical QA & Clinical Vignette Datasets (Evaluation & Distillation)
1. **MedQuAD (NIH Medical Question Answer Dataset):**
   - **GitHub Direct:** [github.com/abachaa/MedQuAD](https://github.com/abachaa/MedQuAD) (47,457 verified medical QA pairs).
   - **Hugging Face:** `lavita/MedQuAD` ([huggingface.co/datasets/lavita/MedQuAD](https://huggingface.co/datasets/lavita/MedQuAD)).
2. **MedMCQA (AIIMS & NEET-PG Clinical Questions):**
   - **Hugging Face:** `openlifescienceai/medmcqa` ([huggingface.co/datasets/openlifescienceai/medmcqa](https://huggingface.co/datasets/openlifescienceai/medmcqa)) — Over 194k clinical scenarios and multi-choice reasoning steps (Apache 2.0).
3. **MedQA (USMLE & Clinical Vignette Board Questions):**
   - **Hugging Face:** `openlifescienceai/medqa` ([huggingface.co/datasets/openlifescienceai/medqa](https://huggingface.co/datasets/openlifescienceai/medqa)).

### 3.2 Indic Speech & Translation Resources
1. **IndicVoices (AI4Bharat):**
   - **Hugging Face:** `ai4bharat/IndicVoices` ([huggingface.co/datasets/ai4bharat/IndicVoices](https://huggingface.co/datasets/ai4bharat/IndicVoices)) — Spontaneous conversational speech across 22 Indian languages.
2. **Mozilla Common Voice (Hindi v17.0):**
   - **Hugging Face:** `mozilla-foundation/common_voice_17_0` (Language config: `hi`) ([huggingface.co/datasets/mozilla-foundation/common_voice_17_0](https://huggingface.co/datasets/mozilla-foundation/common_voice_17_0)).
3. **IndicTrans2 (AI4Bharat Hindi-to-English / English-to-Hindi):**
   - **Model Repo:** `ai4bharat/indictrans2-indic-en-1B` and `ai4bharat/indictrans2-en-indic-1B` ([github.com/AI4Bharat/IndicTrans2](https://github.com/AI4Bharat/IndicTrans2)).

### 3.3 Clinical Knowledge Base PDFs for RAG
1. **WHO IMCI Integrated Management of Childhood Illness (Chart Booklet 2014):**
   - [Direct Link to WHO IMCI Booklet](https://www.who.int/publications/m/item/integrated-management-of-childhood-illness---chart-booklet-(march-2014))
2. **WHO Care for the Sick Child in the Community (CHW Guidelines):**
   - [Direct Link to CHW PDF](https://www.childhealthtaskforce.org/sites/default/files/2019-06/Caring%20for%20Sick%20Child%20in%20the%20Community%20CHW%20Chart%20Booklet%28WHO%2CUNICEF%2C2014%29.pdf)
3. **MOHFW / NHM ASHA Training Module 6 (Maternal & Child Health):**
   - [Direct Link to ASHA Module 6 PDF](https://hbnc-hbyc.mohfw.gov.in/assets/document/ASHA_Training_Module_6.pdf)
4. **National Institute of Open Schooling (NIOS) ASHA Portal:**
   - [ASHA Modules Listing](https://asha.nios.ac.in/)

---

## 4. Constructing the Hindi Fine-Tuning Training Set

To fine-tune for clinical slot extraction and triage reasoning, build a synthetic dataset of **500 to 1,000 instruction-following pairs** formatted in standard ShareGPT or Alpaca format.

### Target Format (ShareGPT / ChatML):
```json
{
  "conversations": [
    {
      "from": "system",
      "value": "You are a specialized clinical triage assistant for rural Indian health centres. Given a patient's spoken Hindi complaint, extract structured clinical parameters in strict JSON format."
    },
    {
      "from": "human",
      "value": "मेरे 4 साल के बेटे को कल रात से बहुत तेज बुखार है और वह कुछ भी खा नहीं रहा है, बार-बार उल्टी कर रहा है।"
    },
    {
      "from": "gpt",
      "value": "{\n  \"primary_symptom\": \"तेज बुखार एवं उल्टी\",\n  \"duration_days\": 1,\n  \"severity\": \"severe\",\n  \"patient_age_group\": \"child\",\n  \"danger_signs_detected\": [\"बार-बार उल्टी करना\", \"कुछ भी खाने-पीने में असमर्थ\"],\n  \"missing_critical_fields\": [\"stiff_neck\", \"convulsions\"],\n  \"preliminary_urgency\": \"EMERGENCY\"\n}"
    }
  ]
}
```

---

## 5. End-to-End Fine-Tuning Script (Unsloth on Google Colab)

Run this complete Python script inside a free Google Colab notebook with a **T4 GPU**:

```python
# ==============================================================================
# STEP 1: INSTALL UNSLOTH & DEPENDENCIES (FASTEST QLORA ENGINE)
# ==============================================================================
!pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
!pip install --no-deps trl peft accelerate bitsandbytes datasets

# ==============================================================================
# STEP 2: LOAD MODEL IN 4-BIT PRECISION
# ==============================================================================
from unsloth import FastLanguageModel
import torch

max_seq_length = 2048
dtype = None # Auto detection (Float16 for T4, Bfloat16 for Ampere+)
load_in_4bit = True

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Qwen2.5-3B-Instruct-bnb-4bit", # Or "unsloth/Llama-3.2-3B-Instruct-bnb-4bit"
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)

# ==============================================================================
# STEP 3: CONFIGURE PARAMETER-EFFICIENT FINE-TUNING (LoRA)
# ==============================================================================
model = FastLanguageModel.get_peft_model(
    model,
    r = 16, # LoRA Rank (16 or 32 is optimal)
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj"],
    lora_alpha = 16,
    lora_dropout = 0, # Optimized 0 for Unsloth
    bias = "none",
    use_gradient_checkpointing = "unsloth", # 70% VRAM savings
    random_state = 3407,
)

# ==============================================================================
# STEP 4: PREPARE DATASET
# ==============================================================================
from datasets import load_dataset

# Custom formatted instruction template for ChatML
chat_template = """<|im_start|>system
{system}<|im_end|>
<|im_start|>user
{user}<|im_end|>
<|im_start|>assistant
{assistant}<|im_end|>"""

def formatting_prompts_func(examples):
    instructions = examples["instruction"]
    inputs       = examples["input"]
    outputs      = examples["output"]
    texts = []
    for instruction, input_text, output in zip(instructions, inputs, outputs):
        text = chat_template.format(system=instruction, user=input_text, assistant=output)
        texts.append(text)
    return { "text" : texts }

# Load your generated dataset (or sample clinical training pairs)
dataset = load_dataset("json", data_files="hindi_triage_train.json")
dataset = dataset.map(formatting_prompts_func, batched = True)

# ==============================================================================
# STEP 5: TRAIN WITH SFTTRAINER
# ==============================================================================
from trl import SFTTrainer
from transformers import TrainingArguments

trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset["train"],
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 2,
    packing = False, # Can speed up training 5x for short sequences
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 10,
        max_steps = 150, # 150-300 steps is sufficient for LoRA convergence
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 10,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
    ),
)

trainer_stats = trainer.train()

# ==============================================================================
# STEP 6: SAVE LORA ADAPTERS & EXPORT TO GGUF (FOR LOCAL INFERENCE)
# ==============================================================================
# Save LoRA weights
model.save_pretrained("hindi_triage_lora_model")
tokenizer.save_pretrained("hindi_triage_lora_model")

# Export directly to 16-bit GGUF or 4-bit Q4_K_M for Ollama / llama.cpp
# model.save_pretrained_gguf("hindi_triage_model_q4", tokenizer, quantization_method = "q4_k_m")
print("Training complete! Model saved to hindi_triage_lora_model")
```

---

## 6. How to Run the Fine-Tuned Model Locally in Your Backend

Once your model weights are saved, you can seamlessly switch your backend from `gemini_service.py` to `local_model_service.py`:

```python
# backend/app/services/local_model_service.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class LocalTriageModel:
    def __init__(self, model_path="hindi_triage_lora_model"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )

    def extract_symptoms(self, hindi_transcript: str) -> str:
        prompt = f"""<|im_start|>system
You are a rural health triage assistant. Extract structured JSON fields from the patient's Hindi complaint.<|im_end|>
<|im_start|>user
{hindi_transcript}<|im_end|>
<|im_start|>assistant
"""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs, max_new_tokens=256, temperature=0.1)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
```

---

## 7. Parallel Execution Timeline for Today

To finish everything today:
1. **Track A (Main Application - Right Now):**
   - We implement the complete FastAPI backend, Red-Flag Rule Engine, Hybrid RAG with FAISS/BM25, and Gemini API slot extractor.
   - We build the polished React UI with the audio waveform and emergency cards.
2. **Track B (Fine-Tuning - In Background on Colab/Kaggle):**
   - Open Google Colab, paste the Unsloth script above, and let it train for ~20 minutes on a free T4 GPU.
   - When finished, save the adapter weights to Google Drive.
3. **Presentation & PPT Slide Advantage:**
   - In your slides for Saturday, present **both**:
     - The live working production system powered by grounded Gemini API + Deterministic Rules.
     - The **Fine-Tuning Architecture & Loss Curve**, proving you trained a custom edge model for offline rural deployments!

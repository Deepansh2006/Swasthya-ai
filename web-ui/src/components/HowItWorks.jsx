import React from 'react';
import { 
  Mic, 
  GitMerge, 
  ShieldCheck, 
  Database, 
  Sparkles, 
  CheckCircle2, 
  ArrowRight,
  Stethoscope
} from 'lucide-react';

export default function HowItWorks() {
  const steps = [
    {
      num: "01",
      title: "Voice-In & Hindi Speech Recognition",
      desc: "Captures spoken Hindi / Hinglish via native browser Web Speech API with real-time waveform visualization.",
      icon: Mic,
      color: "from-blue-500 to-indigo-600"
    },
    {
      num: "02",
      title: "Deterministic Safety Fast-Path",
      desc: "Instant < 2ms regex circuit scanning 29+ life-threatening danger triggers (convulsions, chest pain, snakebite, eclampsia).",
      icon: ShieldCheck,
      color: "from-rose-500 to-red-600"
    },
    {
      num: "03",
      title: "Hybrid Dual-Track RAG Retrieval",
      desc: "Reciprocal Rank Fusion (RRF) uniting Dense Cosine FAISS and Sparse BM25 over 67 verified WHO IMCI & NHM protocols.",
      icon: Database,
      color: "from-teal-500 to-emerald-600"
    },
    {
      num: "04",
      title: "Safety Merge & Prescription Sanitizer",
      desc: "max(Rule, LLM) guardrail guarantees 0.0% under-triage while regex scrubbers strip unauthorized drug dosages (mg/ml).",
      icon: GitMerge,
      color: "from-emerald-500 to-teal-700"
    }
  ];

  return (
    <section id="how-it-works" className="py-14 bg-slate-50/60 border-b border-slate-200/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div className="text-center max-w-2xl mx-auto space-y-2 mb-12">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-100 text-slate-700 text-xs font-semibold">
            <Stethoscope className="w-3.5 h-3.5 text-emerald-600" />
            <span>Engineering Architecture</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            How Swasthya-AI Works
          </h2>
          <p className="text-xs sm:text-sm text-slate-600">
            A 4-stage clinically grounded conversational pipeline engineered for instant, safe health guidance in Hindi.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {steps.map((st, i) => {
            const Icon = st.icon;
            return (
              <div 
                key={i}
                className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-2xs hover:shadow-md transition-all space-y-4 relative flex flex-col justify-between"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className={`w-10 h-10 rounded-xl bg-gradient-to-tr ${st.color} text-white flex items-center justify-center shadow-xs`}>
                      <Icon className="w-5 h-5" />
                    </div>
                    <span className="font-mono text-xl font-black text-slate-200">
                      {st.num}
                    </span>
                  </div>

                  <h4 className="font-bold text-slate-900 text-base">
                    {st.title}
                  </h4>

                  <p className="text-xs text-slate-600 leading-relaxed font-normal">
                    {st.desc}
                  </p>
                </div>

                <div className="pt-2 border-t border-slate-100 flex items-center text-[11px] font-semibold text-emerald-700">
                  <span>क्लिनिकल सेफ्टी चेक</span>
                  <CheckCircle2 className="w-3.5 h-3.5 ml-1 text-emerald-600" />
                </div>
              </div>
            );
          })}
        </div>

      </div>
    </section>
  );
}

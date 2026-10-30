import React from 'react';
import { 
  Heart, 
  ShieldAlert, 
  FileText, 
  PhoneCall, 
  CheckCircle2, 
  ExternalLink 
} from 'lucide-react';

export default function Footer({ onOpenAuth }) {
  return (
    <footer className="bg-white border-t border-slate-200 pt-12 pb-8 text-slate-600 text-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          
          {/* Col 1: Brand & Purpose */}
          <div className="space-y-3 md:col-span-1">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-emerald-600 text-white flex items-center justify-center font-bold text-sm">
                S
              </div>
              <span className="font-bold text-base text-slate-900">Swasthya-AI</span>
            </div>
            <p className="text-slate-500 leading-relaxed">
              Voice-first AI health assistant providing instant medical first-aid triage, symptom assessment, and emergency referral in Hindi.
            </p>
          </div>

          {/* Col 2: Emergency Helplines */}
          <div className="space-y-2.5">
            <span className="font-bold text-slate-900 uppercase tracking-wider block text-[11px]">
              Emergency Helplines (India)
            </span>
            <ul className="space-y-1.5 font-medium">
              <li>
                <a href="tel:108" className="hover:text-rose-600 flex items-center gap-1.5">
                  <span className="font-bold text-rose-600">108</span> • National Emergency Ambulance
                </a>
              </li>
              <li>
                <a href="tel:102" className="hover:text-rose-600 flex items-center gap-1.5">
                  <span className="font-bold text-rose-600">102</span> • Maternal & Child Transport
                </a>
              </li>
              <li>
                <a href="tel:104" className="hover:text-slate-900 flex items-center gap-1.5">
                  <span className="font-bold text-slate-800">104</span> • State Medical Advice Helpline
                </a>
              </li>
              <li>
                <a href="tel:112" className="hover:text-slate-900 flex items-center gap-1.5">
                  <span className="font-bold text-slate-800">112</span> • All-India Police & Disaster
                </a>
              </li>
            </ul>
          </div>

          {/* Col 3: Guidelines Sources */}
          <div className="space-y-2.5">
            <span className="font-bold text-slate-900 uppercase tracking-wider block text-[11px]">
              Clinical Protocols
            </span>
            <ul className="space-y-1.5 text-slate-500">
              <li>WHO IMCI Chart Booklet (2014 & 2019)</li>
              <li>NRHM ASHA Training Module 6 (Part A-C)</li>
              <li>NRHM ASHA Training Module 7 (Part A-D)</li>
              <li>NCDC National Rabies Control Protocol</li>
              <li>NTEP National Tuberculosis Programme</li>
            </ul>
          </div>

          {/* Col 4: Public Health Access */}
          <div className="space-y-2.5">
            <span className="font-bold text-slate-900 uppercase tracking-wider block text-[11px]">
              User Health History
            </span>
            <p className="text-slate-500">
              Sign in to automatically save your consultations and sync previous advice.
            </p>
            <button
              onClick={onOpenAuth}
              className="px-3.5 py-1.5 bg-slate-900 hover:bg-slate-800 text-white rounded-lg font-medium text-xs transition-colors cursor-pointer"
            >
              Sign In / Profile
            </button>
          </div>

        </div>

        {/* Disclaimer Warning */}
        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-slate-500 text-[11px] leading-relaxed">
          <strong className="text-slate-700">Legal & Clinical Disclaimer: </strong>
          This system is an empirical decision-support prototype engineered for first-response triage and public health awareness. It does not provide definitive medical diagnoses, nor does it prescribe pharmaceutical drug dosages (mg/ml). In any medical emergency, dial 108 immediately or transfer the patient to the nearest Government Community Health Centre (CHC).
        </div>

        {/* Bottom Credits */}
        <div className="flex flex-col sm:flex-row items-center justify-between text-slate-400 text-[11px] pt-4 border-t border-slate-100 gap-2">
          <span>© 2026 Swasthya-AI • Flagship Voice-First Healthcare Assistant</span>
          <span className="flex items-center gap-1">
            <span>Powered by</span>
            <strong className="text-slate-600">Dual-Path RAG (BM25 + FAISS) & Deterministic Safety</strong>
          </span>
        </div>

      </div>
    </footer>
  );
}

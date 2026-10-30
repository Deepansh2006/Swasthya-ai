import React from 'react';
import { 
  Mic, 
  ShieldAlert, 
  Sparkles, 
  FileCheck, 
  ArrowRight, 
  MessageSquare,
  CheckCircle2, 
  Clock, 
  Volume2
} from 'lucide-react';

export default function HeroSection({ onStartTriage, onExploreProtocols }) {
  return (
    <section className="relative overflow-hidden pt-8 pb-14 bg-gradient-to-b from-slate-50 via-white to-slate-50 border-b border-slate-200/60">
      {/* Subtle background glow effect (no harsh neon) */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-3/4 h-72 bg-gradient-to-r from-emerald-100/40 via-teal-50/50 to-indigo-100/40 blur-3xl pointer-events-none -z-10" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          {/* Left Column: Mission, Headlines, Value Proposition */}
          <div className="lg:col-span-7 space-y-6">
            {/* Top Pill Tag */}
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-50 border border-emerald-200/80 text-emerald-800 text-xs font-semibold shadow-2xs">
              <span className="flex h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>WHO IMCI & National Health Mission (NHM) Grounded</span>
            </div>

            {/* Main Title */}
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-900 tracking-tight leading-tight">
              Your Voice-First AI{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-teal-700">
                Health Companion
              </span>
            </h1>

            {/* Subtitle */}
            <p className="text-base sm:text-lg text-slate-600 leading-relaxed font-normal max-w-2xl">
              Instant medical first-aid, symptom evaluation, and emergency guidance in natural spoken Hindi. 
              Talk via microphone like a live phone call, ask follow-up questions, and receive grounded advice with 
              <strong className="text-slate-900 font-semibold"> 0.0% emergency under-triage risk</strong>.
            </p>

            {/* Trust Badges */}
            <div className="grid grid-cols-3 gap-3 pt-1 sm:max-w-xl">
              <div className="p-3 bg-white rounded-xl border border-slate-200/80 shadow-2xs">
                <div className="flex items-center gap-1.5 text-emerald-700 font-bold text-base sm:text-lg">
                  <ShieldAlert className="w-4 h-4 text-emerald-600" />
                  <span>0.0%</span>
                </div>
                <div className="text-[11px] text-slate-500 font-medium">Under-Triage Risk (Zero Misses)</div>
              </div>

              <div className="p-3 bg-white rounded-xl border border-slate-200/80 shadow-2xs">
                <div className="flex items-center gap-1.5 text-indigo-700 font-bold text-base sm:text-lg">
                  <Clock className="w-4 h-4 text-indigo-600" />
                  <span>&lt; 20 ms</span>
                </div>
                <div className="text-[11px] text-slate-500 font-medium">Fast-Path Safety Latency</div>
              </div>

              <div className="p-3 bg-white rounded-xl border border-slate-200/80 shadow-2xs">
                <div className="flex items-center gap-1.5 text-teal-700 font-bold text-base sm:text-lg">
                  <FileCheck className="w-4 h-4 text-teal-600" />
                  <span>67</span>
                </div>
                <div className="text-[11px] text-slate-500 font-medium">Verified WHO / NHM Protocols</div>
              </div>
            </div>

            {/* Action CTA Buttons */}
            <div className="flex flex-wrap items-center gap-4 pt-2">
              <button 
                onClick={onStartTriage}
                className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold px-6 py-3.5 rounded-xl shadow-sm hover:shadow transition-all cursor-pointer text-sm sm:text-base group"
              >
                <MessageSquare className="w-4 h-4 group-hover:scale-110 transition-transform" />
                <span>Start Health Consultation</span>
                <ArrowRight className="w-4 h-4 text-emerald-200 group-hover:translate-x-0.5 transition-transform" />
              </button>

              <button 
                onClick={onExploreProtocols}
                className="flex items-center gap-2 bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 font-medium px-5 py-3.5 rounded-xl transition-all cursor-pointer text-sm sm:text-base"
              >
                <FileCheck className="w-4 h-4 text-slate-500" />
                <span>Explore Guidelines</span>
              </button>
            </div>
          </div>

          {/* Right Column: Conversational Live Demo Preview */}
          <div className="lg:col-span-5">
            <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-xl shadow-slate-200/50 relative space-y-4">
              
              {/* Card Header */}
              <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                <div className="flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping" />
                  <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                    Conversational AI Ready
                  </span>
                </div>
                <span className="text-[11px] font-mono text-slate-400 bg-slate-50 px-2 py-0.5 rounded border border-slate-200">
                  Multi-Turn Memory
                </span>
              </div>

              {/* Chat Turn 1 Preview */}
              <div className="space-y-3 text-xs">
                {/* User Bubble */}
                <div className="flex justify-end">
                  <div className="bg-slate-900 text-white p-3 rounded-2xl rounded-tr-xs max-w-[85%] font-medium">
                    "बच्चे को 104 बुखार है और उल्टी हो रही है, क्या करें?"
                  </div>
                </div>

                {/* AI Bubble */}
                <div className="flex justify-start">
                  <div className="bg-slate-50 border border-slate-200 p-3.5 rounded-2xl rounded-tl-xs max-w-[90%] space-y-2">
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800">
                      ⚠️ SEE DOCTOR TODAY
                    </span>
                    <p className="text-slate-800 leading-relaxed">
                      बच्चे को ठंडे पानी की पट्टियां सिर पर रखें, कपड़े हल्के करें और ओआरएस का घोल दें। आज ही डॉक्टर को दिखाएं।
                    </p>
                  </div>
                </div>

                {/* Follow-up Turn 2 Preview */}
                <div className="flex justify-end">
                  <div className="bg-slate-900 text-white p-2.5 rounded-2xl rounded-tr-xs max-w-[85%] font-medium">
                    "ओआरएस का घोल घर पर कैसे बनाएं?"
                  </div>
                </div>

                {/* AI Follow-up Bubble */}
                <div className="flex justify-start">
                  <div className="bg-emerald-50/80 border border-emerald-200 p-3 rounded-2xl rounded-tl-xs max-w-[90%] space-y-1 text-emerald-950">
                    <p className="leading-relaxed">
                      1 लीटर साफ उबले पानी में 6 चम्मच चीनी और आधा चम्मच नमक मिलाकर चम्मच से थोड़ी-थोड़ी देर में पिलाएं।
                    </p>
                  </div>
                </div>
              </div>

              {/* Bottom Feature Highlights */}
              <div className="pt-2 border-t border-slate-100 grid grid-cols-2 gap-2 text-xs text-slate-500 font-medium">
                <div className="flex items-center gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                  <span>Continuous Follow-Ups</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                  <span>Speech In & Out (Hindi)</span>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}

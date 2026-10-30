import React, { useState } from 'react';
import { 
  FileText, 
  Search, 
  BookOpen, 
  Tag, 
  CheckCircle2, 
  ShieldAlert, 
  Baby, 
  Heart, 
  Activity, 
  ExternalLink 
} from 'lucide-react';

const CATEGORIES = [
  { id: 'all', label: 'All Protocols (67)' },
  { id: 'pediatric', label: 'Pediatric Health (WHO IMCI)' },
  { id: 'maternal', label: 'Maternal Care (NHM ASHA)' },
  { id: 'emergency', label: 'Emergency Red-Flags' },
  { id: 'general', label: 'Infectious & Primary Care' }
];

const PROTOCOL_SAMPLES = [
  {
    id: "WHO_IMCI_2019_INFANT_PSBI_01",
    title: "Possible Serious Bacterial Infection (PSBI) in Infants",
    title_hi: "2 माह तक के नवजात में गंभीर जीवाणु संक्रमण (PSBI)",
    source: "WHO IMCI Young Infant (2019)",
    page: 1,
    urgency: "EMERGENCY",
    category: "pediatric",
    excerpt_hi: "Unable to feed, convulsions, severe chest indrawing, or temp >= 38.0°C indicates Very Severe Disease (PSBI). Keep warm and refer URGENTLY to hospital."
  },
  {
    id: "NHM_ASHA_M6_PREG_DANGER_01",
    title: "Antenatal Danger Signs & Severe Preeclampsia",
    title_hi: "गर्भावस्था के दौरान खतरे के गंभीर लक्षण",
    source: "NHM ASHA Module 6 (MoHFW)",
    page: 30,
    urgency: "EMERGENCY",
    category: "maternal",
    excerpt_hi: "Vaginal bleeding, absent fetal movement, severe headache with blurred vision, or facial edema require immediate 108 emergency hospital transfer."
  },
  {
    id: "NHM_ASHA_M6_PREG_DETECT_01",
    title: "Pregnancy Detection (Nishchay Kit) and EDD",
    title_hi: "गर्भावस्था का पता लगाना (निश्चय किट)",
    source: "NHM ASHA Module 6 (MoHFW)",
    page: 21,
    urgency: "HOME_CARE",
    category: "maternal",
    excerpt_hi: "On missed period, test 2 drops of morning urine on Nishchay card. Two purple bands indicate positive; register with ANM immediately for ANC."
  },
  {
    id: "NHM_ASHA_M7_ARI_PNEUMONIA_01",
    title: "Acute Respiratory Infection (ARI) and Pneumonia",
    title_hi: "श्वास में संक्रमण (ARI) और न्यूमोनिया की पहचान",
    source: "NHM ASHA Module 7 (MoHFW)",
    page: 29,
    urgency: "EMERGENCY",
    category: "pediatric",
    excerpt_hi: "Count respiratory rate for 1 full minute (2-12 mo: >=50 bpm; 1-5 yr: >=40 bpm). If chest indrawing present, classify Severe Pneumonia and refer immediately."
  },
  {
    id: "NHM_ADULT_CARDIO_01",
    title: "Acute Chest Pain & Myocardial Infarction",
    title_hi: "हार्ट अटैक (दिल का दौरा) एवं सीने में तेज दर्द",
    source: "NHM & ICMR Emergency Guidelines",
    page: 14,
    urgency: "EMERGENCY",
    category: "emergency",
    excerpt_hi: "Central substernal chest heaviness radiating to left arm or jaw with cold sweating indicates Acute MI. Keep patient seated and dial 108 immediately."
  },
  {
    id: "NHM_PRIMARY_COUGH_01",
    title: "Chronic Cough Lasting Over Two Weeks (TB)",
    title_hi: "2 सप्ताह से अधिक समय से खांसी (टीबी स्क्रीनिंग)",
    source: "NTEP & NHM Guidelines",
    page: 16,
    urgency: "SEE_DOCTOR_THIS_WEEK",
    category: "general",
    excerpt_hi: "Cough persisting over 2 weeks with evening fever, night sweats, or unexplained weight loss requires free sputum examination at nearest PHC/DMC."
  }
];

export default function GuidelinesSection() {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  const filtered = PROTOCOL_SAMPLES.filter(p => {
    const matchesCat = selectedCategory === 'all' || p.category === selectedCategory || (selectedCategory === 'emergency' && p.urgency === 'EMERGENCY');
    const matchesSearch = p.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          p.title_hi.includes(searchQuery) ||
                          p.source.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCat && matchesSearch;
  });

  return (
    <section id="guidelines-section" className="py-14 bg-slate-50/70 border-b border-slate-200/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-8">
          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 text-emerald-800 text-xs font-semibold mb-2 border border-emerald-200/60">
              <BookOpen className="w-3.5 h-3.5 text-emerald-600" />
              <span>Verified Clinical Knowledge Repository</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              67 Verified Clinical Protocols (WHO IMCI & NHM)
            </h2>
            <p className="text-xs sm:text-sm text-slate-500 mt-1 max-w-2xl">
              Grounded directly in MoHFW National Health Mission ASHA modules and WHO Integrated Management of Childhood Illness (2014 & 2019).
            </p>
          </div>

          {/* Search bar */}
          <div className="w-full md:w-72 relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
            <input 
              type="text"
              placeholder="Search clinical protocols..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-2 text-xs sm:text-sm bg-white border border-slate-200 rounded-xl focus:outline-hidden focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500"
            />
          </div>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-2 overflow-x-auto pb-3 mb-6 scrollbar-none">
          {CATEGORIES.map(cat => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all cursor-pointer ${
                selectedCategory === cat.id
                  ? 'bg-slate-900 text-white shadow-2xs'
                  : 'bg-white hover:bg-slate-100 text-slate-600 border border-slate-200'
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>

        {/* Protocols Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filtered.map((item, idx) => (
            <div 
              key={idx}
              className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-2xs hover:shadow-md transition-all flex flex-col justify-between space-y-4"
            >
              <div className="space-y-2.5">
                <div className="flex items-center justify-between gap-2">
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md ${
                    item.urgency === 'EMERGENCY'
                      ? 'bg-rose-50 text-rose-700 border border-rose-200'
                      : item.urgency === 'SEE_DOCTOR_TODAY'
                      ? 'bg-amber-50 text-amber-800 border border-amber-200'
                      : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                  }`}>
                    {item.urgency}
                  </span>
                  <span className="text-[11px] font-mono text-slate-400">
                    Page {item.page}
                  </span>
                </div>

                <div>
                  <h4 className="font-bold text-slate-900 text-sm">
                    {item.title}
                  </h4>
                  <p className="text-xs text-slate-400 font-normal">
                    {item.title_hi}
                  </p>
                </div>

                <p className="text-xs text-slate-600 leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-100">
                  {item.excerpt_hi}
                </p>
              </div>

              <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-400">
                <span className="font-medium text-slate-500 truncate max-w-[200px]">{item.source}</span>
                <span className="text-emerald-600 font-semibold flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Clinical Verified</span>
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Bottom Callout */}
        <div className="mt-8 p-4 rounded-xl bg-white border border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-600">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
            <span>
              All 67 clinical protocols indexed into <strong>BM25 Sparse</strong> and <strong>FAISS Dense (Cosine)</strong> stores for dual-track retrieval.
            </span>
          </div>
          <span className="font-mono text-slate-400 text-[11px]">
            guidelines_chunks.jsonl • 512-dim Normalized Cosine
          </span>
        </div>

      </div>
    </section>
  );
}

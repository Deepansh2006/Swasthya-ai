import React, { useState } from 'react';
import { 
  Key, 
  X, 
  CheckCircle2, 
  ShieldAlert, 
  ExternalLink 
} from 'lucide-react';

export default function KeyConfigModal({ isOpen, onClose }) {
  const [apiKey, setApiKey] = useState('');
  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleSave = async (e) => {
    e.preventDefault();
    if (!apiKey.trim()) return;
    setLoading(true);
    try {
      await fetch('/api/config/gemini', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ api_key: apiKey.trim() })
      });
      setSaved(true);
      setTimeout(() => {
        setSaved(false);
        onClose();
      }, 1000);
    } catch (err) {
      alert('कुंजी सहेजने में विफल।');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs transition-opacity">
      <div className="bg-white w-full max-w-md rounded-2xl border border-slate-200/90 shadow-2xl p-6 relative">
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="space-y-1 text-center pb-4 border-b border-slate-100">
          <div className="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center mx-auto mb-2 border border-indigo-100">
            <Key className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-slate-900">
            Google Gemini API Key कॉन्फ़िगरेशन
          </h3>
          <p className="text-xs text-slate-500">
            विस्तृत प्राकृतिक भाषा समझ और स्लॉट एक्सट्रैक्शन हेतु
          </p>
        </div>

        <form onSubmit={handleSave} className="space-y-4 pt-4">
          <div className="p-3 bg-emerald-50/60 border border-emerald-200/60 rounded-xl text-xs text-emerald-800">
            <strong>नोट:</strong> सिस्टम इस कुंजी के बिना भी अंतर्निहित 67 क्लिनिकल दिशानिर्देशों और आपातकालीन रेड-फ्लैग इंजन के साथ 
            <strong> 100% सुरक्षित और क्रियाशील </strong> है।
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Gemini API Key
            </label>
            <input 
              type="password"
              placeholder="AIzaSy..."
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="w-full px-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-hidden focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 font-mono"
            />
          </div>

          <div className="flex items-center justify-between text-[11px] text-slate-500">
            <a 
              href="https://aistudio.google.com/app/apikey" 
              target="_blank" 
              rel="noreferrer"
              className="inline-flex items-center gap-1 text-indigo-600 hover:underline font-medium"
            >
              <span>मुफ्त API Key प्राप्त करें</span>
              <ExternalLink className="w-3 h-3" />
            </a>
            <span>सुरक्षित इन-मेमोरी स्टोरेज</span>
          </div>

          <div className="pt-2">
            <button 
              type="submit"
              disabled={loading}
              className="w-full py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-semibold rounded-lg shadow-sm text-sm transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
            >
              {saved ? (
                <>
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>सफलतापूर्वक सहेजी गई!</span>
                </>
              ) : (
                <span>कुंजी सहेजें (Save API Key)</span>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

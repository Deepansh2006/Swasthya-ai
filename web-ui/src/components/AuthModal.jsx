import React, { useState } from 'react';
import { 
  X, 
  User, 
  Phone, 
  MapPin, 
  ShieldCheck, 
  CheckCircle2, 
  Sparkles,
  ArrowRight
} from 'lucide-react';

export default function AuthModal({ isOpen, onClose, onLoginSuccess }) {
  const [name, setName] = useState('Ramesh Kumar');
  const [phone, setPhone] = useState('9876543210');
  const [city, setCity] = useState('Lucknow, UP');
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleLogin = (e) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      const userObj = {
        name: name.trim() || 'Health User',
        phone: phone.trim() || '9876543210',
        city: city.trim() || 'India',
        userId: 'USR-' + Math.random().toString(36).substr(2, 6).toUpperCase()
      };
      localStorage.setItem('swasthya_ai_user', JSON.stringify(userObj));
      onLoginSuccess(userObj);
      onClose();
    }, 400);
  };

  const handleGuest = () => {
    const guestObj = {
      name: 'Guest User',
      phone: '',
      city: 'India',
      userId: 'GUEST-' + Math.random().toString(36).substr(2, 6).toUpperCase()
    };
    localStorage.setItem('swasthya_ai_user', JSON.stringify(guestObj));
    onLoginSuccess(guestObj);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs transition-opacity">
      <div className="bg-white w-full max-w-md rounded-2xl border border-slate-200/90 shadow-2xl p-6 relative animate-in fade-in zoom-in-95 duration-150">
        {/* Close Button */}
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="space-y-1 text-center pb-5 border-b border-slate-100">
          <div className="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center mx-auto mb-2 border border-emerald-100">
            <User className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold text-slate-900">
            Sign In / Register
          </h3>
          <p className="text-xs text-slate-500">
            Save your consultation history and continue follow-up advice anytime
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleLogin} className="space-y-4 pt-5">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Your Name (आपका नाम)
            </label>
            <div className="relative">
              <User className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input 
                type="text" 
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. Ramesh Kumar"
                required
                className="w-full pl-9 pr-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-hidden focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 font-medium"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Mobile Number or Email (मोबाइल नंबर या ईमेल)
            </label>
            <div className="relative">
              <Phone className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input 
                type="text" 
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="e.g. 9876543210"
                required
                className="w-full pl-9 pr-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-hidden focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 font-mono"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              City / District (शहर या जिला)
            </label>
            <div className="relative">
              <MapPin className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input 
                type="text" 
                value={city}
                onChange={(e) => setCity(e.target.value)}
                placeholder="e.g. Lucknow, Varanasi, Delhi"
                className="w-full pl-9 pr-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-hidden focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500"
              />
            </div>
          </div>

          <div className="pt-2 space-y-2">
            <button 
              type="submit"
              disabled={loading}
              className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold rounded-lg shadow-sm text-sm transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
            >
              {loading ? (
                <span>Signing In...</span>
              ) : (
                <>
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Sign In & Save My History</span>
                </>
              )}
            </button>

            <button 
              type="button"
              onClick={handleGuest}
              className="w-full py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium rounded-lg text-xs transition-colors cursor-pointer"
            >
              Continue as Guest (No Registration Needed)
            </button>
          </div>

          <div className="pt-2 text-center">
            <span className="text-[11px] text-slate-400">
              🔒 Your conversations are stored locally on your device for your privacy.
            </span>
          </div>
        </form>
      </div>
    </div>
  );
}

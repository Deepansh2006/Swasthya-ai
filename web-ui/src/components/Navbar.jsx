import React, { useState } from 'react';
import { 
  Activity, 
  PhoneCall, 
  User, 
  LogIn, 
  LogOut, 
  Menu, 
  X, 
  MessageSquare 
} from 'lucide-react';

export default function Navbar({ onOpenAuth, onScrollToSection, user, onLogout }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 bg-white/85 backdrop-blur-md border-b border-slate-200/80 transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Brand Logo & National Grounding Badges */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center text-white shadow-sm shadow-emerald-500/20">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-lg text-slate-900 tracking-tight">Swasthya-AI</span>
                <span className="text-[11px] font-semibold bg-emerald-50 text-emerald-700 px-2 py-0.5 rounded-full border border-emerald-200/60">
                  WHO & NHM
                </span>
              </div>
              <p className="text-xs text-slate-500 hidden sm:block">
                Voice-First AI Health & First-Aid Assistant
              </p>
            </div>
          </div>

          {/* Center Navigation Links */}
          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600">
            <button 
              onClick={() => onScrollToSection('chat-section')} 
              className="hover:text-emerald-600 transition-colors cursor-pointer flex items-center gap-1.5"
            >
              <MessageSquare className="w-4 h-4 text-emerald-600" />
              <span>AI Health Chat</span>
            </button>
            <button 
              onClick={() => onScrollToSection('guidelines-section')} 
              className="hover:text-emerald-600 transition-colors cursor-pointer"
            >
              Clinical Protocols (67)
            </button>
            <button 
              onClick={() => onScrollToSection('how-it-works')} 
              className="hover:text-emerald-600 transition-colors cursor-pointer"
            >
              How It Works
            </button>
          </nav>

          {/* Right Action Buttons */}
          <div className="hidden sm:flex items-center gap-3">
            {/* 108 Emergency Direct Fast-Dial */}
            <a 
              href="tel:108" 
              className="flex items-center gap-1.5 text-xs font-semibold bg-rose-50 text-rose-700 hover:bg-rose-100 border border-rose-200 px-3 py-1.5 rounded-lg transition-colors shadow-2xs"
            >
              <PhoneCall className="w-3.5 h-3.5 text-rose-600 animate-pulse" />
              <span>108 Ambulance SOS</span>
            </a>

            {/* User Login / User Status */}
            {user ? (
              <div className="flex items-center gap-2 pl-2 border-l border-slate-200">
                <div className="flex items-center gap-1.5 bg-slate-100 text-slate-800 text-xs font-medium px-2.5 py-1.5 rounded-lg">
                  <User className="w-3.5 h-3.5 text-slate-500" />
                  <span className="font-semibold">{user.name}</span>
                </div>
                <button 
                  onClick={onLogout}
                  className="p-1.5 text-slate-400 hover:text-rose-600 rounded-md transition-colors cursor-pointer"
                  title="Logout"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <button 
                onClick={onOpenAuth}
                className="flex items-center gap-1.5 text-xs font-semibold bg-slate-900 text-white hover:bg-slate-800 px-3.5 py-2 rounded-lg transition-all shadow-sm cursor-pointer"
              >
                <LogIn className="w-3.5 h-3.5" />
                <span>Sign In / Profile</span>
              </button>
            )}
          </div>

          {/* Mobile menu toggle */}
          <div className="flex md:hidden items-center gap-2">
            <a 
              href="tel:108" 
              className="flex items-center gap-1 text-xs font-bold bg-rose-600 text-white px-2.5 py-1.5 rounded-lg"
            >
              <PhoneCall className="w-3 h-3" />
              <span>108</span>
            </a>
            <button 
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 text-slate-600 rounded-lg hover:bg-slate-100"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-slate-200 bg-white px-4 pt-2 pb-4 space-y-2">
          <button 
            onClick={() => { onScrollToSection('chat-section'); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 text-sm font-medium text-slate-700"
          >
            AI Health Chat
          </button>
          <button 
            onClick={() => { onScrollToSection('guidelines-section'); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 text-sm font-medium text-slate-700"
          >
            Clinical Protocols (67)
          </button>
          <button 
            onClick={() => { onScrollToSection('how-it-works'); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 text-sm font-medium text-slate-700"
          >
            How It Works
          </button>
          <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
            {user ? (
              <button 
                onClick={onLogout}
                className="text-xs text-rose-600 font-semibold"
              >
                Logout ({user.name})
              </button>
            ) : (
              <button 
                onClick={() => { onOpenAuth(); setMobileMenuOpen(false); }}
                className="text-xs bg-slate-900 text-white px-3 py-1.5 rounded-md font-medium"
              >
                Sign In
              </button>
            )}
          </div>
        </div>
      )}
    </header>
  );
}

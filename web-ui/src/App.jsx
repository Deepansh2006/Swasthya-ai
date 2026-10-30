import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import ChatAgentWorkspace from './components/ChatAgentWorkspace';
import GuidelinesSection from './components/GuidelinesSection';
import HowItWorks from './components/HowItWorks';
import Footer from './components/Footer';
import AuthModal from './components/AuthModal';

export default function App() {
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);

  // Load user from localStorage on mount
  useEffect(() => {
    try {
      const savedUser = localStorage.getItem('swasthya_ai_user');
      if (savedUser) {
        setCurrentUser(JSON.parse(savedUser));
      }
    } catch (e) {
      console.warn("Could not load user profile:", e);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('swasthya_ai_user');
    setCurrentUser(null);
  };

  const scrollToSection = (id) => {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50/50 text-slate-900 selection:bg-emerald-100 selection:text-emerald-900">
      {/* Top Navbar with Profile & Emergency 108 */}
      <Navbar 
        onOpenAuth={() => setAuthModalOpen(true)}
        onScrollToSection={scrollToSection}
        user={currentUser}
        onLogout={handleLogout}
      />

      <main className="flex-1">
        {/* Hero Section */}
        <HeroSection 
          onStartTriage={() => scrollToSection('chat-section')}
          onExploreProtocols={() => scrollToSection('guidelines-section')}
        />

        {/* ChatGPT-Style Multi-Turn Health Agent Interface */}
        <ChatAgentWorkspace 
          currentUser={currentUser}
          onOpenAuth={() => setAuthModalOpen(true)}
        />

        {/* 67 Clinical Guidelines Section */}
        <GuidelinesSection />

        {/* How It Works Architecture Pipeline */}
        <HowItWorks />
      </main>

      {/* Footer */}
      <Footer onOpenAuth={() => setAuthModalOpen(true)} />

      {/* User Login / Registration Modal */}
      <AuthModal 
        isOpen={authModalOpen}
        onClose={() => setAuthModalOpen(false)}
        onLoginSuccess={(user) => setCurrentUser(user)}
      />
    </div>
  );
}

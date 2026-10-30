import React, { useState, useEffect, useRef } from 'react';
import { 
  Mic, 
  MicOff, 
  Play, 
  Square, 
  Volume2, 
  Sparkles, 
  ShieldAlert, 
  AlertTriangle, 
  Clock, 
  Home, 
  CheckCircle2, 
  PhoneCall, 
  ThumbsUp, 
  ThumbsDown, 
  RefreshCw, 
  FileText, 
  Stethoscope,
  Info
} from 'lucide-react';

const PRESET_VIGNETTES = [
  {
    title: "1. Infant High Fever + Convulsions (Emergency)",
    desc_hi: "शिशु में तेज बुखार व झटके",
    text: "मेरे 3 साल के बच्चे को 104 बुखार है और अभी शरीर अकड़ रहा है और मुंह से झाग आ रहा है",
    urgency: "EMERGENCY"
  },
  {
    title: "2. Snakebite with Rapid Swelling (Emergency)",
    desc_hi: "सर्पदंश / सांप का काटना",
    text: "खेत में काम करते हुए सांप ने पैर पर काट लिया है, दो निशान हैं और सूजन बहुत बढ़ रही है",
    urgency: "EMERGENCY"
  },
  {
    title: "3. Pregnancy Severe Headache & Vision Loss (Maternal Danger)",
    desc_hi: "गर्भवती में गंभीर सिरदर्द व धुंधला दिखना",
    text: "मेरी पत्नी 8 महीने की गर्भवती है, बहुत तेज सिरदर्द है और आंखों के आगे अंधेरा छा रहा है",
    urgency: "EMERGENCY"
  },
  {
    title: "4. Child Mild Diarrhea & Alert (Home Care)",
    desc_hi: "सामान्य दस्त एवं ओआरएस देखभाल",
    text: "मेरे 4 साल के बच्चे को सुबह से 2 बार पतला दस्त हुआ है, बच्चा खेल कूद रहा है और पानी पी रहा है",
    urgency: "HOME_CARE"
  },
  {
    title: "5. Home Pregnancy Test with Nishchay Kit (Home Care)",
    desc_hi: "निश्चय किट से गर्भ जांच",
    text: "मेरी पत्नी की माहवारी रुक गई है निश्चय किट से घर पर जांच कैसे करें",
    urgency: "HOME_CARE"
  },
  {
    title: "6. Cough > 2 Weeks with Night Sweats (Doctor This Week)",
    desc_hi: "दो हफ्ते से अधिक खांसी (टीबी स्क्रीनिंग)",
    text: "मुझे दो हफ्ते से ज्यादा समय से बलगम वाली खांसी आ रही है और रात में पसीना आता है",
    urgency: "SEE_DOCTOR_THIS_WEEK"
  }
];

export default function TriageWorkspace() {
  const [transcript, setTranscript] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const [feedbackGiven, setFeedbackGiven] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);

  const recognitionRef = useRef(null);
  const audioRef = useRef(null);
  const canvasRef = useRef(null);
  const animationFrameRef = useRef(null);

  // Initialize SpeechRecognition if supported
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const rec = new SpeechRecognition();
      rec.continuous = true;
      rec.interimResults = true;
      rec.lang = 'hi-IN';

      rec.onresult = (event) => {
        let currentText = '';
        for (let i = 0; i < event.results.length; i++) {
          currentText += event.results[i][0].transcript;
        }
        setTranscript(currentText);
      };

      rec.onerror = (e) => {
        console.error("Speech Recognition error:", e);
        setIsRecording(false);
      };

      rec.onend = () => {
        setIsRecording(false);
      };

      recognitionRef.current = rec;
    }
  }, []);

  // Visualizer Animation
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let phase = 0;

    const renderWave = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const width = canvas.width;
      const height = canvas.height;

      ctx.lineWidth = 2;
      ctx.strokeStyle = isRecording ? '#10b981' : '#cbd5e1';

      ctx.beginPath();
      for (let x = 0; x < width; x++) {
        const amplitude = isRecording ? 14 : 2;
        const frequency = isRecording ? 0.05 : 0.02;
        const y = height / 2 + Math.sin(x * frequency + phase) * amplitude;
        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();

      phase += isRecording ? 0.15 : 0.02;
      animationFrameRef.current = requestAnimationFrame(renderWave);
    };

    renderWave();
    return () => cancelAnimationFrame(animationFrameRef.current);
  }, [isRecording]);

  const toggleRecording = () => {
    if (isRecording) {
      if (recognitionRef.current) recognitionRef.current.stop();
      setIsRecording(false);
    } else {
      setTranscript('');
      if (recognitionRef.current) {
        try {
          recognitionRef.current.start();
          setIsRecording(true);
        } catch (e) {
          console.warn("Recognition already started or unsupported");
          setIsRecording(true);
        }
      } else {
        alert("आपका ब्राउज़र Web Speech API सपोर्ट नहीं करता। कृपया टेक्स्ट टाइप करें या नीचे दिए उदाहरण चुनें।");
      }
    }
  };

  const handleRunTriage = async (customText) => {
    const queryText = (customText !== undefined ? customText : transcript).trim();
    if (!queryText) return;

    setLoading(true);
    setResult(null);
    setFeedbackGiven(null);
    setAudioUrl(null);

    try {
      const resp = await fetch('/api/triage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          transcript: queryText,
          turn_number: 1
        })
      });

      if (!resp.ok) throw new Error("Triage API error");
      const data = await resp.json();
      setResult(data);

      // Auto synthesize TTS in background
      if (data.advice_hi) {
        fetchTTS(data.advice_hi);
      }
    } catch (err) {
      console.error("Triage failed:", err);
      alert("ट्राइएज अनुरोध में समस्या आई। कृपया सुनिश्चित करें कि बैकएंड चालू है।");
    } finally {
      setLoading(false);
    }
  };

  const fetchTTS = async (text) => {
    try {
      const resp = await fetch('/api/tts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
      if (resp.ok) {
        const audioData = await resp.json();
        if (audioData.audio_base64) {
          setAudioUrl(`data:audio/mp3;base64,${audioData.audio_base64}`);
        }
      }
    } catch (e) {
      console.warn("TTS failed:", e);
    }
  };

  const playAdviceAudio = () => {
    if (audioUrl) {
      if (audioRef.current) {
        audioRef.current.currentTime = 0;
        audioRef.current.play();
        setIsPlayingAudio(true);
      }
    } else if (window.speechSynthesis && result?.advice_hi) {
      const utterance = new SpeechSynthesisUtterance(result.advice_hi);
      utterance.lang = 'hi-IN';
      utterance.onend = () => setIsPlayingAudio(false);
      setIsPlayingAudio(true);
      window.speechSynthesis.speak(utterance);
    }
  };

  const handleFeedback = async (score) => {
    if (!result?.session_id) return;
    try {
      await fetch('/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: result.session_id,
          turn_number: 1,
          rating: score
        })
      });
      setFeedbackGiven(score);
    } catch (e) {
      console.error(e);
    }
  };

  const getUrgencyBadge = (level) => {
    switch (level) {
      case 'EMERGENCY':
        return {
          bg: 'bg-rose-50 text-rose-700 border-rose-200',
          badge: 'bg-rose-600 text-white',
          title: '🚨 EMERGENCY • Immediate Hospital Referral Required',
          desc: 'High-risk life-threatening symptoms detected. Call 108 Emergency Ambulance immediately.',
          icon: ShieldAlert
        };
      case 'SEE_DOCTOR_TODAY':
        return {
          bg: 'bg-amber-50 text-amber-800 border-amber-200',
          badge: 'bg-amber-600 text-white',
          title: '⚠️ SEE DOCTOR TODAY • Visit PHC / CHC Center Today',
          desc: 'Potential complications. Patient must be evaluated by a medical officer within 24 hours.',
          icon: AlertTriangle
        };
      case 'SEE_DOCTOR_THIS_WEEK':
        return {
          bg: 'bg-blue-50 text-blue-800 border-blue-200',
          badge: 'bg-blue-600 text-white',
          title: '📋 SEE DOCTOR THIS WEEK • Routine OPD Investigation',
          desc: 'Non-critical condition requiring standard diagnostic workup (e.g. sputum test, blood test).',
          icon: Clock
        };
      case 'HOME_CARE':
      default:
        return {
          bg: 'bg-emerald-50 text-emerald-800 border-emerald-200',
          badge: 'bg-emerald-600 text-white',
          title: '🏡 HOME CARE & MONITORING • First-Aid & Hydration',
          desc: 'Manageable at home with ASHA kit (ORS, Zinc, hydration) and watchful observation for danger signs.',
          icon: Home
        };
    }
  };

  return (
    <section id="triage-section" className="py-12 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto space-y-2 mb-10">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-100 text-slate-700 text-xs font-semibold">
            <Stethoscope className="w-3.5 h-3.5 text-emerald-600" />
            <span>Interactive Clinical Workspace</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Patient Symptom Voice & Text Triage
          </h2>
          <p className="text-sm sm:text-base text-slate-600">
            Click the microphone to speak naturally in Hindi, or type patient symptoms below. Evaluated against WHO IMCI and National Health Mission protocols in real-time.
          </p>
        </div>

        {/* Workspace Layout: Left Input Panel + Right Results Panel */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Left: Input & Speech Panel */}
          <div className="lg:col-span-6 space-y-6">
            <div className="bg-slate-50/80 rounded-2xl p-6 border border-slate-200 shadow-sm space-y-5">
              
              {/* Audio Visualizer & Mic Button */}
              <div className="flex flex-col items-center justify-center p-6 bg-white rounded-xl border border-slate-200/80 space-y-4">
                <canvas 
                  ref={canvasRef} 
                  width={320} 
                  height={44} 
                  className="w-full max-w-xs h-11 rounded"
                />

                <div className="flex items-center gap-4">
                  <button
                    onClick={toggleRecording}
                    className={`w-16 h-16 rounded-full flex items-center justify-center transition-all shadow-md cursor-pointer ${
                      isRecording 
                        ? 'bg-rose-600 hover:bg-rose-700 text-white animate-pulse shadow-rose-500/30 ring-4 ring-rose-200' 
                        : 'bg-emerald-600 hover:bg-emerald-700 text-white shadow-emerald-500/30'
                    }`}
                    title={isRecording ? "Stop Recording" : "Speak in Hindi"}
                  >
                    {isRecording ? <MicOff className="w-7 h-7" /> : <Mic className="w-7 h-7" />}
                  </button>
                </div>

                <div className="text-center">
                  <span className="text-xs font-semibold text-slate-700">
                    {isRecording ? "Listening... Speak in Hindi (Web Speech API Active)" : "Click Microphone & Speak in Hindi"}
                  </span>
                  <p className="text-[11px] text-slate-400">
                    Example: "बच्चे को 104 बुखार है और उल्टी हो रही है"
                  </p>
                </div>
              </div>

              {/* Text Area for Transcript / Manual Edits */}
              <div className="space-y-1.5">
                <div className="flex items-center justify-between text-xs text-slate-500 font-medium">
                  <span>Patient Spoken Transcript (Hindi / Hinglish)</span>
                  <span>{transcript ? transcript.split(/\s+/).filter(Boolean).length : 0} words</span>
                </div>
                <textarea
                  rows={4}
                  value={transcript}
                  onChange={(e) => setTranscript(e.target.value)}
                  placeholder="Type symptoms in Hindi or speak via microphone above..."
                  className="w-full p-3.5 bg-white border border-slate-200 rounded-xl text-slate-900 text-sm focus:outline-hidden focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 font-normal leading-relaxed resize-none shadow-2xs"
                />
              </div>

              {/* Triage Submit Button */}
              <div className="flex items-center gap-3">
                <button
                  onClick={() => handleRunTriage()}
                  disabled={loading || !transcript.trim()}
                  className="flex-1 py-3 bg-slate-900 hover:bg-slate-800 text-white font-semibold rounded-xl shadow-sm text-sm transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <>
                      <RefreshCw className="w-4 h-4 animate-spin text-emerald-400" />
                      <span>Checking Clinical Protocols...</span>
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4 text-emerald-400" />
                      <span>Run Clinical Triage Evaluation</span>
                    </>
                  )}
                </button>

                {transcript && (
                  <button
                    onClick={() => { setTranscript(''); setResult(null); }}
                    className="p-3 text-slate-400 hover:text-slate-700 border border-slate-200 bg-white rounded-xl transition-colors cursor-pointer"
                    title="Clear Text"
                  >
                    <RefreshCw className="w-4 h-4" />
                  </button>
                )}
              </div>
            </div>

            {/* Quick Demo Vignette Chips */}
            <div className="space-y-2.5">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block">
                Clinical Test Cases (Viva Demo Presets):
              </span>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {PRESET_VIGNETTES.map((vig, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setTranscript(vig.text);
                      handleRunTriage(vig.text);
                    }}
                    className="text-left p-2.5 bg-white hover:bg-slate-50 border border-slate-200/90 rounded-xl transition-all shadow-2xs group cursor-pointer"
                  >
                    <div className="flex items-center justify-between text-xs font-semibold text-slate-800 group-hover:text-emerald-700">
                      <span>{vig.title}</span>
                    </div>
                    <p className="text-[11px] text-emerald-700 font-medium truncate mt-0.5">
                      Hindi: "{vig.desc_hi || vig.text}"
                    </p>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Right: Triage Response Card & Guideline Citations */}
          <div className="lg:col-span-6 space-y-6">
            {result ? (
              <div className="bg-white rounded-2xl border border-slate-200/90 shadow-md p-6 space-y-6 animate-in fade-in duration-200">
                
                {/* Urgency Classification Header */}
                {(() => {
                  const style = getUrgencyBadge(result.urgency_level);
                  const Icon = style.icon;
                  return (
                    <div className={`p-4 rounded-xl border ${style.bg} space-y-2`}>
                      <div className="flex items-center justify-between flex-wrap gap-2">
                        <span className={`px-3 py-1 rounded-md text-xs font-bold ${style.badge} shadow-xs`}>
                          {result.urgency_level}
                        </span>
                        <div className="flex items-center gap-2 text-xs font-mono font-medium">
                          <span>Latency:</span>
                          <span className="font-bold bg-white/80 px-2 py-0.5 rounded border border-slate-200/60">
                            {result.execution_latency_ms} ms
                          </span>
                        </div>
                      </div>

                      <div className="flex items-start gap-2.5 pt-1">
                        <Icon className="w-5 h-5 shrink-0 mt-0.5" />
                        <div>
                          <h4 className="font-bold text-sm sm:text-base leading-tight">
                            {style.title}
                          </h4>
                          <p className="text-xs opacity-90 mt-0.5">
                            {style.desc}
                          </p>
                        </div>
                      </div>
                    </div>
                  );
                })()}

                {/* Emergency 108 SOS Call Trigger */}
                {result.urgency_level === 'EMERGENCY' && (
                  <div className="p-4 bg-rose-600 text-white rounded-xl shadow-md flex items-center justify-between gap-4 animate-in slide-in-from-top-2">
                    <div>
                      <div className="font-bold text-sm sm:text-base flex items-center gap-1.5">
                        <PhoneCall className="w-4 h-4 animate-bounce" />
                        <span>Call 108 Emergency Ambulance Immediately</span>
                      </div>
                      <p className="text-xs text-rose-100">
                        Patient exhibits acute danger signs requiring immediate secondary hospital transfer.
                      </p>
                    </div>
                    <a
                      href="tel:108"
                      className="px-4 py-2 bg-white text-rose-700 hover:bg-rose-50 font-bold text-sm rounded-lg shadow-sm whitespace-nowrap transition-colors"
                    >
                      Dial 108
                    </a>
                  </div>
                )}

                {/* Clinical Guidance in Clear Hindi with English Label */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
                      <FileText className="w-4 h-4 text-emerald-600" />
                      <span>Primary First-Aid & Referral Guidance:</span>
                    </span>

                    {/* Audio Listen Button */}
                    <button
                      onClick={playAdviceAudio}
                      className="flex items-center gap-1 text-xs font-semibold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200/80 px-2.5 py-1 rounded-lg transition-colors cursor-pointer"
                    >
                      <Volume2 className="w-3.5 h-3.5 text-emerald-600" />
                      <span>{isPlayingAudio ? "Playing Audio..." : "Listen Spoken Hindi"}</span>
                    </button>
                  </div>

                  <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 text-sm leading-relaxed whitespace-pre-line font-medium">
                    {result.advice_hi}
                  </div>
                </div>

                {/* Warning Signs to Watch */}
                {result.warning_signs_hi && (
                  <div className="p-3.5 rounded-xl bg-amber-50/70 border border-amber-200/80 text-amber-900 text-xs space-y-1">
                    <strong className="font-bold flex items-center gap-1.5 text-amber-800">
                      <AlertTriangle className="w-4 h-4 text-amber-600" />
                      <span>Key Red-Flags to Watch (खतरे के लक्षण):</span>
                    </strong>
                    <p className="leading-relaxed">
                      {result.warning_signs_hi}
                    </p>
                  </div>
                )}

                {/* Grounded Guidelines Citations */}
                {result.sources && result.sources.length > 0 && (
                  <div className="space-y-2 pt-2 border-t border-slate-100">
                    <span className="text-xs font-bold text-slate-600 uppercase tracking-wider block">
                      Verified Clinical Protocol Citations (Evidence Grounding):
                    </span>
                    <div className="space-y-2">
                      {result.sources.map((src, i) => (
                        <div key={i} className="p-3 bg-slate-50 rounded-xl border border-slate-200/80 text-xs space-y-1">
                          <div className="flex items-center justify-between font-semibold text-slate-800">
                            <span className="truncate pr-2">{src.protocol}</span>
                            <span className="text-[10px] text-emerald-700 bg-emerald-100/70 px-1.5 py-0.5 rounded font-mono shrink-0">
                              Relevance: {Math.round(src.relevance_score * 100)}%
                            </span>
                          </div>
                          <p className="text-slate-500 text-[11px]">
                            {src.source} • Page {src.page}
                          </p>
                          <p className="text-slate-700 text-xs italic bg-white p-2 rounded border border-slate-100 line-clamp-2">
                            "{src.excerpt}"
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Feedback Action Buttons */}
                <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                  <span>Was this clinical guidance accurate and helpful?</span>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleFeedback(1)}
                      className={`p-1.5 rounded-lg border transition-colors cursor-pointer ${
                        feedbackGiven === 1 
                          ? 'bg-emerald-50 border-emerald-300 text-emerald-700 font-bold' 
                          : 'border-slate-200 hover:bg-slate-50 text-slate-600'
                      }`}
                      title="Helpful (Thumbs Up)"
                    >
                      <ThumbsUp className="w-3.5 h-3.5" />
                    </button>
                    <button
                      onClick={() => handleFeedback(-1)}
                      className={`p-1.5 rounded-lg border transition-colors cursor-pointer ${
                        feedbackGiven === -1 
                          ? 'bg-rose-50 border-rose-300 text-rose-700 font-bold' 
                          : 'border-slate-200 hover:bg-slate-50 text-slate-600'
                      }`}
                      title="Needs Refinement (Thumbs Down)"
                    >
                      <ThumbsDown className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>

                {audioUrl && (
                  <audio 
                    ref={audioRef} 
                    src={audioUrl} 
                    onEnded={() => setIsPlayingAudio(false)} 
                    className="hidden" 
                  />
                )}
              </div>
            ) : (
              /* Empty Placeholder State */
              <div className="bg-slate-50/60 rounded-2xl border-2 border-dashed border-slate-200 p-12 text-center space-y-4">
                <div className="w-14 h-14 bg-white rounded-2xl shadow-xs border border-slate-200 flex items-center justify-center mx-auto text-slate-400">
                  <Stethoscope className="w-7 h-7 text-slate-400" />
                </div>
                <div className="max-w-sm mx-auto space-y-1">
                  <h4 className="font-bold text-slate-800 text-sm sm:text-base">
                    Clinical Triage Evaluation Appears Here
                  </h4>
                  <p className="text-xs text-slate-500 leading-relaxed">
                    Click the microphone on the left or select a preset vignette above. 
                    Our dual-path clinical engine will cross-check 67 protocols in real-time.
                  </p>
                </div>
              </div>
            )}
          </div>

        </div>
      </div>
    </section>
  );
}

// app.js - Frontend Logic for Voice-First Hindi Health Triage Assistant

let currentSessionId = null;
let currentTurn = 1;
let isRecording = false;
let recognition = null;
let audioContext = null;
let analyser = null;
let microphone = null;
let visualizerAnimationId = null;
let recordingStartTime = null;
let timerInterval = null;
let lastTriageResult = null;

// DOM Elements
const micBtn = document.getElementById('micBtn');
const recordingStatus = document.getElementById('recordingStatus');
const timerDisplay = document.getElementById('timerDisplay');
const transcriptInput = document.getElementById('transcriptInput');
const charCount = document.getElementById('charCount');
const triageBtn = document.getElementById('triageBtn');
const clearBtn = document.getElementById('clearBtn');
const visualizerCanvas = document.getElementById('audioVisualizer');
const canvasCtx = visualizerCanvas.getContext('2d');

const idleState = document.getElementById('idleState');
const loadingState = document.getElementById('loadingState');
const resultState = document.getElementById('resultState');

const urgencyBanner = document.getElementById('urgencyBanner');
const urgencyIcon = document.getElementById('urgencyIcon');
const urgencyTitle = document.getElementById('urgencyTitle');
const fastPathPill = document.getElementById('fastPathPill');
const emergencySOSBox = document.getElementById('emergencySOSBox');
const adviceText = document.getElementById('adviceText');
const warningBox = document.getElementById('warningBox');
const warningText = document.getElementById('warningText');
const followupBox = document.getElementById('followupBox');
const followupText = document.getElementById('followupText');
const slotsDisplay = document.getElementById('slotsDisplay');
const sourcesList = document.getElementById('sourcesList');
const latencyBadge = document.getElementById('latencyBadge');
const playAudioBtn = document.getElementById('playAudioBtn');
const audioElement = document.getElementById('audioElement');

// Modals
const benchmarkModal = document.getElementById('benchmarkModal');
const viewBenchmarkBtn = document.getElementById('viewBenchmarkBtn');
const closeModalBtn = document.getElementById('closeModalBtn');

const keyModal = document.getElementById('keyModal');
const configKeyBtn = document.getElementById('configKeyBtn');
const closeKeyModalBtn = document.getElementById('closeKeyModalBtn');
const geminiKeyInput = document.getElementById('geminiKeyInput');
const saveKeyBtn = document.getElementById('saveKeyBtn');

// Feedback
const thumbUpBtn = document.getElementById('thumbUpBtn');
const thumbDownBtn = document.getElementById('thumbDownBtn');
const feedbackThanks = document.getElementById('feedbackThanks');

// -----------------------------------------------------------------------------
// Initialization
// -----------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    initSession();
    initSpeechRecognition();
    setupCanvas();
    setupEventListeners();
});

async function initSession() {
    try {
        const res = await fetch('/api/session', { method: 'POST' });
        const data = await res.json();
        currentSessionId = data.session_id;
    } catch (e) {
        currentSessionId = 'sess_' + Math.random().toString(36).substring(2, 8);
    }
}

function setupCanvas() {
    canvasCtx.fillStyle = 'rgba(0, 0, 0, 0.2)';
    canvasCtx.fillRect(0, 0, visualizerCanvas.width, visualizerCanvas.height);
}

// -----------------------------------------------------------------------------
// Voice Recognition (Browser Web Speech API Hindi)
// -----------------------------------------------------------------------------
function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'hi-IN'; // Hindi (India)

        recognition.onstart = () => {
            isRecording = true;
            micBtn.classList.add('recording');
            recordingStatus.textContent = 'सुन रहा हूँ... बोलिए (Listening...)';
            startTimer();
            startVisualizer();
        };

        recognition.onresult = (event) => {
            let finalTranscript = '';
            for (let i = 0; i < event.results.length; ++i) {
                finalTranscript += event.results[i][0].transcript;
            }
            transcriptInput.value = finalTranscript;
            updateCharCount();
        };

        recognition.onerror = (event) => {
            console.warn('Speech recognition error:', event.error);
            stopRecording();
            recordingStatus.textContent = 'माइक त्रुटि। कृपया टाइप करें।';
        };

        recognition.onend = () => {
            stopRecording();
        };
    } else {
        recordingStatus.textContent = 'ब्राउज़र में वॉइस API उपलब्ध नहीं है। कृपया टाइप करें।';
    }
}

function toggleRecording() {
    if (!isRecording) {
        if (recognition) {
            try {
                recognition.start();
            } catch (e) {
                console.error(e);
            }
        } else {
            alert('इस ब्राउज़र में स्पीच रिकग्निशन समर्थित नहीं है। कृपया सीधे टेक्स्ट बॉक्स में टाइप करें।');
        }
    } else {
        if (recognition) {
            recognition.stop();
        }
        stopRecording();
    }
}

function stopRecording() {
    isRecording = false;
    micBtn.classList.remove('recording');
    recordingStatus.textContent = 'माइक बटन दबाएं और समस्या बताएं';
    stopTimer();
    stopVisualizer();
}

function startTimer() {
    recordingStartTime = Date.now();
    timerInterval = setInterval(() => {
        const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
        const mins = String(Math.floor(elapsed / 60)).padStart(2, '0');
        const secs = String(elapsed % 60).padStart(2, '0');
        timerDisplay.textContent = `${mins}:${secs} / 01:00`;
        if (elapsed >= 60) {
            stopRecording();
        }
    }, 500);
}

function stopTimer() {
    clearInterval(timerInterval);
}

function startVisualizer() {
    let phase = 0;
    function draw() {
        if (!isRecording) return;
        canvasCtx.fillStyle = 'rgba(15, 23, 42, 0.4)';
        canvasCtx.fillRect(0, 0, visualizerCanvas.width, visualizerCanvas.height);

        canvasCtx.lineWidth = 2;
        canvasCtx.strokeStyle = '#38bdf8';
        canvasCtx.beginPath();

        const sliceWidth = visualizerCanvas.width / 40;
        let x = 0;

        for (let i = 0; i < 40; i++) {
            const v = Math.sin(phase + i * 0.2) * 18 + Math.random() * 8;
            const y = visualizerCanvas.height / 2 + v;
            if (i === 0) canvasCtx.moveTo(x, y);
            else canvasCtx.lineTo(x, y);
            x += sliceWidth;
        }

        canvasCtx.stroke();
        phase += 0.15;
        visualizerAnimationId = requestAnimationFrame(draw);
    }
    draw();
}

function stopVisualizer() {
    if (visualizerAnimationId) {
        cancelAnimationFrame(visualizerAnimationId);
    }
    setupCanvas();
}

// -----------------------------------------------------------------------------
// Triage Pipeline API Execution
// -----------------------------------------------------------------------------
async function executeTriage() {
    const text = transcriptInput.value.trim();
    if (!text) {
        alert('कृपया अपनी समस्या बोलें या टेक्स्ट बॉक्स में लिखें।');
        return;
    }

    // Switch to loading
    idleState.classList.add('hidden');
    resultState.classList.add('hidden');
    loadingState.classList.remove('hidden');

    try {
        const response = await fetch('/api/triage', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: currentSessionId,
                transcript: text,
                turn_number: currentTurn
            })
        });

        if (!response.ok) {
            throw new Error('ट्राइएज सेवा प्रतिक्रिया देने में विफल रही।');
        }

        const data = await response.json();
        lastTriageResult = data;
        renderTriageResult(data);
        currentTurn++;

    } catch (err) {
        alert('त्रुटि: ' + err.message);
        idleState.classList.remove('hidden');
    } finally {
        loadingState.classList.add('hidden');
    }
}

function renderTriageResult(data) {
    resultState.classList.remove('hidden');

    // Urgency Banner Styling
    urgencyBanner.style.borderLeftColor = data.urgency_color;
    urgencyTitle.textContent = data.urgency_badge_hi;
    urgencyTitle.style.color = data.urgency_color;

    // Fast-path badge
    if (data.is_emergency && data.rule_urgency === 'EMERGENCY') {
        fastPathPill.classList.remove('hidden');
    } else {
        fastPathPill.classList.add('hidden');
    }

    // Call 108 SOS button
    if (data.call_108_recommended || data.is_emergency) {
        emergencySOSBox.classList.remove('hidden');
        urgencyIcon.textContent = '🚨';
    } else {
        emergencySOSBox.classList.add('hidden');
        urgencyIcon.textContent = data.urgency_level === 'HOME_CARE' ? '🟢' : '🩺';
    }

    // Advice & Warning
    adviceText.textContent = data.advice_hi;
    if (data.warning_signs_hi) {
        warningBox.classList.remove('hidden');
        warningText.textContent = data.warning_signs_hi;
    } else {
        warningBox.classList.add('hidden');
    }

    // Follow-up question
    if (data.follow_up_question_hi) {
        followupBox.classList.remove('hidden');
        followupText.textContent = data.follow_up_question_hi;
    } else {
        followupBox.classList.add('hidden');
    }

    // Extracted Slots
    slotsDisplay.textContent = JSON.stringify(data.extracted_slots || {}, null, 2);

    // Sources List
    sourcesList.innerHTML = '';
    if (data.sources && data.sources.length > 0) {
        data.sources.forEach(src => {
            const item = document.createElement('div');
            item.className = 'source-item';
            item.innerHTML = `
                <div class="source-title">${src.source} (${src.protocol})</div>
                <div class="source-meta">पृष्ठ सं. ${src.page} • प्रासंगिकता: ${Math.round(src.relevance_score * 100)}%</div>
                <div class="source-excerpt">"${src.excerpt}"</div>
            `;
            sourcesList.appendChild(item);
        });
    } else {
        sourcesList.innerHTML = '<div class="source-meta">कोई विशिष्ट संदर्भ उद्धृत नहीं।</div>';
    }

    latencyBadge.textContent = `विलंबता: ${data.execution_latency_ms} ms`;
    feedbackThanks.classList.add('hidden');

    // Auto-synthesize voice
    speakHindiAdvice(data.advice_hi);
}

// -----------------------------------------------------------------------------
// Voice Synthesis (TTS)
// -----------------------------------------------------------------------------
async function speakHindiAdvice(text) {
    if (!text) return;

    playAudioBtn.disabled = true;
    const playText = document.getElementById('playText');
    playText.textContent = 'ऑडियो तैयार हो रहा है...';

    try {
        const res = await fetch('/api/tts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text, language: 'hi' })
        });
        const data = await res.json();

        if (data.audio_url) {
            audioElement.src = data.audio_url;
            audioElement.play();
            playText.textContent = 'पुनः सुनें (Replay Hindi Voice)';
        } else {
            // Fallback to browser SpeechSynthesis
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'hi-IN';
                window.speechSynthesis.speak(utterance);
                playText.textContent = 'सुन रहे हैं... (Playing)';
            }
        }
    } catch (e) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'hi-IN';
            window.speechSynthesis.speak(utterance);
        }
    } finally {
        playAudioBtn.disabled = false;
    }
}

// -----------------------------------------------------------------------------
// Event Handlers & Presets
// -----------------------------------------------------------------------------
function setupEventListeners() {
    micBtn.addEventListener('click', toggleRecording);
    triageBtn.addEventListener('click', executeTriage);

    clearBtn.addEventListener('click', () => {
        transcriptInput.value = '';
        updateCharCount();
        idleState.classList.remove('hidden');
        resultState.classList.add('hidden');
    });

    transcriptInput.addEventListener('input', updateCharCount);

    // Preset Chips
    document.querySelectorAll('.preset-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const text = chip.getAttribute('data-text');
            transcriptInput.value = text;
            updateCharCount();
            executeTriage();
        });
    });

    // Play Audio Button
    playAudioBtn.addEventListener('click', () => {
        if (lastTriageResult && lastTriageResult.advice_hi) {
            speakHindiAdvice(lastTriageResult.advice_hi);
        }
    });

    // Modals
    viewBenchmarkBtn.addEventListener('click', () => benchmarkModal.classList.remove('hidden'));
    closeModalBtn.addEventListener('click', () => benchmarkModal.classList.add('hidden'));

    configKeyBtn.addEventListener('click', () => keyModal.classList.remove('hidden'));
    closeKeyModalBtn.addEventListener('click', () => keyModal.classList.add('hidden'));

    saveKeyBtn.addEventListener('click', async () => {
        const key = geminiKeyInput.value.trim();
        if (!key) return;
        try {
            await fetch('/api/config/gemini', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ api_key: key })
            });
            alert('Gemini API Key सफलतापूर्वक सहेजी गई!');
            keyModal.classList.add('hidden');
        } catch (e) {
            alert('कुंजी सहेजने में त्रुटि।');
        }
    });

    // Feedback
    thumbUpBtn.addEventListener('click', () => sendFeedback(1));
    thumbDownBtn.addEventListener('click', () => sendFeedback(-1));
}

function updateCharCount() {
    const text = transcriptInput.value.trim();
    const words = text ? text.split(/\s+/).length : 0;
    charCount.textContent = `${words} शब्द`;
}

async function sendFeedback(rating) {
    try {
        await fetch('/api/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: currentSessionId,
                turn_number: currentTurn,
                rating: rating
            })
        });
        feedbackThanks.classList.remove('hidden');
    } catch (e) {
        console.error(e);
    }
}

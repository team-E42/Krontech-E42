let currentLanguage = 'en-US';

const textInput = document.getElementById('textInput');
const speakBtn = document.getElementById('speakBtn');
const stopBtn = document.getElementById('stopBtn');

const synth = window.speechSynthesis;

let voices = synth.getVoices();
synth.onvoiceschanged = () => { voices = synth.getVoices() };

const langToggle = document.getElementById('langToggle');

langToggle.addEventListener('click', () => {
    if (currentLanguage === "en-US") {
        currentLanguage = "ro-RO";
        langToggle.textContent = "🌐 Română";
    } else {
        currentLanguage = "en-US";
        langToggle.textContent = "🌐 English";
    }
});

speakBtn.addEventListener('click', () => {
    const text = textInput.value;
    if (text) {
        const utterance = new SpeechSynthesisUtterance(text);

        const voice = voices.find(v => v.lang === currentLanguage);
        if (voice) utterance.voice = voice;

        utterance.lang = currentLanguage;
        utterance.rate = .9;
        utterance.pitch = 2;  
        utterance.volume = 1; 

        synth.speak(utterance);
    }
});

stopBtn.addEventListener('click', () => {
    synth.cancel();
});
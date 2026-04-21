// Frontend Logic
const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const recordBtn = document.getElementById('recordBtn');
const toggleSpeechBtn = document.getElementById('toggleSpeechBtn');

const settingsModal = document.getElementById('settingsModal');
const apiKeyInput = document.getElementById('apiKeyInput');
const saveKeyBtn = document.getElementById('saveKeyBtn');
const openSettingsBtn = document.getElementById('openSettingsBtn');

let ws = null;
let synthesisEnabled = false;

// Initialize Settings Check
const savedKey = localStorage.getItem('gemini_api_key');
if (savedKey) {
    settingsModal.classList.add('hidden');
    connectWebSocket(savedKey);
}

openSettingsBtn.addEventListener('click', () => {
    settingsModal.classList.remove('hidden');
    apiKeyInput.value = localStorage.getItem('gemini_api_key') || '';
});

saveKeyBtn.addEventListener('click', () => {
    const key = apiKeyInput.value.trim();
    if (key.length > 5) {
        localStorage.setItem('gemini_api_key', key);
        settingsModal.classList.add('hidden');
        connectWebSocket(key);
    } else {
        alert("Please enter a valid API Key.");
    }
});

function connectWebSocket(apiKey) {
    if (ws) ws.close();
    
    // Connect to FastAPI WebSocket
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    ws = new WebSocket(`${protocol}//${window.location.host}/ws/chat`);
    
    ws.onopen = () => {
        ws.send(JSON.stringify({ api_key: apiKey }));
        userInput.disabled = false;
        userInput.focus();
    };
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.error) {
            appendMessage(data.error, 'system-message');
            localStorage.removeItem('gemini_api_key');
            settingsModal.classList.remove('hidden');
        } else {
            appendMessage(data.message, data.type === 'system' ? 'system-message' : 'bot-message');
            updateTimeline(data.message);
            if (synthesisEnabled && data.type !== 'system') {
                speakText(data.message);
            }
        }
    };
    
    ws.onclose = () => {
        userInput.disabled = true;
    };
}

function appendMessage(text, className) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${className}`;
    
    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    
    // Parse Markdown if it's from the bot
    if (className === 'bot-message') {
        bubble.innerHTML = marked.parse(text);
    } else {
        bubble.textContent = text;
    }
    
    msgDiv.appendChild(bubble);
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Sending Messages
function sendMessage() {
    const text = userInput.value.trim();
    if (text && ws && ws.readyState === WebSocket.OPEN) {
        appendMessage(text, 'user-message');
        ws.send(text);
        userInput.value = '';
    }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// Timeline Progress Logic
const steps = ['eligibility', 'registration', 'research', 'voting method', 'polling '];
function updateTimeline(text) {
    const lowerText = text.toLowerCase();
    
    if (lowerText.includes('register') || lowerText.includes('registration')) {
        document.getElementById('step-1').classList.add('completed');
        document.getElementById('step-2').classList.add('active');
    }
    if (lowerText.includes('research') || lowerText.includes('candidate')) {
        document.getElementById('step-2').classList.add('completed');
        document.getElementById('step-3').classList.add('active');
    }
    if (lowerText.includes('mail') || lowerText.includes('in-person')) {
        document.getElementById('step-3').classList.add('completed');
        document.getElementById('step-4').classList.add('active');
    }
    if (lowerText.includes('poll') || lowerText.includes('location')) {
        document.getElementById('step-4').classList.add('completed');
        document.getElementById('step-5').classList.add('active');
    }
}

// Voice Features: Web Speech API
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    
    recognition.onstart = () => {
        recordBtn.classList.add('recording');
    };
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        userInput.value = transcript;
        sendMessage();
    };
    
    recognition.onend = () => {
        recordBtn.classList.remove('recording');
    };
    
    recordBtn.addEventListener('mousedown', () => recognition.start());
} else {
    recordBtn.style.display = 'none';
}

toggleSpeechBtn.addEventListener('click', () => {
    synthesisEnabled = !synthesisEnabled;
    toggleSpeechBtn.classList.toggle('active', synthesisEnabled);
    if (!synthesisEnabled) window.speechSynthesis.cancel();
});

function speakText(text) {
    // Strip markdown for speech
    const plainText = text.replace(/[*_#\[\]]/g, '');
    const utterThis = new SpeechSynthesisUtterance(plainText);
    utterThis.pitch = 1;
    utterThis.rate = 1.05;
    window.speechSynthesis.speak(utterThis);
}

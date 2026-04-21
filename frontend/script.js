const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const recordBtn = document.getElementById('recordBtn');
const toggleSpeechBtn = document.getElementById('toggleSpeechBtn');
const themeToggleBtn = document.getElementById('themeToggleBtn');

let synthesisEnabled = false;
let sessionId = "session_" + Math.random().toString(36).substring(7);

// Initialize Theme
if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
    themeToggleBtn.innerHTML = '<i class="fa-solid fa-sun"></i>';
}

themeToggleBtn.addEventListener('click', () => {
    document.body.classList.toggle("dark-mode");
    const isDark = document.body.classList.contains("dark-mode");
    localStorage.setItem("theme", isDark ? "dark" : "light");
    themeToggleBtn.innerHTML = isDark ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
});

function appendMessage(text, className, additionalHtml = '') {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${className}`;
    
    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    
    bubble.innerHTML = text + additionalHtml;
    
    msgDiv.appendChild(bubble);
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function handleAction(action, actionData) {
    if (action === "trigger_maps" && actionData?.zip_code) {
        try {
            const res = await fetch(`/locations?zip_code=${actionData.zip_code}`);
            const data = await res.json();
            return `<div class="integration-card">
                <i class="fa-solid fa-map-pin"></i> 
                <strong>Found:</strong> ${data.address}<br>
                <a href="${data.maps_url}" target="_blank">Open in Google Maps ➔</a>
            </div>`;
        } catch(e) { console.error(e); }
    }
    
    if (action === "trigger_calendar") {
        try {
            const res = await fetch(`/reminder`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({})
            });
            const data = await res.json();
            return `<div class="integration-card">
                <i class="fa-solid fa-calendar-plus"></i> 
                <strong>Election Day Setup!</strong><br>
                <a href="${data.calendar_link}" target="_blank">Add to Google Calendar ➔</a>
            </div>`;
        } catch(e) { console.error(e); }
    }
    return '';
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    appendMessage(text, 'user-message');
    updateTimeline(text);
    userInput.value = '';
    userInput.disabled = true;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId, message: text })
        });
        const data = await response.json();
        
        // Handle trigger plugins downstream
        let integrationHtml = await handleAction(data.triggered_action, data.action_data);
        
        appendMessage(data.reply, 'bot-message', integrationHtml);
        updateTimeline(data.reply);
        
        if (synthesisEnabled) speakText(data.reply);
        
    } catch (e) {
        appendMessage("Sorry, the Cloud API is currently unreachable. Make sure the server is running.", 'system-message');
    } finally {
        userInput.disabled = false;
        userInput.focus();
    }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// Timeline Progress Logic
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
        userInput.placeholder = "Listening...";
    };
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        userInput.value = transcript;
        sendMessage();
    };
    
    recognition.onend = () => {
        recordBtn.classList.remove('recording');
        userInput.placeholder = "E.g., How do I register to vote?";
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
    const plainText = text.replace(/<[^>]*>?/gm, ''); // strip HTML
    const utterThis = new SpeechSynthesisUtterance(plainText);
    utterThis.pitch = 1;
    utterThis.rate = 1.05;
    window.speechSynthesis.speak(utterThis);
}

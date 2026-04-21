# Advanced SmartVote Navigator AI (Web App Edition)

### 1. Project Name
**SmartVote Navigator AI** (Powered by Gemini & FastAPI)

### 2. Problem Statement
The election process can be overwhelming. This project solves that by providing an incredibly intuitive, context-aware web application that breaks down the election process step-by-step. 

### 3. Solution Approach
Moving away from a basic CLI, SmartVote Navigator AI is now an advanced full-stack application. It uses a **FastAPI** WebSocket server to stream real-time responses from a strictly-constrained neutral **Google Gemini AI** instance, presented via a beautiful, responsive **Vanilla Glassmorphism UI**.

### 4. Features
*   **Stunning Glassmorphism UI:** Premium animated interface ensuring high user engagement.
*   **Voice Integration:** Real-time Speech-to-Text and Text-to-Speech using the browser's native Web Speech API.
*   **Visual Progress Tracking:** A dynamic timeline sidebar that updates visually as you progress through your voting "journey".
*   **Multilingual Support & Advanced Intent:** Powered by Gemini, the AI can naturally converse in any language and understands complex semantic nuances while strictly prohibiting political bias.
*   **Secure BYOK (Bring Your Own Key):** Users configure their Gemini API key directly in their browser's local storage via a secure Settings Modal.

### 5. Tech Stack
*   **Backend:** Python, FastAPI, Uvicorn, Google GenAI SDK.
*   **Frontend:** Vanilla JS, HTML, CSS (Zero bloated libraries).

### 6. Installation & Running

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Run the FastAPI Server:
```bash
python -m uvicorn backend.main:app --reload
```

3. Open your browser and navigate to `http://localhost:8000`. You will be prompted to enter your Gemini API key to begin.

### 7. Assumptions & Future Improvements
*   **Assumptions:** The user has a modern browser capable of utilizing the Web Speech API and WebSocket connections.
*   **Future Improvements:** Persist user journeys across sessions using a database, and implement direct OAuth integration.

"""
main.py

FastAPI backend for SmartVote Navigator AI.
Provides WebSocket endpoints for real-time text and speech processing,
and serves the static HTML/CSS/JS files.
"""

import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.gemini_agent import get_gemini_client, get_chat_session

app = FastAPI(title="SmartVote Navigator AI API")

# Serve static files for the frontend
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
async def root():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Wait for the client to send the API Key in the first message to initialize
    init_data = await websocket.receive_json()
    api_key = init_data.get("api_key")
    
    if not api_key:
        await websocket.send_json({"error": "No API Key provided. Please set it in the UI."})
        await websocket.close()
        return

    try:
        client = get_gemini_client(api_key)
        chat = get_chat_session(client)
        await websocket.send_json({"message": "✅ Secure Connection Established. How can I guide you through the election process today?", "type": "system"})
        
        while True:
            user_msg = await websocket.receive_text()
            
            # Send context to Gemini
            response = chat.send_message(user_msg)
            
            # Reply to user
            await websocket.send_json({
                "message": response.text,
                "type": "bot"
            })
            
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        error_msg = str(e)
        if "API key not valid" in error_msg or "400" in error_msg or "403" in error_msg:
             await websocket.send_json({"error": "Invalid API Key or Quota Exceeded. Please update your API Key."})
        else:
             await websocket.send_json({"error": f"An error occurred: {error_msg}"})
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

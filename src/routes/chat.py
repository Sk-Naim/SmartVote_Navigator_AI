"""
Chat routing endpoints.
"""
from fastapi import APIRouter
from src.models.schemas import ChatRequest, ChatResponse
from src.logic.decision_engine import decision_engine
from src.services.firebase import firebase_service

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Process the user query synchronously to save resources,
    but utilizing async firebase handlers to optimize I/O.
    """
    # 1. Logic Processing
    response = decision_engine.process_query(request.session_id, request.message)

    # 2. Asynchronously save to Firebase (Mock or Real)
    await firebase_service.save_session_log(
        session_id=request.session_id,
        data={
            "query": request.message,
            "reply": response.reply,
            "action": response.triggered_action,
        },
    )

    return response

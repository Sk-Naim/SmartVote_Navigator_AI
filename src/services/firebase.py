"""
Firebase service wrapper.
"""
import firebase_admin
from firebase_admin import credentials, firestore
from src.utils.config import settings
from typing import Dict, Any
from datetime import datetime


class FirebaseService:
    """
    Service for interacting with Firebase Firestore.
    """
    def __init__(self):
        self.mock = settings.MOCK_FIREBASE
        self.db = None
        self.mock_store = {}

        if not self.mock:
            try:
                if not firebase_admin._apps:
                    if settings.FIREBASE_CREDENTIALS_PATH:
                        cred = credentials.Certificate(
                            settings.FIREBASE_CREDENTIALS_PATH
                        )
                        firebase_admin.initialize_app(cred)
                    else:
                        # Use application default credentials
                        firebase_admin.initialize_app()
                self.db = firestore.client()
            except Exception as e:
                print(f"Failed to initialize real Firebase, falling back to mock: {e}")
                self.mock = True

    async def save_session_log(self, session_id: str, data: Dict[str, Any]):
        """Saves a conversation log to Firestore or mock store."""
        data["timestamp"] = datetime.utcnow().isoformat()
        if self.mock:
            if session_id not in self.mock_store:
                self.mock_store[session_id] = []
            self.mock_store[session_id].append(data)
        else:
            self.db.collection("sessions").document(session_id).collection("logs").add(
                data
            )

    async def get_session_history(self, session_id: str) -> list:
        """Retrieves session history from Firestore or mock store."""
        if self.mock:
            return self.mock_store.get(session_id, [])
        else:
            docs = (
                self.db.collection("sessions")
                .document(session_id)
                .collection("logs")
                .order_by("timestamp")
                .stream()
            )
            return [doc.to_dict() for doc in docs]


firebase_service = FirebaseService()

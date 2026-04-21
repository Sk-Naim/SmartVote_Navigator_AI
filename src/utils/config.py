import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "SmartVote Navigator AI Cloud API"
    FIREBASE_CREDENTIALS_PATH: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "")
    MOCK_FIREBASE: bool = os.getenv("MOCK_FIREBASE", "True").lower() == "true"

settings = Settings()

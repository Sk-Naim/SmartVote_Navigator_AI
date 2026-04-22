"""
Configuration settings module.
"""
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Application configuration settings.
    """
    PROJECT_NAME: str = "SmartVote Navigator AI Cloud API"
    FIREBASE_CREDENTIALS_PATH: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "")
    MOCK_FIREBASE: bool = os.getenv("MOCK_FIREBASE", "True").lower() == "true"


settings = Settings()

import os
import logging
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "AIIMS Mentor Chatbot")
DEBUG = os.getenv("DEBUG", "False") == "True"
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:maryam123@localhost:5432/aiims_db"
)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
logger = logging.getLogger("config")

if not GEMINI_API_KEY:
    logger.warning(
        "GEMINI_API_KEY is not set. Every AI request will fail until this is configured."
    )
# Note: Google migrated Gemini API keys from the old "AIza..." (Standard)
# format to the new "AQ...." (Auth key) format during 2026. Both formats
# are valid — do NOT reject/warn based on prefix. The google-genai SDK
# (used below in ai_engine.py) handles Auth keys correctly; the older,
# deprecated google-generativeai SDK does not.

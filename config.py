import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "development-secret-key")
    DATABASE_PATH = BASE_DIR / "instance" / "govassist.db"
    KNOWLEDGE_BASE_PATH = BASE_DIR / "data" / "knowledge_base.json"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")

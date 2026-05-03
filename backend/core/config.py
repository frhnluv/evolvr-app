# core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Adaptive Backend"
    SUPABASE_URL: str
    SUPABASE_KEY: str
    GEMINI_API_KEY: str
    
    # Add other keys later (e.g., SMTP for alerts, Clever Webhook Secret)
    # SMTP_SERVER: str = ""
    # CLEVER_SECRET: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path

# Always resolve to project root .env regardless of where uvicorn is run from
ENV_PATH = Path(__file__).resolve().parents[3] / ".env"

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=str(ENV_PATH), extra="ignore")

    MONGO_URI: str = "mongodb://localhost:27017/momentum_ai"
    SECRET_KEY: str = "your_secret_key_here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    OPENAI_API_KEY: str = ""
    GOOGLE_CALENDAR_API_KEY: str = ""

    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASS: str = ""

    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_FROM_NUMBER: str = ""

    GITHUB_TOKEN: str = ""

settings = Settings()
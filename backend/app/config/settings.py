from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017/momentum_ai"
    SECRET_KEY: str = "your_secret_key_here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    OPENAI_API_KEY: str = ""
    GOOGLE_CALENDAR_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()

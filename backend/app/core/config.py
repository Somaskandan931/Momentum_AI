"""
Centralized configuration and environment variable loader.
Resolves .env from the project root (Momentum_AI/.env) regardless
of where uvicorn is launched from.

Project layout assumed:
  Momentum_AI/
  ├── .env                          ← your secrets go here
  └── backend/
      └── app/
          └── core/
              └── config.py         ← this file
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# backend/ is 2 levels above this file:
#   config.py → core/ → app/ → backend/
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_ENV_PATH = _PROJECT_ROOT / ".env"

load_dotenv(_ENV_PATH)

# ── Groq ──────────────────────────────────────────────────────────────────────
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    raise ValueError(
        f"GROQ_API_KEY not found.\n"
        f"Looked for .env at: {_ENV_PATH}\n"
        f"Add GROQ_API_KEY=gsk_... to that file and restart the server."
    )

# ── MongoDB ───────────────────────────────────────────────────────────────────
MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "momentum_ai")

# ── Auth ──────────────────────────────────────────────────────────────────────
SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
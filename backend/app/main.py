"""
Entry point for Momentum AI backend.
config must be imported first — it loads .env before any service initialises.
"""

# ── Load environment variables BEFORE any other app import ───────────────────
from backend.app.core import config  # noqa: F401  (side-effect: loads .env)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.database.mongodb import connect_db, disconnect_db
from backend.app.routes import (
    idea_routes,
    project_routes,
    task_routes,
    schedule_routes,
    collaboration_routes,
    voice_routes,
)
from backend.app.auth.auth_routes import router as auth_router
from backend.app.database.db_init import init_collections


app = FastAPI(
    title="Momentum AI API",
    description="AI-powered idea execution platform",
    version="1.0.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Lifecycle ─────────────────────────────────────────────────────────────────
async def on_startup():
    await connect_db()
    await init_collections()

app.add_event_handler("startup", on_startup)
app.add_event_handler("shutdown", disconnect_db)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_router,                 prefix="/api/auth",      tags=["Auth"])
app.include_router(idea_routes.router,          prefix="/api/ideas",     tags=["Ideas"])
app.include_router(project_routes.router,       prefix="/api/projects",  tags=["Projects"])
app.include_router(task_routes.router,          prefix="/api/tasks",     tags=["Tasks"])
app.include_router(schedule_routes.router,      prefix="/api/schedules", tags=["Schedules"])
app.include_router(collaboration_routes.router, prefix="/api/collab",    tags=["Collaboration"])
app.include_router(voice_routes.router,         prefix="/api/voice",     tags=["Voice"])


@app.get("/")
def root():
    return {"message": "Momentum AI API is running"}
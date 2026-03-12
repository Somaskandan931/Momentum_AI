from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.mongodb import connect_db, disconnect_db
from app.routes import idea_routes, project_routes, task_routes, schedule_routes, collaboration_routes
from app.auth.auth_routes import router as auth_router

app = FastAPI(
    title="Momentum AI API",
    description="AI-powered idea execution platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connect_db)
app.add_event_handler("shutdown", disconnect_db)

app.include_router(auth_router,          prefix="/api/auth",          tags=["Auth"])
app.include_router(idea_routes.router,   prefix="/api/ideas",         tags=["Ideas"])
app.include_router(project_routes.router,prefix="/api/projects",      tags=["Projects"])
app.include_router(task_routes.router,   prefix="/api/tasks",         tags=["Tasks"])
app.include_router(schedule_routes.router,prefix="/api/schedules",    tags=["Schedules"])
app.include_router(collaboration_routes.router,prefix="/api/collab",  tags=["Collaboration"])

@app.get("/")
def root():
    return {"message": "Momentum AI API is running"}

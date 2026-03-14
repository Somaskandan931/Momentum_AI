"""
Survival Score Service — computes an "Idea Survival Score" (0–100) for a project.
Tries the trained ML model first; falls back to a heuristic scorer.
"""

from bson import ObjectId

from backend.app.database.mongodb import get_db
from backend.app.auth.jwt_handler import GUEST_USER_ID


# ── Main service function ─────────────────────────────────────────────────────

async def compute_survival_score(project_id: str, user_id: str) -> float:
    """
    Compute and return the Idea Survival Score for a project (0–100).
    Guest users skip productivity log lookup (no user context).
    """
    db = get_db()

    # Fetch tasks for this project
    tasks: list[dict] = []
    async for t in db.tasks.find({"project_id": project_id}):
        tasks.append(t)

    # Fetch productivity logs (skipped for guests)
    logs: list[dict] = []
    if user_id != GUEST_USER_ID:
        async for log in db.productivity_logs.find({"user_id": user_id}):
            logs.append(log)

    # Fetch project document (try plain string first, then ObjectId)
    project = await db.projects.find_one({"_id": project_id})
    if project is None:
        try:
            project = await db.projects.find_one({"_id": ObjectId(project_id)})
        except Exception:
            project = None

    team_size = len(project.get("team_members", [])) + 1 if project else 1

    features = _extract_features(tasks, logs, team_size)

    # Try ML model, fall back to heuristic
    try:
        from ai_engine.survival_score.predictor import predict_score
        score = predict_score(features)
    except Exception:
        score = _heuristic_score(features)

    return round(float(score), 2)


# ── Feature extraction ────────────────────────────────────────────────────────

def _extract_features(tasks: list[dict], logs: list[dict], team_size: int) -> dict:
    total_tasks = len(tasks)
    high_priority = sum(1 for t in tasks if t.get("priority") == "high")
    avg_estimated = (
        sum(t.get("estimated_time", 60) for t in tasks) / total_tasks
        if total_tasks else 60
    )
    total_logs = len(logs)
    avg_delay = (
        sum(log.get("delay_minutes", 0) for log in logs) / total_logs
        if total_logs else 0
    )
    avg_focus = (
        sum(log.get("focus_score", 0.5) for log in logs) / total_logs
        if total_logs else 0.5
    )

    return {
        "total_tasks":         total_tasks,
        "high_priority_ratio": high_priority / max(total_tasks, 1),
        "avg_estimated_time":  avg_estimated,
        "team_size":           team_size,
        "avg_delay":           avg_delay,
        "avg_focus_score":     avg_focus,
        "has_history":         total_logs > 0,
    }


# ── Heuristic fallback ────────────────────────────────────────────────────────

def _heuristic_score(features: dict) -> float:
    score = 50.0
    if features["team_size"] > 1:
        score += 10
    if features["avg_focus_score"] > 0.7:
        score += 15
    if features["avg_delay"] < 10:
        score += 10
    if features["total_tasks"] <= 10:
        score += 5
    if features["high_priority_ratio"] < 0.5:
        score += 10
    return min(score, 100.0)
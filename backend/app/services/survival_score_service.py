from app.database.mongodb import get_db
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))

async def compute_survival_score(project_id: str, user_id: str) -> float:
    """
    Compute Idea Survival Score (0-100) using the trained ML model.
    Falls back to heuristic if model is not available.
    """
    db = get_db()

    # Gather features
    tasks = []
    async for t in db.tasks.find({"project_id": project_id}):
        tasks.append(t)

    logs = []
    async for l in db.productivity_logs.find({"user_id": user_id}):
        logs.append(l)

    project = await db.projects.find_one({"_id": project_id})
    team_size = len(project.get("team_members", [])) + 1 if project else 1

    features = _extract_features(tasks, logs, team_size)

    try:
        from ai_engine.survival_score.predictor import predict_score
        score = predict_score(features)
    except Exception:
        score = _heuristic_score(features)

    return round(score, 2)

def _extract_features(tasks: list, logs: list, team_size: int) -> dict:
    total_tasks = len(tasks)
    high_priority = sum(1 for t in tasks if t.get("priority") == "high")
    avg_estimated = sum(t.get("estimated_time", 60) for t in tasks) / max(total_tasks, 1)
    avg_delay = sum(l.get("delay_minutes", 0) for l in logs) / max(len(logs), 1)
    avg_focus = sum(l.get("focus_score", 0.5) for l in logs) / max(len(logs), 1)

    return {
        "total_tasks": total_tasks,
        "high_priority_ratio": high_priority / max(total_tasks, 1),
        "avg_estimated_time": avg_estimated,
        "team_size": team_size,
        "avg_delay": avg_delay,
        "avg_focus_score": avg_focus,
        "has_history": len(logs) > 0
    }

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

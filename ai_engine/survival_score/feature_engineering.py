"""
Feature engineering for the Idea Survival Score predictor.
"""
import pandas as pd
import numpy as np


FEATURE_COLUMNS = [
    "total_tasks",
    "high_priority_ratio",
    "medium_priority_ratio",
    "avg_estimated_time",
    "team_size",
    "avg_delay",
    "avg_focus_score",
    "completion_rate",
    "has_history"
]


def extract_features(tasks: list, logs: list, team_size: int) -> dict:
    """
    Extract numeric features from raw MongoDB documents.

    Args:
        tasks:     List of task dicts from db.tasks
        logs:      List of productivity_log dicts from db.productivity_logs
        team_size: Number of team members (including creator)

    Returns:
        Dict of features ready for model inference
    """
    total = len(tasks)
    if total == 0:
        return {col: 0.0 for col in FEATURE_COLUMNS}

    high = sum(1 for t in tasks if t.get("priority") == "high")
    medium = sum(1 for t in tasks if t.get("priority") == "medium")
    completed = sum(1 for t in tasks if t.get("status") == "Completed")

    avg_est = np.mean([t.get("estimated_time", 60) for t in tasks])
    avg_delay = np.mean([l.get("delay_minutes", 0) for l in logs]) if logs else 0.0
    avg_focus = np.mean([l.get("focus_score", 0.5) for l in logs]) if logs else 0.5

    return {
        "total_tasks": float(total),
        "high_priority_ratio": high / total,
        "medium_priority_ratio": medium / total,
        "avg_estimated_time": float(avg_est),
        "team_size": float(team_size),
        "avg_delay": float(avg_delay),
        "avg_focus_score": float(avg_focus),
        "completion_rate": completed / total,
        "has_history": float(len(logs) > 0)
    }


def features_to_dataframe(features: dict) -> pd.DataFrame:
    return pd.DataFrame([features])[FEATURE_COLUMNS]


def generate_synthetic_training_data(n_samples: int = 2000) -> pd.DataFrame:
    """
    Generate synthetic training data for the survival score model.
    Used when real user data is not yet available.
    Run this on Google Colab to produce training_data/survival_training.csv
    """
    np.random.seed(42)
    rows = []

    for _ in range(n_samples):
        total_tasks = np.random.randint(3, 20)
        high_ratio = np.random.uniform(0, 1)
        med_ratio = np.random.uniform(0, 1 - high_ratio)
        avg_time = np.random.uniform(30, 300)
        team_size = np.random.randint(1, 6)
        avg_delay = np.random.uniform(0, 60)
        avg_focus = np.random.uniform(0.2, 1.0)
        completion_rate = np.random.uniform(0, 1)
        has_history = np.random.randint(0, 2)

        # Heuristic label
        score = 50
        score += (avg_focus - 0.5) * 40
        score -= avg_delay * 0.3
        score += (team_size - 1) * 5
        score += completion_rate * 20
        score -= high_ratio * 10
        score = float(np.clip(score, 0, 100))

        rows.append({
            "total_tasks": total_tasks,
            "high_priority_ratio": round(high_ratio, 3),
            "medium_priority_ratio": round(med_ratio, 3),
            "avg_estimated_time": round(avg_time, 1),
            "team_size": team_size,
            "avg_delay": round(avg_delay, 2),
            "avg_focus_score": round(avg_focus, 3),
            "completion_rate": round(completion_rate, 3),
            "has_history": has_history,
            "survival_score": round(score, 2)
        })

    return pd.DataFrame(rows)

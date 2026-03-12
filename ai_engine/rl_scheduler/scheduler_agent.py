"""
Scheduler agent — inference module.
Loads the trained PPO model and produces a schedule for a list of tasks.
"""
import os
import numpy as np
from datetime import datetime, timedelta

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../models/momentum_rl_scheduler_final")


def schedule_with_agent(tasks: list) -> list[dict]:
    """
    Use the trained RL agent to schedule a list of tasks.

    Args:
        tasks: List of task dicts from MongoDB (must have estimated_time, priority)

    Returns:
        List of schedule slot dicts with task_id, start_time, end_time
    """
    from stable_baselines3 import PPO
    try:
        from ai_engine.rl_scheduler.environment import SchedulingEnv
    except ImportError:
        from environment import SchedulingEnv

    if not os.path.exists(MODEL_PATH + ".zip"):
        raise FileNotFoundError(f"Trained model not found at {MODEL_PATH}.zip. Please train first.")

    model = PPO.load(MODEL_PATH)
    env = SchedulingEnv(tasks=[_normalize_task(t) for t in tasks])

    obs, _ = env.reset()
    done = False
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, _, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

    return _convert_slots(env.scheduled)


def _normalize_task(task: dict) -> dict:
    """Convert MongoDB task document to env-compatible format."""
    priority_map = {"high": "high", "medium": "medium", "low": "low"}
    return {
        "id": str(task.get("_id", task.get("id", "unknown"))),
        "title": task.get("title", "Untitled"),
        "priority": priority_map.get(task.get("priority", "medium"), "medium"),
        "estimated_time": task.get("estimated_time", 60),
        "deadline_hour": 17.0
    }


def _convert_slots(scheduled: list) -> list[dict]:
    """Convert env scheduled list to ScheduleSlot-compatible dicts."""
    base_date = datetime.utcnow().replace(hour=9, minute=0, second=0, microsecond=0)
    slots = []
    for item in scheduled:
        start = base_date + timedelta(hours=item["start"] - 9)
        end = base_date + timedelta(hours=item["end"] - 9)
        slots.append({
            "task_id": item["id"],
            "start_time": start,
            "end_time": end
        })
    return slots

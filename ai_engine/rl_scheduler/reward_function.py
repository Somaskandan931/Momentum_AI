"""
Reward function definitions for the Momentum AI RL scheduler.
Separated here for easy tuning without modifying the environment.
"""

def compute_reward(
    task: dict,
    action: int,
    current_hour: float,
    scheduled_count: int,
    max_tasks: int
) -> float:
    """
    Compute reward signal for a given scheduling action.

    Args:
        task:            The task being acted on
        action:          0=assign, 1=delay, 2=prioritize, 3=reallocate
        current_hour:    Current simulated time (e.g. 9.5 = 9:30 AM)
        scheduled_count: How many tasks already scheduled
        max_tasks:       Total tasks in session

    Returns:
        Float reward value
    """
    priority_bonus = {"high": 0.5, "medium": 0.2, "low": 0.0}

    if action == 0:  # Assign task
        reward = 1.0 + priority_bonus.get(task.get("priority", "medium"), 0.2)
        duration_hours = task.get("estimated_time", 60) / 60.0
        end_hour = current_hour + duration_hours

        # Penalize deadline miss
        deadline = task.get("deadline_hour", 18.0)
        if end_hour > deadline:
            reward -= 1.0

        # Penalize late-day scheduling
        if current_hour > 16:
            reward -= 0.4

        # Bonus for balanced workload
        balance_ratio = scheduled_count / max(max_tasks, 1)
        if 0.3 <= balance_ratio <= 0.7:
            reward += 0.3

        return reward

    elif action == 1:  # Delay
        return -0.3  # Penalty for avoidable delay

    elif action == 2:  # Prioritize
        return 0.1  # Small reward for reordering

    elif action == 3:  # Reallocate
        return 0.05  # Minimal reward, used for team scenarios

    return 0.0

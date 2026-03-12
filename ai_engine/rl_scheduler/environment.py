"""
Custom Gymnasium environment for task scheduling.
The RL agent learns to assign tasks to time slots optimally.

Designed to be trained on Google Colab using stable-baselines3.
"""
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from datetime import datetime, timedelta


class SchedulingEnv(gym.Env):
    """
    Custom scheduling environment.

    Observation space:
        - current_hour:          float  (0-23)
        - remaining_tasks:       float  (0-20 normalized)
        - avg_priority:          float  (0-1, high=1)
        - avg_estimated_time:    float  (normalized 0-1)
        - workload_balance:      float  (0-1)
        - deadline_pressure:     float  (0-1, 1=urgent)

    Action space:
        0 - assign task to current slot
        1 - delay task by 1 hour
        2 - prioritize task (move to front)
        3 - reallocate task to another user (team scenario)
    """

    metadata = {"render_modes": ["human"]}

    def __init__(self, tasks: list = None, max_tasks: int = 10):
        super().__init__()
        self.max_tasks = max_tasks
        self.tasks = tasks or self._generate_dummy_tasks(max_tasks)

        self.observation_space = spaces.Box(
            low=np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32),
            high=np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0], dtype=np.float32),
            dtype=np.float32
        )
        self.action_space = spaces.Discrete(4)

        self.current_hour = 9.0
        self.scheduled = []
        self.remaining = list(self.tasks)
        self.total_reward = 0.0
        self.step_count = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.tasks = self._generate_dummy_tasks(self.max_tasks)
        self.remaining = list(self.tasks)
        self.scheduled = []
        self.current_hour = 9.0
        self.total_reward = 0.0
        self.step_count = 0
        return self._get_obs(), {}

    def step(self, action):
        if not self.remaining:
            return self._get_obs(), 0.0, True, False, {}

        task = self.remaining[0]
        reward = 0.0
        terminated = False

        if action == 0:  # assign
            reward = self._assign_task(task)
            self.remaining.pop(0)
        elif action == 1:  # delay
            reward = -0.3
            self.current_hour = min(self.current_hour + 1, 18)
        elif action == 2:  # prioritize
            if len(self.remaining) > 1:
                high_idx = self._find_highest_priority()
                self.remaining.insert(0, self.remaining.pop(high_idx))
            reward = 0.1
        elif action == 3:  # reallocate
            reward = 0.05
            self.remaining.pop(0)

        self.total_reward += reward
        self.step_count += 1

        if not self.remaining or self.current_hour >= 18:
            terminated = True

        return self._get_obs(), reward, terminated, False, {}

    def _assign_task(self, task: dict) -> float:
        duration_hours = task["estimated_time"] / 60.0
        end_hour = self.current_hour + duration_hours

        reward = 1.0  # base reward for completing a task

        # Bonus for high priority tasks
        if task["priority"] == "high":
            reward += 0.5

        # Penalty for deadline miss
        if end_hour > task.get("deadline_hour", 18):
            reward -= 1.0

        # Penalty for overloading
        if self.current_hour > 17:
            reward -= 0.7

        self.scheduled.append({**task, "start": self.current_hour, "end": end_hour})
        self.current_hour = end_hour + 0.25  # 15 min buffer
        return reward

    def _find_highest_priority(self) -> int:
        priority_map = {"high": 2, "medium": 1, "low": 0}
        return max(
            range(len(self.remaining)),
            key=lambda i: priority_map.get(self.remaining[i]["priority"], 1)
        )

    def _get_obs(self) -> np.ndarray:
        if not self.remaining:
            return np.zeros(6, dtype=np.float32)

        priority_map = {"high": 1.0, "medium": 0.5, "low": 0.0}
        avg_priority = np.mean([priority_map.get(t["priority"], 0.5) for t in self.remaining])
        avg_time = np.mean([t["estimated_time"] for t in self.remaining]) / 480.0  # normalize by 8h
        deadline_pressure = min(1.0, len([t for t in self.remaining if t.get("deadline_hour", 18) < self.current_hour + 2]) / max(len(self.remaining), 1))
        workload = len(self.scheduled) / max(self.max_tasks, 1)

        return np.array([
            self.current_hour / 24.0,
            len(self.remaining) / self.max_tasks,
            avg_priority,
            avg_time,
            workload,
            deadline_pressure
        ], dtype=np.float32)

    def _generate_dummy_tasks(self, n: int) -> list:
        priorities = ["high", "medium", "low"]
        tasks = []
        for i in range(n):
            tasks.append({
                "id": f"task_{i}",
                "title": f"Task {i}",
                "priority": priorities[i % 3],
                "estimated_time": np.random.randint(30, 180),
                "deadline_hour": np.random.uniform(14, 18)
            })
        return tasks

    def render(self):
        print(f"Hour: {self.current_hour:.1f} | Remaining: {len(self.remaining)} | Scheduled: {len(self.scheduled)}")

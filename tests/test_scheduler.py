"""
Tests for the RL scheduling environment and reward function.
Run: pytest tests/test_scheduler.py -v
"""
import pytest
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ai_engine.rl_scheduler.environment import SchedulingEnv
from ai_engine.rl_scheduler.reward_function import compute_reward


class TestSchedulingEnvironment:

    def test_env_reset(self):
        env = SchedulingEnv(max_tasks=5)
        obs, info = env.reset()
        assert obs.shape == (6,)
        assert all(0.0 <= v <= 1.0 for v in obs)

    def test_observation_space(self):
        env = SchedulingEnv(max_tasks=5)
        obs, _ = env.reset()
        assert env.observation_space.contains(obs)

    def test_action_space(self):
        env = SchedulingEnv(max_tasks=5)
        assert env.action_space.n == 4

    def test_step_assign(self):
        env = SchedulingEnv(max_tasks=5)
        obs, _ = env.reset()
        obs, reward, terminated, truncated, info = env.step(0)  # assign
        assert isinstance(reward, float)
        assert obs.shape == (6,)

    def test_episode_terminates(self):
        env = SchedulingEnv(max_tasks=3)
        obs, _ = env.reset()
        done = False
        steps = 0
        while not done and steps < 100:
            action = env.action_space.sample()
            obs, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            steps += 1
        assert done

    def test_tasks_scheduled_after_full_episode(self):
        env = SchedulingEnv(max_tasks=5)
        env.reset()
        for _ in range(20):
            obs, _, terminated, _, _ = env.step(0)
            if terminated:
                break
        assert len(env.scheduled) > 0


class TestRewardFunction:

    def test_assign_high_priority(self):
        task = {"priority": "high", "estimated_time": 60, "deadline_hour": 17.0}
        reward = compute_reward(task, action=0, current_hour=10.0, scheduled_count=2, max_tasks=8)
        assert reward > 1.0

    def test_assign_past_deadline(self):
        task = {"priority": "medium", "estimated_time": 120, "deadline_hour": 11.0}
        reward = compute_reward(task, action=0, current_hour=10.5, scheduled_count=0, max_tasks=5)
        assert reward < 1.0

    def test_delay_penalty(self):
        task = {"priority": "low", "estimated_time": 30, "deadline_hour": 17.0}
        reward = compute_reward(task, action=1, current_hour=9.0, scheduled_count=0, max_tasks=5)
        assert reward < 0

    def test_prioritize_small_reward(self):
        task = {"priority": "high", "estimated_time": 60, "deadline_hour": 17.0}
        reward = compute_reward(task, action=2, current_hour=9.0, scheduled_count=0, max_tasks=5)
        assert reward > 0

    def test_balanced_workload_bonus(self):
        task = {"priority": "medium", "estimated_time": 60, "deadline_hour": 17.0}
        reward_balanced = compute_reward(task, action=0, current_hour=10.0, scheduled_count=4, max_tasks=8)
        reward_empty = compute_reward(task, action=0, current_hour=10.0, scheduled_count=0, max_tasks=8)
        assert reward_balanced >= reward_empty

"""
Tests for AI engine modules: feature engineering, command parser, survival score heuristic.
Run: pytest tests/test_ai_models.py -v
"""
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ai_engine.survival_score.feature_engineering import extract_features, generate_synthetic_training_data, FEATURE_COLUMNS
from voice_interface.command_parser import parse_command


class TestFeatureEngineering:

    def _make_tasks(self, n=5):
        priorities = ["high", "medium", "low"]
        return [{"priority": priorities[i % 3], "estimated_time": 60 + i * 10, "status": "To Do"} for i in range(n)]

    def _make_logs(self, n=3):
        return [{"delay_minutes": i * 2, "focus_score": 0.7 + i * 0.05} for i in range(n)]

    def test_extract_returns_all_columns(self):
        tasks = self._make_tasks()
        logs = self._make_logs()
        features = extract_features(tasks, logs, team_size=2)
        for col in FEATURE_COLUMNS:
            assert col in features

    def test_empty_tasks(self):
        features = extract_features([], [], team_size=1)
        assert features["total_tasks"] == 0.0

    def test_team_size_reflected(self):
        tasks = self._make_tasks(4)
        features = extract_features(tasks, [], team_size=3)
        assert features["team_size"] == 3.0

    def test_high_priority_ratio(self):
        tasks = [{"priority": "high", "estimated_time": 60, "status": "To Do"}] * 4 + \
                [{"priority": "low", "estimated_time": 60, "status": "To Do"}] * 6
        features = extract_features(tasks, [], team_size=1)
        assert abs(features["high_priority_ratio"] - 0.4) < 0.01

    def test_synthetic_data_shape(self):
        df = generate_synthetic_training_data(100)
        assert len(df) == 100
        assert "survival_score" in df.columns
        for col in FEATURE_COLUMNS:
            assert col in df.columns

    def test_synthetic_scores_in_range(self):
        df = generate_synthetic_training_data(200)
        assert df["survival_score"].min() >= 0
        assert df["survival_score"].max() <= 100


class TestCommandParser:

    def test_add_task_basic(self):
        result = parse_command("add task build login page")
        assert result["action"] == "add_task"
        assert "login" in result["title"]

    def test_add_task_with_deadline(self):
        result = parse_command("add task write tests due tomorrow")
        assert result["action"] == "add_task"
        assert result["deadline"] is not None

    def test_show_schedule(self):
        result = parse_command("show today's schedule")
        assert result["action"] == "show_schedule"

    def test_move_task(self):
        result = parse_command("move design review to evening")
        assert result["action"] == "move_task"
        assert "design review" in result["task"]

    def test_complete_task(self):
        result = parse_command("mark authentication as done")
        assert result["action"] == "complete_task"

    def test_list_tasks(self):
        result = parse_command("show my tasks")
        assert result["action"] == "list_tasks"

    def test_unknown_command(self):
        result = parse_command("what is the weather today")
        assert result["action"] == "unknown"
        assert "raw_text" in result

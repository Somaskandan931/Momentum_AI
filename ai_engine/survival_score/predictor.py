"""
Survival Score predictor — inference module.
Loads trained XGBoost model and returns a 0-100 score.
"""
import os
import joblib
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../models/survival_score_model.pkl")

_model = None

def _load_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Trained model not found at {MODEL_PATH}. "
                "Please run ai_engine/survival_score/train_model.py first."
            )
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_score(features: dict) -> float:
    """
    Predict Idea Survival Score from extracted feature dict.

    Args:
        features: Dict with keys matching FEATURE_COLUMNS

    Returns:
        Float score between 0 and 100
    """
    try:
        from ai_engine.survival_score.feature_engineering import features_to_dataframe
    except ImportError:
        from feature_engineering import features_to_dataframe

    model = _load_model()
    X = features_to_dataframe(features)
    score = model.predict(X)[0]
    return float(np.clip(score, 0, 100))


if __name__ == "__main__":
    # Quick test with dummy features
    test_features = {
        "total_tasks": 8,
        "high_priority_ratio": 0.25,
        "medium_priority_ratio": 0.5,
        "avg_estimated_time": 90.0,
        "team_size": 2,
        "avg_delay": 5.0,
        "avg_focus_score": 0.8,
        "completion_rate": 0.6,
        "has_history": 1.0
    }
    score = predict_score(test_features)
    print(f"Predicted Survival Score: {score:.1f} / 100")

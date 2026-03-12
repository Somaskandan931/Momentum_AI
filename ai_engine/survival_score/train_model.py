"""
================================================================================
  Momentum AI — Survival Score Model Training Script
  Designed for Google Colab
================================================================================

USAGE ON GOOGLE COLAB:

  Step 1 — Install dependencies:
    !pip install scikit-learn xgboost pandas numpy matplotlib joblib

  Step 2 — Mount Drive (optional, to save model):
    from google.colab import drive
    drive.mount('/content/drive')

  Step 3 — Add project to path:
    import sys
    sys.path.insert(0, '/content/drive/MyDrive/momentum-ai')

  Step 4 — Run:
    from ai_engine.survival_score.train_model import train
    train()

  The trained model will be saved to:
    models/survival_score_model.pkl

================================================================================
"""

import os
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor

try:
    from ai_engine.survival_score.feature_engineering import (
        generate_synthetic_training_data, FEATURE_COLUMNS
    )
except ImportError:
    from feature_engineering import generate_synthetic_training_data, FEATURE_COLUMNS

MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), "../../models/survival_score_model.pkl")
DATA_SAVE_PATH = os.path.join(os.path.dirname(__file__), "../../data/training_data/survival_training.csv")


def train(data_path: str = None, save_path: str = None):
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(DATA_SAVE_PATH), exist_ok=True)

    # ── Load or generate data ──────────────────────────────────────────────
    if data_path and os.path.exists(data_path):
        print(f"Loading data from {data_path}")
        df = pd.read_csv(data_path)
    else:
        print("Generating synthetic training data (2000 samples)...")
        df = generate_synthetic_training_data(2000)
        df.to_csv(DATA_SAVE_PATH, index=False)
        print(f"Training data saved to {DATA_SAVE_PATH}")

    print(f"Dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    print(df.describe())

    X = df[FEATURE_COLUMNS]
    y = df["survival_score"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # ── Build pipeline ─────────────────────────────────────────────────────
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("xgb", XGBRegressor(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            verbosity=0
        ))
    ])

    # ── Cross-validation ───────────────────────────────────────────────────
    print("\nRunning 5-fold cross validation...")
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="r2")
    print(f"CV R² scores: {cv_scores}")
    print(f"Mean CV R²:   {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    # ── Train final model ──────────────────────────────────────────────────
    print("\nTraining final model...")
    model.fit(X_train, y_train)

    # ── Evaluate ───────────────────────────────────────────────────────────
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"\nTest MAE:  {mae:.2f}")
    print(f"Test R²:   {r2:.4f}")

    # ── Feature importance plot ────────────────────────────────────────────
    xgb_model = model.named_steps["xgb"]
    importances = xgb_model.feature_importances_
    plt.figure(figsize=(8, 5))
    plt.barh(FEATURE_COLUMNS, importances, color="steelblue")
    plt.xlabel("Importance")
    plt.title("Survival Score — Feature Importance")
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(MODEL_SAVE_PATH), "feature_importance.png"))
    plt.show()
    print("Feature importance plot saved.")

    # ── Save model ─────────────────────────────────────────────────────────
    save_to = save_path or MODEL_SAVE_PATH
    joblib.dump(model, save_to)
    print(f"\nModel saved to: {save_to}")
    return model


if __name__ == "__main__":
    train()

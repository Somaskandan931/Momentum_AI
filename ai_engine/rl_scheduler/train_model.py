"""
================================================================================
  Momentum AI — RL Scheduler Training Script
  Designed for Google Colab (GPU/CPU)
================================================================================

USAGE ON GOOGLE COLAB:
  1. Upload this file and ai_engine/rl_scheduler/environment.py to your Drive
  2. Run the setup cell below, then execute train()

COLAB SETUP CELL:
  !pip install stable-baselines3 gymnasium numpy pandas

COLAB MOUNT (if loading from Drive):
  from google.colab import drive
  drive.mount('/content/drive')
  import sys
  sys.path.insert(0, '/content/drive/MyDrive/momentum-ai')
================================================================================
"""

import os
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import EvalCallback, CheckpointCallback
from stable_baselines3.common.monitor import Monitor

# Import our custom environment
try:
    from ai_engine.rl_scheduler.environment import SchedulingEnv
except ImportError:
    from environment import SchedulingEnv  # when run directly from Colab


# ── Configuration ──────────────────────────────────────────────────────────────
CONFIG = {
    "total_timesteps": 200_000,     # increase to 500k+ for better results on Colab
    "n_envs": 4,                    # parallel environments
    "learning_rate": 3e-4,
    "n_steps": 2048,
    "batch_size": 64,
    "n_epochs": 10,
    "gamma": 0.99,
    "gae_lambda": 0.95,
    "clip_range": 0.2,
    "ent_coef": 0.01,               # entropy bonus encourages exploration
    "save_path": "./models",
    "log_path": "./logs",
    "model_name": "momentum_rl_scheduler",
    "eval_freq": 10_000,
    "checkpoint_freq": 50_000,
}


def make_env():
    return Monitor(SchedulingEnv(max_tasks=10))


def train():
    os.makedirs(CONFIG["save_path"], exist_ok=True)
    os.makedirs(CONFIG["log_path"], exist_ok=True)

    print("Creating vectorized environments...")
    env = make_vec_env(make_env, n_envs=CONFIG["n_envs"])
    eval_env = make_vec_env(make_env, n_envs=1)

    print("Initializing PPO model...")
    model = PPO(
        policy="MlpPolicy",
        env=env,
        learning_rate=CONFIG["learning_rate"],
        n_steps=CONFIG["n_steps"],
        batch_size=CONFIG["batch_size"],
        n_epochs=CONFIG["n_epochs"],
        gamma=CONFIG["gamma"],
        gae_lambda=CONFIG["gae_lambda"],
        clip_range=CONFIG["clip_range"],
        ent_coef=CONFIG["ent_coef"],
        verbose=1,
        tensorboard_log=CONFIG["log_path"]
    )

    callbacks = [
        EvalCallback(
            eval_env,
            best_model_save_path=CONFIG["save_path"],
            log_path=CONFIG["log_path"],
            eval_freq=CONFIG["eval_freq"],
            deterministic=True,
            render=False,
            verbose=1
        ),
        CheckpointCallback(
            save_freq=CONFIG["checkpoint_freq"],
            save_path=CONFIG["save_path"],
            name_prefix=CONFIG["model_name"]
        )
    ]

    print(f"Training for {CONFIG['total_timesteps']:,} timesteps...")
    model.learn(
        total_timesteps=CONFIG["total_timesteps"],
        callback=callbacks,
        progress_bar=True
    )

    final_path = os.path.join(CONFIG["save_path"], CONFIG["model_name"] + "_final")
    model.save(final_path)
    print(f"Model saved to: {final_path}.zip")
    return model


def evaluate(model_path: str = None, n_episodes: int = 10):
    """Evaluate a saved model and print average reward."""
    if model_path is None:
        model_path = os.path.join(CONFIG["save_path"], CONFIG["model_name"] + "_final")

    model = PPO.load(model_path)
    env = SchedulingEnv(max_tasks=10)

    rewards = []
    for ep in range(n_episodes):
        obs, _ = env.reset()
        total_reward = 0
        done = False
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(action)
            total_reward += reward
            done = terminated or truncated
        rewards.append(total_reward)
        print(f"Episode {ep+1}: reward = {total_reward:.2f}")

    print(f"\nMean reward over {n_episodes} episodes: {np.mean(rewards):.2f} ± {np.std(rewards):.2f}")
    return rewards


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["train", "eval"], default="train")
    parser.add_argument("--model", type=str, default=None)
    args = parser.parse_args()

    if args.mode == "train":
        train()
    else:
        evaluate(args.model)

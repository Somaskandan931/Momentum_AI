"""
Idea Service — generates an AI-powered project roadmap via Groq.
Uses the centralised config module so the API key is always resolved
from Momentum_AI/.env regardless of the working directory.
"""

import json
from groq import Groq

from backend.app.core.config import GROQ_API_KEY

# Initialise Groq client once at module load (key is already validated in config)
_client = Groq(api_key=GROQ_API_KEY)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _clean_json(content: str):
    """
    Strip markdown fences and safely parse JSON returned by the LLM.
    Handles both ```json ... ``` and raw JSON responses.
    """
    content = content.strip()

    # Remove opening fence line (e.g. ```json or ```)
    if content.startswith("```"):
        lines = content.splitlines()
        # Drop first line (fence open) and last line if it's a closing fence
        inner = lines[1:]
        if inner and inner[-1].strip() == "```":
            inner = inner[:-1]
        content = "\n".join(inner).strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON returned from AI:\n{content}") from exc


# ── Main service function ─────────────────────────────────────────────────────

async def generate_roadmap(idea: str) -> list[dict]:
    """
    Send a project idea to Groq and return a structured task roadmap.

    Returns a list of dicts, each containing:
        day, title, description, priority, estimated_time
    """

    prompt = f"""
You are an expert product manager and startup mentor.

A user submitted this project idea:

"{idea}"

Break this into a **practical execution roadmap**.

Rules:
- 5 to 7 tasks total
- Each task represents one day
- Tasks must be realistic for a solo developer

Return ONLY valid JSON in this format:

[
  {{
    "day": 1,
    "title": "Task title",
    "description": "Short explanation of the task",
    "priority": "high | medium | low",
    "estimated_time": 120
  }}
]

No markdown. No explanations. Only JSON.
"""

    try:
        response = _client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You return strictly valid JSON only. No markdown, no prose."},
                {"role": "user",   "content": prompt},
            ],
            temperature=0.4,
        )

        content = response.choices[0].message.content
        roadmap = _clean_json(content)

        if not isinstance(roadmap, list):
            raise ValueError("AI response was not a JSON array")

        return roadmap

    except Exception as e:
        raise RuntimeError(f"Roadmap generation failed: {e}") from e
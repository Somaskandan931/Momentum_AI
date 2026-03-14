"""
Trend Service — analyses market competition for a project idea via Groq.
Uses the centralised config module so the API key is always resolved
from Momentum_AI/.env regardless of the working directory.
"""

import json
from groq import Groq

from backend.app.core.config import GROQ_API_KEY

_client = Groq(api_key=GROQ_API_KEY)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _clean_json(content: str) -> dict:
    """Strip markdown fences and parse JSON."""
    content = content.strip()

    if content.startswith("```"):
        lines = content.splitlines()
        inner = lines[1:]
        if inner and inner[-1].strip() == "```":
            inner = inner[:-1]
        content = "\n".join(inner).strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON returned from AI:\n{content}") from exc


# ── Main service function ─────────────────────────────────────────────────────

async def analyze_trend(idea: str) -> dict:
    """
    Analyse market competition and suggest differentiators for a project idea.

    Returns a dict with:
        competition_level, existing_solutions, suggested_improvements, innovation_score
    """

    prompt = f"""
You are a startup idea analyst.

Analyse the following project idea:

"{idea}"

Return ONLY valid JSON with exactly these keys:

{{
  "competition_level": "low | medium | high",
  "existing_solutions": ["tool1", "tool2", "tool3"],
  "suggested_improvements": ["feature1", "feature2", "feature3"],
  "innovation_score": 7
}}

No markdown. No explanations. Only JSON.
"""

    try:
        response = _client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You return strictly valid JSON only. No markdown, no prose."},
                {"role": "user",   "content": prompt},
            ],
            temperature=0.3,
        )

        content = response.choices[0].message.content
        return _clean_json(content)

    except Exception as e:
        raise RuntimeError(f"Trend analysis failed: {e}") from e
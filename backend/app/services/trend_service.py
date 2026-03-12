import openai
from app.config.settings import settings
import json

openai.api_key = settings.OPENAI_API_KEY

async def analyze_trend(idea: str) -> dict:
    """Analyze market competition and suggest differentiators for a project idea."""
    prompt = f"""
You are a startup idea analyst. Analyze the following project idea for market saturation and competition:

"{idea}"

Return ONLY a JSON object with:
- "competition_level": one of "low", "medium", "high"
- "existing_solutions": list of 3 existing similar tools (names only)
- "suggested_improvements": list of 3 specific feature ideas to differentiate
- "innovation_score": integer from 1 to 10

Example:
{{
  "competition_level": "high",
  "existing_solutions": ["Notion", "Trello", "Asana"],
  "suggested_improvements": ["Add AI-generated task breakdown", "Integrate voice commands", "Include burnout prediction"],
  "innovation_score": 6
}}
"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    content = response.choices[0].message.content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    return json.loads(content)

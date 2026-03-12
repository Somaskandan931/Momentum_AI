import httpx
from app.config.settings import settings
import openai

openai.api_key = settings.OPENAI_API_KEY

async def generate_roadmap(idea: str) -> list[dict]:
    """Send idea to LLM and get structured task list back."""
    prompt = f"""
You are a project planning assistant. A user has submitted the following project idea:

"{idea}"

Break this idea into a day-by-day execution roadmap of 5 to 7 tasks.
Return ONLY a JSON array. Each item must have:
- "day": integer
- "title": short task title
- "description": one sentence description
- "priority": one of high, medium, low
- "estimated_time": estimated minutes to complete

Example format:
[
  {{"day": 1, "title": "Research APIs", "description": "Explore available speech-to-text APIs.", "priority": "high", "estimated_time": 120}},
  ...
]
"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    import json
    content = response.choices[0].message.content.strip()
    # Strip markdown code fences if present
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    return json.loads(content)

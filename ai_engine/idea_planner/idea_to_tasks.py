"""
Standalone idea planner module.
Called directly or via the backend idea_service.
"""
import openai
import json
import os

def generate_roadmap(idea: str, api_key: str = None) -> list[dict]:
    """
    Given a project idea string, returns a structured task roadmap.

    Args:
        idea: The project idea text
        api_key: OpenAI API key (reads from env if not provided)

    Returns:
        List of task dicts with day, title, description, priority, estimated_time
    """
    openai.api_key = api_key or os.getenv("OPENAI_API_KEY")

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

Return only the JSON array, no explanation.
"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    content = response.choices[0].message.content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    return json.loads(content)


if __name__ == "__main__":
    import sys
    idea = sys.argv[1] if len(sys.argv) > 1 else "AI Resume Analyzer"
    tasks = generate_roadmap(idea)
    for t in tasks:
        print(f"Day {t['day']}: {t['title']} [{t['priority']}] — {t['estimated_time']} min")

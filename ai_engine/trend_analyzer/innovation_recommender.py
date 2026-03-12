"""
Innovation recommender — suggests differentiators for a project idea.
"""
import openai
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def recommend_innovations(idea: str, competition_level: str = "medium") -> dict:
    """
    Suggest innovation strategies for a project idea.

    Args:
        idea:              The project idea
        competition_level: 'low', 'medium', or 'high'

    Returns:
        Dict with suggested_improvements and differentiation strategies
    """
    prompt = f"""
The project idea "{idea}" has {competition_level} market competition.

Suggest 5 specific, actionable ways to make this project more innovative and unique.
Focus on features, UX improvements, or technical approaches that competitors are missing.

Return ONLY a JSON object:
{{
  "suggested_improvements": [
    "Improvement 1",
    "Improvement 2",
    "Improvement 3",
    "Improvement 4",
    "Improvement 5"
  ],
  "key_differentiator": "One sentence describing the strongest unique angle",
  "recommended_tech": ["tech1", "tech2", "tech3"]
}}

Return only the JSON, no explanation.
"""
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        return json.loads(content)
    except Exception as e:
        return {
            "suggested_improvements": [],
            "key_differentiator": "Unable to generate recommendations.",
            "recommended_tech": [],
            "error": str(e)
        }

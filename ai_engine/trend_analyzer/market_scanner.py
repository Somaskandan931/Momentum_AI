"""
Market scanner — checks for existing solutions using LLM analysis.
"""
import openai
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def scan_market(idea: str) -> dict:
    """
    Scan for existing solutions and market saturation for a project idea.

    Args:
        idea: Project idea string

    Returns:
        Dict with competition_level, existing_solutions, innovation_score
    """
    prompt = f"""
Analyze the following project idea for market competition:

"{idea}"

Return ONLY a JSON object:
{{
  "competition_level": "low" | "medium" | "high",
  "existing_solutions": ["Tool1", "Tool2", "Tool3"],
  "innovation_score": 1-10,
  "market_gap": "one sentence describing the gap this idea could fill"
}}

Return only the JSON, no explanation.
"""
    try:
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
    except Exception as e:
        return {
            "competition_level": "unknown",
            "existing_solutions": [],
            "innovation_score": 5,
            "market_gap": "Unable to analyze at this time.",
            "error": str(e)
        }

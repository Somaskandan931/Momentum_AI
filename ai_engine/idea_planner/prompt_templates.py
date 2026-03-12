ROADMAP_PROMPT = """
You are a project planning assistant. A user has submitted the following project idea:

"{idea}"

Break this idea into a day-by-day execution roadmap of 5 to 7 tasks.
Return ONLY a JSON array. Each item must have:
- "day": integer
- "title": short task title
- "description": one sentence description
- "priority": one of high, medium, low
- "estimated_time": estimated minutes to complete

Return only the JSON array, no explanation, no markdown.
"""

TREND_ANALYSIS_PROMPT = """
You are a startup idea analyst. Analyze the following project idea for market saturation and competition:

"{idea}"

Return ONLY a JSON object with:
- "competition_level": one of "low", "medium", "high"
- "existing_solutions": list of 3 existing similar tools (names only)
- "suggested_improvements": list of 3 specific feature ideas to differentiate
- "innovation_score": integer from 1 to 10

Return only the JSON object, no explanation, no markdown.
"""

SURVIVAL_PROMPT = """
Given the following project metadata, estimate the probability (0-100) that this project will be successfully completed.

Project title: {title}
Total tasks: {total_tasks}
High priority ratio: {high_priority_ratio}
Team size: {team_size}
Average estimated task time (minutes): {avg_estimated_time}
Developer average focus score (0-1): {avg_focus_score}
Average task delay (minutes): {avg_delay}

Return ONLY a single integer between 0 and 100.
"""

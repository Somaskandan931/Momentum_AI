"""
GitHub activity analyzer.
Fetches commit and PR activity to track development progress.
"""
import httpx
import os
from datetime import datetime

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}


async def get_repo_activity(owner: str, repo: str, since_days: int = 7) -> dict:
    """
    Fetch recent repository activity: commits, PRs, issues.

    Args:
        owner:      GitHub username or org
        repo:       Repository name
        since_days: Look back this many days

    Returns:
        Dict with commits, pull_requests, issues counts and summaries
    """
    base = f"https://api.github.com/repos/{owner}/{repo}"
    since = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    async with httpx.AsyncClient(headers=HEADERS) as client:
        commits_r = await client.get(f"{base}/commits", params={"since": since, "per_page": 50})
        prs_r = await client.get(f"{base}/pulls", params={"state": "all", "per_page": 20})
        issues_r = await client.get(f"{base}/issues", params={"state": "all", "per_page": 20})

    commits = commits_r.json() if commits_r.status_code == 200 else []
    prs = prs_r.json() if prs_r.status_code == 200 else []
    issues = issues_r.json() if issues_r.status_code == 200 else []

    return {
        "commit_count": len(commits),
        "recent_commits": [
            {"sha": c["sha"][:7], "message": c["commit"]["message"].split("\n")[0], "author": c["commit"]["author"]["name"]}
            for c in commits[:5]
        ],
        "open_prs": sum(1 for p in prs if p.get("state") == "open"),
        "merged_prs": sum(1 for p in prs if p.get("merged_at")),
        "open_issues": sum(1 for i in issues if i.get("state") == "open"),
        "activity_score": min(100, len(commits) * 5 + len(prs) * 10)
    }


def compute_development_velocity(commits: int, prs_merged: int, days: int = 7) -> float:
    """Estimate development velocity score 0-100."""
    daily_commits = commits / max(days, 1)
    return min(100.0, daily_commits * 20 + prs_merged * 15)

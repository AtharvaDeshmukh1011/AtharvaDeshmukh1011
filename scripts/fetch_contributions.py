import json
import os
import sys
import urllib.request
from pathlib import Path

USER = "AtharvaDeshmukh1011"
OUT = Path(__file__).parent.parent / "data" / "contributions.json"
QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
    }
  }
}
"""
LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}


def fetch(token: str) -> dict:
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        calendar = json.load(response)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [
        [{"date": d["date"], "count": d["contributionCount"], "level": LEVELS[d["contributionLevel"]]} for d in w["contributionDays"]]
        for w in calendar["weeks"]
    ]
    return {"total": calendar["totalContributions"], "weeks": weeks}


if __name__ == "__main__":
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if not token:
        sys.exit("set GH_TOKEN")
    data = fetch(token)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1), encoding="utf-8")
    print(data["total"], "contributions,", len(data["weeks"]), "weeks")

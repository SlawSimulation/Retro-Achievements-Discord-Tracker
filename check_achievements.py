import os
import time
import json
import requests
from datetime import datetime

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

def fetch_recent_achievements(username, api_key):
    url = f"https://retroachievements.org/API/API_GetUserRecentAchievements.php?z={username}&y={api_key}&u={username}&c=1"
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    return []

def post_to_discord(achievement):
    embed = {
        "title": f"🏆 {achievement['Title']}",
        "description": achievement["Description"],
        "url": f"https://retroachievements.org/Game/{achievement['GameID']}",
        "thumbnail": {
            "url": f"https://media.retroachievements.org/Badge/{achievement['BadgeName']}.png"
        },
        "color": 0x00ff00,
        "footer": {
            "text": f"Game: {achievement['GameTitle']}"
        },
        "timestamp": datetime.utcfromtimestamp(achievement["AchievedOn"]).isoformat()
    }

    payload = {
        "username": "RA-Bot",
        "avatar_url": "https://retroachievements.org/favicon.ico",
        "embeds": [embed]
    }

    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print(f"✅ Posted: {achievement['Title']}")
    else:
        print(f"❌ Failed to post: {response.status_code} - {response.text}")

def main():
    users = load_users()

    for user in users:
        recent = fetch_recent_achievements(user["username"], user["api_key"])
        new_achievements = [a for a in recent if a["AchievedOn"] > user.get("last_checked", 0)]

        for ach in sorted(new_achievements, key=lambda x: x["AchievedOn"]):
            post_to_discord(ach)
            user["last_checked"] = ach["AchievedOn"]

    save_users(users)

if __name__ == "__main__":
    if not DISCORD_WEBHOOK_URL:
        print("❌ DISCORD_WEBHOOK_URL not set.")
    else:
        main()

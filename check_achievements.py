import json
import requests
import datetime
import time
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

def get_recent_achievements(username, api_key):
    url = f"https://retroachievements.org/API/API_GetUserRecentAchievements.php"
    params = {
        "z": username,
        "y": api_key,
        "u": username
    }
    response = requests.get(url, params=params)
    return response.json()

def post_to_discord(user, achievement):
    embed = {
        "title": f"🏆 {user['ra_username']} unlocked an achievement!",
        "description": f"**{achievement['Title']}**\n{achievement['Description']}",
        "url": f"https://retroachievements.org/Game/{achievement['GameID']}",
        "thumbnail": {"url": achievement["BadgeURL"]},
        "footer": {"text": achievement["GameTitle"]},
        "timestamp": achievement["DateEarned"]
    }

    payload = {"embeds": [embed]}
    response = requests.post(WEBHOOK_URL, json=payload)
    if response.status_code != 204:
        print(f"Failed to send Discord message: {response.status_code} - {response.text}")

def main():
    users = load_users()
    updated = False

    for user in users:
        print(f"Checking {user['ra_username']}...")
        recent = get_recent_achievements(user["ra_username"], user["ra_api_key"])
        if not recent:
            continue

        last_check_time = datetime.datetime.fromisoformat(user["last_check"].replace("Z", "+00:00"))
        new_achievements = []

        for achievement in recent:
            earned_time = datetime.datetime.strptime(achievement["DateEarned"], "%Y-%m-%d %H:%M:%S")
            if earned_time > last_check_time:
                new_achievements.append(achievement)

        for ach in sorted(new_achievements, key=lambda x: x["DateEarned"]):
            post_to_discord(user, ach)

        if new_achievements:
            newest_time = max(datetime.datetime.strptime(a["DateEarned"], "%Y-%m-%d %H:%M:%S") for a in new_achievements)
            user["last_check"] = newest_time.isoformat() + "Z"
            updated = True

    if updated:
        save_users(users)

if __name__ == "__main__":
    main()

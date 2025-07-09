import os
import requests
from datetime import datetime

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL") or "https://discord.com/api/webhooks/..."

def test_embed_post():
    embed = {
        "title": "🏆 SlawPro unlocked an achievement!",
        "description": "**First Steps**\nYou started your retro journey!",
        "url": "https://retroachievements.org/Game/1234",
        "thumbnail": {
            "url": "https://media.retroachievements.org/Badge/12345.png"
        },
        "color": 0x00ff00,
        "footer": {
            "text": "Game: Super Retro Adventure"
        },
        "timestamp": datetime.utcnow().isoformat()
    }

    payload = {
        "username": "RA-Bot",
        "avatar_url": "https://retroachievements.org/favicon.ico",
        "embeds": [embed]
    }

    response = requests.post(WEBHOOK_URL, json=payload)

    if response.status_code == 204:
        print("✅ Embed sent successfully.")
    else:
        print(f"❌ Failed to send embed. Status: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_embed_post()

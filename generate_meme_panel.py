import base64
import urllib.request
import json
from datetime import datetime, timezone

USERNAME = "irti-11"

BG_COLOR = "#0d1117"
CARD_BG = "#151922"
DIVIDER = "#1e222a"
COLOR_PINK = "#f2a6c3"
COLOR_CYAN = "#78dec7"

MEME_MAP = {
    "shipping": {"file": "meme_shipping.jpg", "caption": "when the code just... works"},
    "active":   {"file": "meme_active.jpg",   "caption": "crafting the perfect commit message"},
    "quiet":    {"file": "meme_quiet.jpg",    "caption": "floating between commits"},
}


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "profile-status-script"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())


def get_status():
    try:
        events = fetch_json(f"https://api.github.com/users/{USERNAME}/events/public")
    except Exception as e:
        print("API fetch failed:", e)
        return "quiet"

    push_events = [e for e in events if e.get("type") == "PushEvent"]
    now = datetime.now(timezone.utc)
    week_commits = 0
    for e in push_events:
        dt = datetime.strptime(e["created_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        if (now - dt).days <= 7:
            week_commits += sum(1 for _ in e.get("payload", {}).get("commits", []))

    if week_commits >= 5:
        return "shipping"
    elif week_commits >= 1:
        return "active"
    return "quiet"


def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def generate(width=340, img_h=260):
    status = get_status()
    meme = MEME_MAP[status]
    b64 = img_to_b64(meme["file"])

    card_h = img_h + 50
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {width} {card_h}" width="100%" height="{card_h}" preserveAspectRatio="xMinYMin meet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&amp;display=swap');
    </style>
    <rect width="100%" height="100%" fill="{BG_COLOR}" rx="8" />
    <rect x="0" y="0" width="{width}" height="{card_h}" rx="10" fill="{CARD_BG}" stroke="{DIVIDER}" stroke-width="1" />

    <clipPath id="memeClip">
        <rect x="10" y="10" width="{width-20}" height="{img_h}" rx="6" />
    </clipPath>
    <image x="10" y="10" width="{width-20}" height="{img_h}"
           preserveAspectRatio="xMidYMid slice"
           xlink:href="data:image/jpeg;base64,{b64}" clip-path="url(#memeClip)" />

    <text x="{width/2}" y="{img_h + 32}" text-anchor="middle"
          style="font-family:'Fira Code',monospace; font-size:11.5px; fill:{COLOR_CYAN};">{meme["caption"]}</text>
</svg>'''

    with open("meme_panel.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated meme_panel.svg — status: {status}, meme: {meme['file']}")


if __name__ == "__main__":
    generate()
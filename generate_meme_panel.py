import base64
import urllib.request
import json
import time
import os
from datetime import datetime, timezone, timedelta

USERNAME = "irti-11"
TOKEN = os.environ.get("GH_PAT")

BG_GRADIENT_START = "#1e222a"
BG_GRADIENT_END = "#0d1117"
DIVIDER = "#2a313c"
TEXT_COLOR = "#e2e8f0"
ACCENT_COLOR = "#78dec7"

MEME_MAP = {
    "shipping": {"file": "meme_shipping.jpg", "caption": "🔥 shipping code like a boss"},
    "active":   {"file": "meme_active.jpg",   "caption": "👨‍💻 crafting the perfect commit"},
    "quiet":    {"file": "meme_quiet.jpg",    "caption": "💤 floating in the void"},
}


def fetch_json(url, retries=3):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "profile-status-script")
    if TOKEN:
        req.add_header("Authorization", f"token {TOKEN}")
    last_error = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            last_error = e
            time.sleep(2)
    raise last_error


def count_week_commits(repos, since_iso):
    total = 0
    for r in repos:
        owner = r.get("owner", {}).get("login", USERNAME)
        name = r.get("name")
        if not name:
            continue
        url = f"https://api.github.com/repos/{owner}/{name}/commits?since={since_iso}&author={USERNAME}&per_page=100"
        try:
            commits = fetch_json(url, retries=1)
            total += len(commits)
        except Exception:
            continue
    return total


def get_status():
    try:
        repos = fetch_json("https://api.github.com/user/repos?per_page=100")
    except Exception as e:
        print("API fetch failed:", e)
        return "quiet"

    since_iso = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    week_commits = count_week_commits(repos, since_iso)

    if week_commits >= 5:
        return "shipping"
    elif week_commits >= 1:
        return "active"
    return "quiet"


def img_to_b64(path):
    if not os.path.exists(path):
        print(f"Warning: {path} not found. Creating a blank placeholder.")
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def generate(width=400, img_h=300):
    status = get_status()
    meme = MEME_MAP[status]
    b64 = img_to_b64(meme["file"])

    card_h = img_h + 80

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {width} {card_h}" width="100%" height="{card_h}" preserveAspectRatio="xMinYMin meet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@500;700&amp;display=swap');
    </style>

    <defs>
        <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{BG_GRADIENT_START}"/>
            <stop offset="100%" stop-color="{BG_GRADIENT_END}"/>
        </linearGradient>
        <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#000000" flood-opacity="0.5"/>
        </filter>
        <clipPath id="memeClip">
            <rect x="20" y="20" width="{width-40}" height="{img_h}" rx="12" />
        </clipPath>
    </defs>

    <rect x="0" y="0" width="{width}" height="{card_h}" rx="16" fill="url(#bgGrad)" stroke="{DIVIDER}" stroke-width="1.5" />

    <g filter="url(#shadow)">
        <rect x="20" y="20" width="{width-40}" height="{img_h}" rx="12" fill="#000" />
        '''

    if b64:
        svg += f'<image x="20" y="20" width="{width-40}" height="{img_h}" preserveAspectRatio="xMidYMid slice" xlink:href="data:image/jpeg;base64,{b64}" clip-path="url(#memeClip)" />'

    svg += f'''
    </g>

    <text x="{width/2}" y="{img_h + 55}" text-anchor="middle"
          style="font-family:'Fira Code', monospace; font-size: 15px; font-weight: 700; fill: {TEXT_COLOR}; letter-spacing: 0.5px;">
        {meme["caption"]}
    </text>

    <text x="{width/2}" y="{img_h + 70}" text-anchor="middle"
          style="font-family:'Fira Code', monospace; font-size: 11px; font-weight: 500; fill: {ACCENT_COLOR};">
        Current Mode: {status.upper()}
    </text>
</svg>'''

    with open("meme_panel.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Success: Generated meme_panel.svg — Mode: {status}")


if __name__ == "__main__":
    generate()
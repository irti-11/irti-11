import base64
import urllib.request
import json
from datetime import datetime, timezone
import os

USERNAME = "irti-11"

# --- Premium Colors & Styling ---
BG_GRADIENT_START = "#1e222a"
BG_GRADIENT_END = "#0d1117"
DIVIDER = "#2a313c"
TEXT_COLOR = "#e2e8f0"
ACCENT_COLOR = "#78dec7"

# --- Meme Dictionary ---
# Make sure you save 3 images in your folder with these exact names!
MEME_MAP = {
    "shipping": {"file": "meme_shipping.jpg", "caption": "🔥 shipping code like a boss"},
    "active":   {"file": "meme_active.jpg",   "caption": "👨‍💻 crafting the perfect commit"},
    "quiet":    {"file": "meme_quiet.jpg",    "caption": "💤 floating in the void"},
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
    # Fallback if image is missing so the script doesn't crash
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
    
    # Premium SVG Template
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {width} {card_h}" width="100%" height="{card_h}" preserveAspectRatio="xMinYMin meet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@500;700&amp;display=swap');
    </style>
    
    <defs>
        <!-- Modern Background Gradient -->
        <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{BG_GRADIENT_START}"/>
            <stop offset="100%" stop-color="{BG_GRADIENT_END}"/>
        </linearGradient>
        
        <!-- Soft Drop Shadow for the Image -->
        <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#000000" flood-opacity="0.5"/>
        </filter>
        
        <clipPath id="memeClip">
            <rect x="20" y="20" width="{width-40}" height="{img_h}" rx="12" />
        </clipPath>
    </defs>

    <!-- Base Card -->
    <rect x="0" y="0" width="{width}" height="{card_h}" rx="16" fill="url(#bgGrad)" stroke="{DIVIDER}" stroke-width="1.5" />

    <!-- Meme Image with Clip & Shadow -->
    <g filter="url(#shadow)">
        <rect x="20" y="20" width="{width-40}" height="{img_h}" rx="12" fill="#000" />
        '''
        
    if b64:
        svg += f'<image x="20" y="20" width="{width-40}" height="{img_h}" preserveAspectRatio="xMidYMid slice" xlink:href="data:image/jpeg;base64,{b64}" clip-path="url(#memeClip)" />'
        
    svg += f'''
    </g>

    <!-- Status Caption -->
    <text x="{width/2}" y="{img_h + 55}" text-anchor="middle"
          style="font-family:'Fira Code', monospace; font-size: 15px; font-weight: 700; fill: {TEXT_COLOR}; letter-spacing: 0.5px;">
        {meme["caption"]}
    </text>
    
    <!-- Small Status Indicator -->
    <text x="{width/2}" y="{img_h + 70}" text-anchor="middle"
          style="font-family:'Fira Code', monospace; font-size: 11px; font-weight: 500; fill: {ACCENT_COLOR};">
        Current Mode: {status.upper()}
    </text>
</svg>'''

    with open("dynamic_meme.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"✨ Success: Generated dynamic_meme.svg — Mode: {status}")

if __name__ == "__main__":
    generate()
import urllib.request
import time
import json
import base64
import os
from datetime import datetime, timezone

USERNAME = "irti-11"

# --- Premium Colors ---
BG_GRAD_START = "#1e222a"
BG_GRAD_END = "#0d1117"
CARD_BORDER = "#2a313c"
COLOR_CYAN = "#78dec7"
COLOR_PINK = "#f2a6c3"
COLOR_WHITE = "#e2e8f0"
COLOR_DIM = "#8b9eb0"
BUBBLE_BG = "#151922"

def fetch_json(url, retries=3):
    req = urllib.request.Request(url, headers={"User-Agent": "profile-status-script"})
    last_error = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            last_error = e
            time.sleep(2)
    raise last_error

def get_github_data():
    try:
        user = fetch_json(f"https://api.github.com/users/{USERNAME}")
        repos = fetch_json(f"https://api.github.com/users/{USERNAME}/repos?per_page=100")
        events = fetch_json(f"https://api.github.com/users/{USERNAME}/events/public")
    except Exception as e:
        print("API fetch failed, using fallback data:", e)
        return {"public_repos": 0, "followers": 0, "last_commit": "unknown", "week_commits": 0, "top_lang": "N/A", "status": "quiet"}

    push_events = [e for e in events if e.get("type") == "PushEvent"]

    last_commit = "no recent activity"
    if push_events:
        dt = datetime.strptime(push_events[0]["created_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        delta = datetime.now(timezone.utc) - dt
        hours = int(delta.total_seconds() // 3600)
        if hours < 1:
            last_commit = "just now"
        elif hours < 24:
            last_commit = f"{hours}h ago"
        else:
            last_commit = f"{hours // 24}d ago"

    now = datetime.now(timezone.utc)
    week_commits = 0
    for e in push_events:
        dt = datetime.strptime(e["created_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        if (now - dt).days <= 7:
            week_commits += sum(1 for _ in e.get("payload", {}).get("commits", []))

    lang_count = {}
    for r in repos:
        lang = r.get("language")
        if lang: lang_count[lang] = lang_count.get(lang, 0) + 1
    top_lang = max(lang_count, key=lang_count.get) if lang_count else "N/A"

    status = "shipping" if week_commits >= 5 else "active" if week_commits >= 1 else "quiet"

    return {
        "public_repos": user.get("public_repos", 0),
        "followers": user.get("followers", 0),
        "last_commit": last_commit,
        "week_commits": week_commits,
        "top_lang": top_lang,
        "status": status,
    }

def img_to_b64(path):
    if not os.path.exists(path):
        print(f"Warning: {path} not found! Character won't load.")
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def generate(width=400):
    data = get_github_data()
    char_b64 = img_to_b64("pixel_boy.png")  # Apni image ka naam yahan match karna
    
    status_color = COLOR_CYAN if data['status'] == 'active' else "#aef3a4" if data['status'] == 'shipping' else COLOR_DIM
    
    rows = [
        ("📦", "Public Repos", str(data["public_repos"])),
        ("👥", "Followers", str(data["followers"])),
        ("⏱️", "Last Commit", data["last_commit"]),
        ("📈", "This Week", f'{data["week_commits"]} commits'),
        ("💬", "Top Language", data["top_lang"]),
    ]
    
    stats_h = 240
    char_h = 160
    total_h = stats_h + char_h + 30

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {total_h}" width="100%" height="{total_h}">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600;700&amp;display=swap');
        
        .title {{ font-family: 'Fira Code', monospace; font-size: 16px; font-weight: 700; fill: {COLOR_PINK}; }}
        .label {{ font-family: 'Fira Code', monospace; font-size: 13px; font-weight: 400; fill: {COLOR_WHITE}; }}
        .value {{ font-family: 'Fira Code', monospace; font-size: 13px; font-weight: 600; fill: {COLOR_CYAN}; }}
        
        /* Character Animations */
        .char-wrapper {{
            transition: transform 0.3s ease;
        }}
        
        /* The walk animation triggers when hovering the interactive zone */
        .interactive-zone:hover .char-wrapper {{
            animation: walkLeftRight 3s ease-in-out infinite alternate;
        }}
        
        @keyframes walkLeftRight {{
            0% {{ transform: translateX(-40px); }}
            100% {{ transform: translateX(40px); }}
        }}

        /* Speech Bubble Animations */
        .bubble {{
            opacity: 0;
            transform: scale(0.8) translateY(10px);
            transform-origin: center bottom;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        
        .interactive-zone:hover .bubble {{
            opacity: 1;
            transform: scale(1) translateY(0);
        }}

        /* Cycling Text Messages */
        .msg {{
            opacity: 0;
            font-family: 'Fira Code', monospace; 
            font-size: 11px; 
            font-weight: 600; 
            fill: {COLOR_WHITE};
        }}
        
        /* Only cycle texts when hovering */
        .interactive-zone:hover .msg1 {{ animation: cycle 9s infinite 0s; }}
        .interactive-zone:hover .msg2 {{ animation: cycle 9s infinite 3s; }}
        .interactive-zone:hover .msg3 {{ animation: cycle 9s infinite 6s; }}

        @keyframes cycle {{
            0%, 25% {{ opacity: 1; }}
            33%, 100% {{ opacity: 0; }}
        }}
    </style>

    <defs>
        <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{BG_GRAD_START}"/>
            <stop offset="100%" stop-color="{BG_GRAD_END}"/>
        </linearGradient>
        <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="0" dy="5" stdDeviation="5" flood-color="#000" flood-opacity="0.3"/>
        </filter>
    </defs>

    <!-- Base Card -->
    <rect x="0" y="0" width="{width}" height="{total_h}" rx="16" fill="url(#bgGrad)" stroke="{CARD_BORDER}" stroke-width="2" />

    <!-- Title Section -->
    <text x="20" y="35" class="title">Irtiza's GitHub Status</text>
    <line x1="20" y1="48" x2="{width-20}" y2="48" stroke="{CARD_BORDER}" stroke-width="1.5" />

    <!-- Stats Section -->
    '''
    y = 75
    for icon, label_txt, val in rows:
        svg += f'''
        <text x="20" y="{y}" class="label">{icon}  {label_txt}</text>
        <text x="{width-20}" y="{y}" text-anchor="end" class="value">{val}</text>
        '''
        y += 32

    # Divider before character
    y_char_section = y + 10
    svg += f'''
    <line x1="20" y1="{y_char_section}" x2="{width-20}" y2="{y_char_section}" stroke="{CARD_BORDER}" stroke-width="1.5" />
    <rect x="20" y="{y_char_section+15}" width="{width-40}" height="30" rx="15" fill="{CARD_BORDER}" />
    <text x="{width/2}" y="{y_char_section+35}" text-anchor="middle" style="font-family:'Fira Code',monospace; font-size:12px; font-weight:700; fill:{status_color};">MODE: {data['status'].upper()}</text>
    '''

    # --- Interactive Character Zone ---
    svg += f'''
    <g class="interactive-zone">
        <!-- Invisible trigger box covers the entire bottom area -->
        <rect x="0" y="{y_char_section}" width="{width}" height="{char_h+50}" fill="transparent" cursor="pointer" />
        
        <g class="char-wrapper">
            <!-- Speech Bubble -->
            <g class="bubble" transform="translate({width/2 - 65}, {y_char_section + 65})">
                <!-- Bubble Tail -->
                <polygon points="65,30 55,38 75,30" fill="{BUBBLE_BG}" />
                <!-- Bubble Body -->
                <rect x="0" y="0" width="130" height="30" rx="8" fill="{BUBBLE_BG}" stroke="{COLOR_CYAN}" stroke-width="1" filter="url(#shadow)"/>
                
                <!-- Cycling Messages -->
                <text x="65" y="19" text-anchor="middle" class="msg msg1">Hi, I'm Irtiza!</text>
                <text x="65" y="19" text-anchor="middle" class="msg msg2">Writing clean code 🚀</text>
                <text x="65" y="19" text-anchor="middle" class="msg msg3">Checking commits...</text>
            </g>
            
            <!-- The Pixel Character -->
            <image href="data:image/png;base64,{char_b64}" x="{width/2 - 40}" y="{y_char_section + 95}" width="80" height="80" preserveAspectRatio="xMidYMid meet" filter="url(#shadow)" />
        </g>
    </g>
    '''
    svg += '</svg>'

    with open("status_panel.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"✨ Success: Generated status_panel.svg with interactive pixel boy!")

if __name__ == "__main__":
    generate()
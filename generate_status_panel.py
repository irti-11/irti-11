import urllib.request
import json
from datetime import datetime, timezone

USERNAME = "irti-11"

COLOR_CYAN = "#78dec7"
COLOR_PINK = "#f2a6c3"
COLOR_GREEN = "#aef3a4"
COLOR_WHITE = "#e2e8f0"
COLOR_DIM = "#6272a4"
BG_COLOR = "#0d1117"
CARD_BG = "#151922"
DIVIDER = "#1e222a"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "profile-status-script"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())


def get_github_data():
    try:
        user = fetch_json(f"https://api.github.com/users/{USERNAME}")
        repos = fetch_json(f"https://api.github.com/users/{USERNAME}/repos?per_page=100")
        events = fetch_json(f"https://api.github.com/users/{USERNAME}/events/public")
    except Exception as e:
        print("API fetch failed, using fallback data:", e)
        return {
            "public_repos": 0, "followers": 0, "last_commit": "unknown",
            "week_commits": 0, "top_lang": "N/A", "status": "quiet"
        }

    push_events = [e for e in events if e.get("type") == "PushEvent"]

    last_commit = "no recent activity"
    if push_events:
        dt = datetime.strptime(push_events[0]["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        dt = dt.replace(tzinfo=timezone.utc)
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
        if lang:
            lang_count[lang] = lang_count.get(lang, 0) + 1
    top_lang = max(lang_count, key=lang_count.get) if lang_count else "N/A"

    if week_commits >= 5:
        status = "shipping"
    elif week_commits >= 1:
        status = "active"
    else:
        status = "quiet"

    return {
        "public_repos": user.get("public_repos", 0),
        "followers": user.get("followers", 0),
        "last_commit": last_commit,
        "week_commits": week_commits,
        "top_lang": top_lang,
        "status": status,
    }


STATUS_LABELS = {
    "shipping": ("🚀 actively shipping", COLOR_GREEN),
    "active": ("🛠️ in progress", COLOR_CYAN),
    "quiet": ("💤 taking a break", COLOR_DIM),
}


def build_status_card(data, width):
    label, color = STATUS_LABELS[data["status"]]
    rows = [
        ("📦", "Public Repos", str(data["public_repos"])),
        ("👥", "Followers", str(data["followers"])),
        ("⏱️", "Last Commit", data["last_commit"]),
        ("📈", "This Week", f'{data["week_commits"]} commits'),
        ("💬", "Top Language", data["top_lang"]),
    ]

    h = 34 + len(rows) * 30 + 30
    svg = f'''<g>
    <rect x="0" y="0" width="{width}" height="{h}" rx="10" fill="{CARD_BG}" stroke="{DIVIDER}" stroke-width="1" />
    <text x="16" y="26" style="font-family:'Fira Code',monospace; font-size:14px; font-weight:600; fill:{COLOR_PINK};">GitHub Status</text>
    <line x1="16" y1="34" x2="{width-16}" y2="34" style="stroke:{DIVIDER}; stroke-width:1;" />
'''
    y = 58
    for icon, label_txt, val in rows:
        svg += f'''    <text x="16" y="{y}" style="font-family:'Fira Code',monospace; font-size:12px; fill:{COLOR_WHITE};">{icon}  {label_txt}</text>
    <text x="{width-16}" y="{y}" text-anchor="end" style="font-family:'Fira Code',monospace; font-size:12px; font-weight:600; fill:{COLOR_CYAN};">{val}</text>
'''
        y += 30
    svg += f'''    <rect x="16" y="{y-10}" width="{width-32}" height="22" rx="11" fill="{BG_COLOR}" stroke="{color}" stroke-width="1" />
    <text x="{width/2}" y="{y+5}" text-anchor="middle" style="font-family:'Fira Code',monospace; font-size:11px; font-weight:600; fill:{color};">{label}</text>
</g>'''
    return svg, h


def build_character(width, y_offset, box_h=110):
    cx = width / 2
    cy = y_offset + box_h / 2 + 6

    cycle = 12
    def win(i):
        return i * 4, i * 4 + 4

    def opacity_anim(start, end):
        fade = 0.4
        kt = [0, round(start/cycle,4), round((start+fade)/cycle,4),
              round((end-fade)/cycle,4), round(end/cycle,4)]
        vals = [0, 0, 1, 1, 0]
        if kt[-1] < 1:
            kt.append(1); vals.append(0)
        return ";".join(map(str, kt)), ";".join(map(str, vals))

    s1, s2 = win(0)
    a1, a2 = win(1)
    b1, b2 = win(2)

    kt_sleep, v_sleep = opacity_anim(s1, s2)
    kt_dance, v_dance = opacity_anim(a1, a2)
    kt_wave, v_wave = opacity_anim(b1, b2)

    svg = f'''<g>
    <rect x="0" y="{y_offset}" width="{width}" height="{box_h}" rx="10" fill="{CARD_BG}" stroke="{DIVIDER}" stroke-width="1" />

    <g opacity="0">
        <animate attributeName="opacity" keyTimes="{kt_sleep}" values="{v_sleep}" dur="{cycle}s" repeatCount="indefinite" />
        <ellipse cx="{cx}" cy="{cy+10}" rx="26" ry="18" fill="{COLOR_CYAN}" />
        <line x1="{cx-10}" y1="{cy+6}" x2="{cx-4}" y2="{cy+6}" stroke="{BG_COLOR}" stroke-width="2" stroke-linecap="round" />
        <line x1="{cx+4}" y1="{cy+6}" x2="{cx+10}" y2="{cy+6}" stroke="{BG_COLOR}" stroke-width="2" stroke-linecap="round" />
        <text x="{cx+24}" y="{cy-14}" style="font-family:monospace; font-size:14px; fill:{COLOR_DIM};">z
            <animate attributeName="y" values="{cy-10};{cy-30}" dur="2s" repeatCount="indefinite" />
            <animate attributeName="opacity" values="1;0" dur="2s" repeatCount="indefinite" />
        </text>
        <text x="{cx+34}" y="{cy-22}" style="font-family:monospace; font-size:10px; fill:{COLOR_DIM};">Z
            <animate attributeName="y" values="{cy-18};{cy-36}" dur="2s" begin="0.7s" repeatCount="indefinite" />
            <animate attributeName="opacity" values="1;0" dur="2s" begin="0.7s" repeatCount="indefinite" />
        </text>
    </g>

    <g opacity="0">
        <animate attributeName="opacity" keyTimes="{kt_dance}" values="{v_dance}" dur="{cycle}s" repeatCount="indefinite" />
        <g>
            <animateTransform attributeName="transform" type="translate" values="0,0; 0,-8; 0,0; 0,-8; 0,0" dur="0.9s" repeatCount="indefinite" />
            <circle cx="{cx}" cy="{cy}" r="20" fill="{COLOR_PINK}" />
            <circle cx="{cx-7}" cy="{cy-4}" r="2.4" fill="{BG_COLOR}" />
            <circle cx="{cx+7}" cy="{cy-4}" r="2.4" fill="{BG_COLOR}" />
            <path d="M {cx-7} {cy+6} Q {cx} {cy+12} {cx+7} {cy+6}" stroke="{BG_COLOR}" stroke-width="2" fill="none" stroke-linecap="round" />
        </g>
    </g>

    <g opacity="0">
        <animate attributeName="opacity" keyTimes="{kt_wave}" values="{v_wave}" dur="{cycle}s" repeatCount="indefinite" />
        <circle cx="{cx}" cy="{cy}" r="20" fill="{COLOR_GREEN}" />
        <circle cx="{cx-7}" cy="{cy-4}" r="2.4" fill="{BG_COLOR}" />
        <circle cx="{cx+7}" cy="{cy-4}" r="2.4" fill="{BG_COLOR}" />
        <path d="M {cx-8} {cy+5} Q {cx} {cy+13} {cx+8} {cy+5}" stroke="{BG_COLOR}" stroke-width="2" fill="none" stroke-linecap="round" />
        <g>
            <animateTransform attributeName="transform" type="rotate" values="0 {cx+22} {cy-8}; 30 {cx+22} {cy-8}; 0 {cx+22} {cy-8}" dur="0.6s" repeatCount="indefinite" />
            <line x1="{cx+20}" y1="{cy}" x2="{cx+22}" y2="{cy-16}" stroke="{COLOR_GREEN}" stroke-width="5" stroke-linecap="round" />
        </g>
    </g>
</g>'''
    return svg


def generate(width=340):
    data = get_github_data()
    status_svg, status_h = build_status_card(data, width)
    char_y = status_h + 14
    char_svg = build_character(width, char_y, box_h=110)
    total_h = char_y + 110

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {total_h}" width="100%" height="{total_h}" preserveAspectRatio="xMinYMin meet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&amp;display=swap');
    </style>
    <rect width="100%" height="100%" fill="{BG_COLOR}" rx="8" />
{status_svg}
{char_svg}
</svg>'''

    with open("status_panel.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated status_panel.svg — status: {data['status']}, week_commits: {data['week_commits']}")


if __name__ == "__main__":
    generate()
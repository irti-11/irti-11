import base64
import html
import os

PROJECTS = [
    {
        "file": "stylebazaar.jpg",
        "title": "Style Bazaar",
        "subtitle": "Full-stack e-commerce (PHP, MySQL, JS, AJAX)",
        "bullets": [
            "OTP-verified auth + admin/employee panels",
            "Real-time return-request notifications",
            "Live checkout with card preview",
        ],
    },
    {
        "file": "mrcone.jpg",
        "title": "Mr. Cone",
        "subtitle": "Restaurant landing page (HTML, CSS, JS)",
        "bullets": [
            "Full-width hero with layered imagery",
            "Responsive, mobile-first layout",
            "Custom typography and sectioned content",
        ],
    },
    {
        "file": "32smiles.jpg",
        "title": "32Smiles",
        "subtitle": "Dental clinic website (HTML, CSS, JS)",
        "bullets": [
            "Split-screen hero with service nav",
            "Thumbnail gallery + testimonials",
            "Clean, accessible medical-brand UI",
        ],
    },
]

BG_COLOR = "#0d1117"
BEZEL_COLOR = "#1a1d24"
BEZEL_EDGE = "#2a2e37"
STAND_COLOR = "#1a1d24"
ACCENT = "#78dec7"
TITLE_COLOR = "#f2a6c3"
BODY_COLOR = "#e2e8f0"
DIVIDER_COLOR = "#1e222a"

SCREEN_W = 340
SCREEN_H = 215
BEZEL = 10
SCREEN_X = 30
SCREEN_Y = 26

PANEL_W = 400
GAP = 30

PER_IMAGE = 4.0
FADE = 0.6


def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def generate():
    n = len(PROJECTS)
    cycle = n * PER_IMAGE

    monitor_area_w = SCREEN_X * 2 + SCREEN_W
    svg_w = monitor_area_w + GAP + PANEL_W
    svg_h = SCREEN_Y + SCREEN_H + BEZEL + 60

    def frac(t):
        return round(t / cycle, 5)

    def opacity_kt_vals(start, end):
        fade_in_end = start + FADE
        hold_end = end - FADE
        points = [(0, 0), (frac(start), 0), (frac(fade_in_end), 1),
                  (frac(hold_end), 1), (frac(end), 0)]
        if points[-1][0] < 1:
            points.append((1, 0))
        kt = ";".join(str(p[0]) for p in points)
        vals = ";".join(str(p[1]) for p in points)
        return kt, vals

    images_svg = ""
    panel_svg = ""

    text_x = monitor_area_w + GAP
    for i, proj in enumerate(PROJECTS):
        start = i * PER_IMAGE
        end = start + PER_IMAGE
        kt, vals = opacity_kt_vals(start, end)

        b64 = img_to_b64(proj["file"])
        images_svg += f'''    <g clip-path="url(#screenClip)">
        <image x="{SCREEN_X}" y="{SCREEN_Y}" width="{SCREEN_W}" height="{SCREEN_H}"
               preserveAspectRatio="xMidYMid slice"
               xlink:href="data:image/jpeg;base64,{b64}" opacity="0">
            <animate attributeName="opacity" keyTimes="{kt}" values="{vals}"
                     dur="{cycle}s" repeatCount="indefinite" calcMode="linear" />
        </image>
    </g>
'''
        title = html.escape(proj["title"])
        subtitle = html.escape(proj["subtitle"])

        ty = 50
        panel_svg += f'''    <g opacity="0">
        <animate attributeName="opacity" keyTimes="{kt}" values="{vals}" dur="{cycle}s" repeatCount="indefinite" calcMode="linear" />
        <text x="{text_x}" y="{ty}" style="font-family:'Fira Code',monospace; font-size:19px; font-weight:600; fill:{TITLE_COLOR};">{title}</text>
        <text x="{text_x}" y="{ty + 24}" style="font-family:'Fira Code',monospace; font-size:12px; fill:{ACCENT};">{subtitle}</text>
'''
        by = ty + 55
        for b in proj["bullets"]:
            safe_b = html.escape(b)
            panel_svg += f'''        <text x="{text_x}" y="{by}" style="font-family:'Fira Code',monospace; font-size:12.5px; fill:{BODY_COLOR};">&#8226; {safe_b}</text>
'''
            by += 24
        panel_svg += '    </g>\n'

    stand_x = SCREEN_X + SCREEN_W / 2
    screen_bottom = SCREEN_Y + SCREEN_H + BEZEL

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {svg_w} {svg_h}" width="100%" height="{svg_h}" preserveAspectRatio="xMinYMin meet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&amp;display=swap');
    </style>
    <rect width="100%" height="100%" fill="{BG_COLOR}" rx="8" />
    <line x1="{monitor_area_w + GAP/2}" y1="10" x2="{monitor_area_w + GAP/2}" y2="{svg_h - 10}"
          style="stroke:{DIVIDER_COLOR}; stroke-width:1;" />

    <rect x="{SCREEN_X - BEZEL}" y="{SCREEN_Y - BEZEL}"
          width="{SCREEN_W + BEZEL * 2}" height="{SCREEN_H + BEZEL * 2}"
          rx="12" fill="{BEZEL_COLOR}" stroke="{BEZEL_EDGE}" stroke-width="1.5" />
    <clipPath id="screenClip">
        <rect x="{SCREEN_X}" y="{SCREEN_Y}" width="{SCREEN_W}" height="{SCREEN_H}" rx="3" />
    </clipPath>
    <rect x="{SCREEN_X}" y="{SCREEN_Y}" width="{SCREEN_W}" height="{SCREEN_H}" rx="3" fill="#000000" />
{images_svg}
    <rect x="{SCREEN_X}" y="{SCREEN_Y}" width="{SCREEN_W}" height="{SCREEN_H}" rx="3"
          fill="url(#glare)" opacity="0.5" clip-path="url(#screenClip)" />
    <defs>
        <linearGradient id="glare" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#ffffff" stop-opacity="0.06" />
            <stop offset="40%" stop-color="#ffffff" stop-opacity="0" />
        </linearGradient>
    </defs>
    <rect x="{stand_x - 5}" y="{screen_bottom}" width="10" height="18" fill="{STAND_COLOR}" />
    <rect x="{stand_x - 38}" y="{screen_bottom + 18}" width="76" height="7" rx="3" fill="{STAND_COLOR}" />

{panel_svg}
</svg>'''

    with open("project_monitor.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated project_monitor.svg, cycle={cycle}s, size={os.path.getsize('project_monitor.svg')/1024:.1f}KB")


if __name__ == "__main__":
    generate()
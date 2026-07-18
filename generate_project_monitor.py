import base64
import os

PROJECTS = [
    {"file": "stylebazaar.jpg", "label": "Style Bazaar"},
    {"file": "mrcone.jpg", "label": "Mr. Cone"},
    {"file": "32smiles.jpg", "label": "32Smiles"},
]

BG_COLOR = "#0d1117"
BEZEL_COLOR = "#1a1d24"
BEZEL_EDGE = "#2a2e37"
STAND_COLOR = "#1a1d24"
ACCENT = "#78dec7"

SCREEN_W = 500
SCREEN_H = 275
BEZEL = 14
SCREEN_X = 40
SCREEN_Y = 30

PER_IMAGE = 3.5
FADE = 0.6


def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def generate():
    n = len(PROJECTS)
    cycle = n * PER_IMAGE
    svg_w = SCREEN_X * 2 + SCREEN_W
    svg_h = SCREEN_Y + SCREEN_H + BEZEL + 90

    def frac(t):
        return round(t / cycle, 5)

    images_svg = ""
    label_svg = ""

    for i, proj in enumerate(PROJECTS):
        start = i * PER_IMAGE
        fade_in_end = start + FADE
        hold_end = start + PER_IMAGE - FADE
        end = start + PER_IMAGE

        points = [(0, 0), (frac(start), 0), (frac(fade_in_end), 1),
                  (frac(hold_end), 1), (frac(end), 0)]
        if points[-1][0] < 1:
            points.append((1, 0))
        kt = ";".join(str(p[0]) for p in points)
        vals = ";".join(str(p[1]) for p in points)

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
        label_svg += f'''    <text x="{svg_w/2}" y="{svg_h - 18}" text-anchor="middle" opacity="0"
          style="font-family:'Fira Code',monospace; font-size:14px; font-weight:600; fill:{ACCENT};">
        {proj["label"]}
        <animate attributeName="opacity" keyTimes="{kt}" values="{vals}" dur="{cycle}s" repeatCount="indefinite" calcMode="linear" />
    </text>
'''

    stand_x = svg_w / 2
    screen_bottom = SCREEN_Y + SCREEN_H + BEZEL

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {svg_w} {svg_h}" width="100%" height="{svg_h}" preserveAspectRatio="xMinYMin meet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&amp;display=swap');
    </style>
    <rect width="100%" height="100%" fill="{BG_COLOR}" rx="8" />
    <rect x="{SCREEN_X - BEZEL}" y="{SCREEN_Y - BEZEL}"
          width="{SCREEN_W + BEZEL * 2}" height="{SCREEN_H + BEZEL * 2}"
          rx="14" fill="{BEZEL_COLOR}" stroke="{BEZEL_EDGE}" stroke-width="1.5" />
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
    <rect x="{stand_x - 6}" y="{screen_bottom}" width="12" height="22" fill="{STAND_COLOR}" />
    <rect x="{stand_x - 45}" y="{screen_bottom + 22}" width="90" height="8" rx="4" fill="{STAND_COLOR}" />
{label_svg}
</svg>'''

    with open("project_monitor.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated project_monitor.svg, cycle={cycle}s")


if __name__ == "__main__":
    generate()
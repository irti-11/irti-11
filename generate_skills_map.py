import random

def tree(x, y, scale=1.0, variant=0):
    """Layered pine tree with shading for depth."""
    dark = "#2e6b1f" if variant % 2 == 0 else "#2a5f1c"
    mid = "#3d8b26"
    light = "#4fa832"
    trunk = "#5d4037"
    return f'''<g transform="translate({x},{y}) scale({scale})">
        <rect x="-3" y="18" width="6" height="8" fill="{trunk}"/>
        <ellipse cx="0" cy="27" rx="9" ry="3" fill="#000000" opacity="0.18"/>
        <polygon points="0,-18 14,10 -14,10" fill="{dark}"/>
        <polygon points="0,-18 6,10 -14,10" fill="{mid}" opacity="0.55"/>
        <polygon points="0,-6 11,16 -11,16" fill="{dark}"/>
        <polygon points="0,-6 4,16 -11,16" fill="{mid}" opacity="0.55"/>
        <polygon points="0,4 9,20 -9,20" fill="{mid}"/>
        <polygon points="0,4 3,20 -9,20" fill="{light}" opacity="0.5"/>
    </g>'''

def bush(x, y, scale=1.0):
    return f'''<g transform="translate({x},{y}) scale({scale})">
        <ellipse cx="0" cy="8" rx="12" ry="3" fill="#000000" opacity="0.15"/>
        <circle cx="-7" cy="0" r="7" fill="#3d8b26"/>
        <circle cx="7" cy="0" r="7" fill="#3d8b26"/>
        <circle cx="0" cy="-5" r="8" fill="#4fa832"/>
        <circle cx="-3" cy="-7" r="4" fill="#5cba3c" opacity="0.6"/>
    </g>'''

def fence_h(x, y, length, posts=None):
    if posts is None:
        posts = max(2, length // 18)
    g = f'<g transform="translate({x},{y})">'
    g += f'<rect x="0" y="4" width="{length}" height="3" fill="#c9a06c"/>'
    g += f'<rect x="0" y="10" width="{length}" height="3" fill="#c9a06c"/>'
    step = length / posts
    for i in range(posts + 1):
        px = i * step
        g += f'<rect x="{px-1.5}" y="0" width="3" height="16" fill="#a9784a" stroke="#5c3d20" stroke-width="0.5"/>'
    g += '</g>'
    return g

def lamp_post(x, y):
    return f'''<g transform="translate({x},{y})">
        <ellipse cx="0" cy="34" rx="6" ry="2" fill="#000000" opacity="0.2"/>
        <rect x="-2" y="0" width="4" height="32" fill="#3e3e3e"/>
        <circle cx="0" cy="-3" r="7" fill="#ffe082"/>
        <circle cx="0" cy="-3" r="7" fill="#fff59d" opacity="0.5"/>
        <path d="M -7,0 Q 0,-8 7,0" fill="none" stroke="#3e3e3e" stroke-width="2"/>
    </g>'''

def pond(x, y, rx, ry):
    return f'''<g transform="translate({x},{y})">
        <ellipse cx="0" cy="2" rx="{rx+5}" ry="{ry+5}" fill="#4e7d3a" opacity="0.4"/>
        <ellipse cx="0" cy="0" rx="{rx}" ry="{ry}" fill="#4a90c4" stroke="#2f6a99" stroke-width="2"/>
        <ellipse cx="0" cy="0" rx="{rx*0.7}" ry="{ry*0.6}" fill="#5fa3d6" opacity="0.6"/>
        <ellipse cx="{-rx*0.25}" cy="{-ry*0.2}" rx="{rx*0.35}" ry="{ry*0.18}" fill="#ffffff" opacity="0.35"/>
    </g>'''

def wall_planks(x, y, w, h, color):
    lines = ""
    for i in range(1, w // 9):
        lx = x + i * 9
        lines += f'<line x1="{lx}" y1="{y}" x2="{lx}" y2="{y+h}" stroke="#00000022" stroke-width="1"/>'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>' + lines

def shingled_gable(x0, y0, w, apex_h, roof_color, roof_dark, roof_light):
    """Pitched roof with a highlight ridge and shingle rows."""
    apex_x = x0 + w / 2
    g = f'<polygon points="{x0},{y0} {x0+w},{y0} {apex_x},{y0-apex_h}" fill="{roof_color}" stroke="#2b1a12" stroke-width="2"/>'
    g += f'<polygon points="{x0},{y0} {apex_x},{y0} {apex_x},{y0-apex_h}" fill="{roof_light}" opacity="0.35"/>'
    rows = 3
    for r in range(1, rows):
        frac = r / rows
        ry = y0 - apex_h * frac
        rx0 = x0 + (apex_x - x0) * frac
        rx1 = x0 + w - (x0 + w - apex_x) * frac
        g += f'<line x1="{rx0}" y1="{ry}" x2="{rx1}" y2="{ry}" stroke="{roof_dark}" stroke-width="1.5" opacity="0.5"/>'
    g += f'<rect x="{apex_x-2}" y="{y0-apex_h-6}" width="4" height="6" fill="{roof_dark}"/>'
    return g

def window(x, y, w=14, h=14, glow="#ffe082"):
    return f'''<g>
        <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#3e2723" stroke="#1a0f0a" stroke-width="1.5"/>
        <rect x="{x+2}" y="{y+2}" width="{w-4}" height="{h-4}" fill="{glow}"/>
        <line x1="{x+w/2}" y1="{y+2}" x2="{x+w/2}" y2="{y+h-2}" stroke="#3e2723" stroke-width="1.5"/>
        <line x1="{x+2}" y1="{y+h/2}" x2="{x+w-2}" y2="{y+h/2}" stroke="#3e2723" stroke-width="1.5"/>
    </g>'''

def door(x, y, w=22, h=28, color="#5d4037"):
    return f'''<g>
        <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" stroke="#2b1a12" stroke-width="1.5" rx="2"/>
        <rect x="{x+3}" y="{y+3}" width="{w-6}" height="{h/2-3}" fill="#4a332a" opacity="0.5"/>
        <circle cx="{x+w-6}" cy="{y+h/2+2}" r="1.6" fill="#fbc02d"/>
    </g>'''

def house(x0, y0, w, h, apex_h, roof_color, roof_dark, roof_light, wall_color, label, label_dx=0, chimney=False):
    fx = x0
    fy = y0 - h
    g = f'<g>'
    g += f'<ellipse cx="{x0+w/2}" cy="{y0+6}" rx="{w/2+8}" ry="6" fill="#000000" opacity="0.2"/>'
    g += wall_planks(fx, fy, w, h, wall_color)
    g += f'<rect x="{fx}" y="{fy}" width="{w}" height="{h}" fill="none" stroke="#2b1a12" stroke-width="2"/>'
    g += door(x0 + w/2 - 11, y0 - 28)
    g += window(fx + 8, fy + 8)
    g += window(fx + w - 22, fy + 8)
    if chimney:
        g += f'<rect x="{fx+w-16}" y="{y0-h-apex_h+4}" width="8" height="16" fill="#8d6e63" stroke="#3e2723" stroke-width="1"/>'
        g += f'<rect x="{fx+w-17}" y="{y0-h-apex_h+2}" width="10" height="4" fill="#a1887f"/>'
    g += shingled_gable(fx - 6, fy, w + 12, apex_h, roof_color, roof_dark, roof_light)
    g += f'<text x="{x0 + w/2 + label_dx}" y="{y0 - h - apex_h - 14}" text-anchor="middle" class="zone-label">{label}</text>'
    g += '</g>'
    return g


def generate_animated_skills_svg():
    svg_w, svg_h = 900, 520
    grass_color = "#7ec850"
    grass_dark = "#6ab040"
    path_color = "#e0c48c"
    path_border = "#b98f57"
    text_color = "#ffffff"

    random.seed(99)
    grass_texture = ""
    for _ in range(260):
        x = random.randint(0, svg_w)
        y = random.randint(0, svg_h)
        s = random.choice([6, 8, 10])
        grass_texture += f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{grass_dark}" opacity="0.35"/>\n'

    # ---- Border forest (frames the whole map like a village clearing) ----
    border_trees = ""
    tx = 10
    while tx < svg_w:
        border_trees += tree(tx, 14, scale=0.55, variant=tx)
        border_trees += tree(tx, svg_h - 8, scale=0.55, variant=tx + 1)
        tx += 34
    ty = 40
    while ty < svg_h - 30:
        border_trees += tree(12, ty, scale=0.5, variant=ty)
        border_trees += tree(svg_w - 12, ty, scale=0.5, variant=ty + 3)
        ty += 40

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@600&amp;display=swap');
        text {{ font-family: 'Fira Code', monospace; fill: {text_color}; font-weight: bold; }}
        .ui-box {{ fill: #111111; fill-opacity: 0.95; stroke: #fbc02d; stroke-width: 3; filter: drop-shadow(0px 6px 12px rgba(0,0,0,0.8)); }}
        .skill-text {{ font-size: 14px; fill: #ffffff; }}
        .zone-label {{ font-size: 13px; fill: #ffffff; paint-order: stroke; stroke: #000000; stroke-width: 3px; stroke-linejoin: round; }}
    </style>

    <rect width="100%" height="100%" fill="{grass_color}"/>
    <g>{grass_texture}</g>

    <!-- Main spine road -->
    <rect x="0" y="230" width="{svg_w}" height="42" fill="{path_color}" />
    <rect x="0" y="226" width="{svg_w}" height="4" fill="{path_border}" />
    <rect x="0" y="272" width="{svg_w}" height="4" fill="{path_border}" />
    <g opacity="0.5">'''

    # dashed centerline dots along main road
    dots = ""
    dxx = 10
    while dxx < svg_w:
        dots += f'<rect x="{dxx}" y="249" width="10" height="4" fill="#ffffff"/>'
        dxx += 26
    svg += dots + "</g>"

    branches = [
        (120, 160, 70), (300, 272, 90), (460, 170, 60),
        (630, 272, 60), (800, 150, 80),
    ]
    for bx, by, blen in branches:
        top = by - blen if by < 240 else 272
        h = blen
        y0 = min(by, 272)
        svg += f'<rect x="{bx-15}" y="{y0}" width="30" height="{h}" fill="{path_color}"/>'
        svg += f'<rect x="{bx-19}" y="{y0}" width="4" height="{h}" fill="{path_border}"/>'
        svg += f'<rect x="{bx+15}" y="{y0}" width="4" height="{h}" fill="{path_border}"/>'

    # decoration: pond, bushes, lamps, fences
    svg += pond(210, 430, 42, 20)
    svg += lamp_post(40, 195)
    svg += lamp_post(860, 195)
    svg += lamp_post(370, 300)
    svg += fence_h(150, 470, 90)
    svg += fence_h(650, 60, 100)
    for bxp, byp in [(150, 300), (500, 440), (700, 60), (30, 350)]:
        svg += bush(bxp, byp, 0.9)

    svg += border_trees
    # a few interior accent trees near houses
    for tx2, ty2, sc in [(180, 130, 0.7), (350, 340, 0.7), (520, 260, 0.6),
                          (670, 350, 0.7), (820, 250, 0.65), (60, 260, 0.6)]:
        svg += tree(tx2, ty2, sc, variant=int(tx2))

    # ---- Houses (same 5 zones, richer detail) ----
    svg += house(90, 155, 96, 46, 34, "#c62828", "#8e1c1c", "#ff6659", "#c9986a",
                 "LANGUAGES")
    svg += house(255, 355, 96, 50, 30, "#607d8b", "#37474f", "#90a4ae", "#c9986a",
                 "DATABASE", chimney=True)
    svg += house(415, 165, 100, 46, 32, "#1565c0", "#0d3f7a", "#5e92f3", "#d9ad7c",
                 "FRONTEND")
    svg += house(580, 345, 100, 46, 34, "#2e7d32", "#1b5e20", "#66bb6a", "#c9986a",
                 "VERSION CONTROL", chimney=True)
    svg += house(750, 140, 106, 46, 32, "#6a1b9a", "#4a0072", "#ab47bc", "#d9ad7c",
                 "TOOLS")

    # ---- Popups (unchanged content, same tech logos/skills) ----
    svg += '''
    <!-- Popup 1: Languages -->
    <g opacity="0" transform="translate(20, 20)">
        <animate attributeName="opacity" values="0; 0; 1; 1; 0; 0" keyTimes="0; 0.05; 0.06; 0.15; 0.16; 1" dur="25s" repeatCount="indefinite" />
        <rect x="0" y="0" width="250" height="100" class="ui-box" />
        <g transform="translate(15, 20)">
            <path d="M2,0 L18,0 L16,18 L10,22 L4,18 Z" fill="#E34F26"/>
            <path d="M10,2 L15,2 L14,12 L10,14 L6,12 L6,10 L10,11 L12,10 L12,5 L10,5 L6,5 Z" fill="#FFFFFF"/>
        </g>
        <text x="45" y="36" class="skill-text">HTML5</text>
        <g transform="translate(135, 20)">
            <path d="M2,0 L18,0 L16,18 L10,22 L4,18 Z" fill="#1572B6"/>
            <path d="M10,2 L15,2 L14,12 L10,14 L6,12 L6,10 L10,11 L12,10 L12,5 L10,5 L6,5 Z" fill="#FFFFFF"/>
        </g>
        <text x="165" y="36" class="skill-text">CSS3</text>
        <g transform="translate(15, 60)">
            <rect width="20" height="20" rx="3" fill="#F7DF1E"/>
            <text x="3" y="15" font-family="Arial" font-weight="bold" font-size="12" fill="#000000">JS</text>
        </g>
        <text x="45" y="76" class="skill-text">JavaScript</text>
        <g transform="translate(135, 60)">
            <ellipse cx="10" cy="10" rx="12" ry="7" fill="#777BB4"/>
            <text x="1" y="14" font-family="Arial" font-weight="bold" font-size="10" fill="#FFFFFF">php</text>
        </g>
        <text x="165" y="76" class="skill-text">PHP</text>
    </g>

    <!-- Popup 2: Database -->
    <g opacity="0" transform="translate(155, 400)">
        <animate attributeName="opacity" values="0; 0; 1; 1; 0; 0" keyTimes="0; 0.24; 0.25; 0.33; 0.34; 1" dur="25s" repeatCount="indefinite" />
        <rect x="0" y="0" width="150" height="55" class="ui-box" />
        <g transform="translate(15, 17)">
            <ellipse cx="10" cy="4" rx="10" ry="4" fill="#00758F"/>
            <rect x="0" y="4" width="20" height="10" fill="#00758F"/>
            <ellipse cx="10" cy="14" rx="10" ry="4" fill="#0097A7"/>
        </g>
        <text x="45" y="33" class="skill-text">MySQL</text>
    </g>

    <!-- Popup 3: Frontend -->
    <g opacity="0" transform="translate(370, 20)">
        <animate attributeName="opacity" values="0; 0; 1; 1; 0; 0" keyTimes="0; 0.42; 0.43; 0.52; 0.53; 1" dur="25s" repeatCount="indefinite" />
        <rect x="0" y="0" width="240" height="55" class="ui-box" />
        <g transform="translate(15, 17)">
            <rect x="0" y="2" width="14" height="12" rx="2" fill="none" stroke="#00C4CC" stroke-width="2"/>
            <rect x="12" y="8" width="8" height="10" rx="1" fill="#111111" stroke="#E34F26" stroke-width="2"/>
        </g>
        <text x="45" y="33" class="skill-text">Responsive Design</text>
    </g>

    <!-- Popup 4: Version Control -->
    <g opacity="0" transform="translate(500, 420)">
        <animate attributeName="opacity" values="0; 0; 1; 1; 0; 0" keyTimes="0; 0.61; 0.62; 0.71; 0.72; 1" dur="25s" repeatCount="indefinite" />
        <rect x="0" y="0" width="210" height="55" class="ui-box" />
        <g transform="translate(15, 17)">
            <path d="M10,0 L20,10 L10,20 L0,10 Z" fill="#F05032"/>
            <circle cx="10" cy="5" r="2" fill="#FFFFFF"/>
            <circle cx="15" cy="10" r="2" fill="#FFFFFF"/>
            <circle cx="10" cy="15" r="2" fill="#FFFFFF"/>
            <path d="M10,7 L10,13 M10,13 L15,10" stroke="#FFFFFF" stroke-width="2"/>
        </g>
        <text x="45" y="33" class="skill-text">Git</text>
        <g transform="translate(115, 17)">
            <circle cx="10" cy="10" r="10" fill="#FFFFFF"/>
            <path d="M10,2 C5.5,2 2,5.5 2,10 C2,13.5 4.3,16.5 7.4,17.6 C7.8,17.7 7.9,17.4 7.9,17.2 C7.9,16.8 7.9,15.8 7.9,14.6 C5.6,15.1 5.2,13.5 5.2,13.5 C4.8,12.6 4.3,12.3 4.3,12.3 C3.6,11.8 4.4,11.8 4.4,11.8 C5.2,11.9 5.6,12.6 5.6,12.6 C6.4,14 7.6,13.6 8,13.4 C8.1,12.9 8.3,12.5 8.5,12.3 C6.7,12.1 4.7,11.4 4.7,8.2 C4.7,7.3 5,6.6 5.5,6 C5.4,5.8 5.1,4.9 5.6,3.8 C5.6,3.8 6.3,3.6 7.9,4.7 C8.6,4.5 9.3,4.4 10,4.4 C10.7,4.4 11.4,4.5 12.1,4.7 C13.7,3.6 14.4,3.8 14.4,3.8 C14.9,4.9 14.6,5.8 14.5,6 C15,6.6 15.3,7.3 15.3,8.2 C15.3,11.4 13.4,12.1 11.5,12.3 C11.8,12.6 12,13.1 12,13.9 C12,15 12,15.9 12,16.2 C12,16.5 12.2,16.8 12.6,16.7 C15.7,15.6 18,12.6 18,9 C18,4.5 14.4,1 10,1 Z" fill="#181717"/>
        </g>
        <text x="145" y="33" class="skill-text">GitHub</text>
    </g>

    <!-- Popup 5: Tools -->
    <g opacity="0" transform="translate(620, 10)">
        <animate attributeName="opacity" values="0; 0; 1; 1; 0; 0" keyTimes="0; 0.80; 0.81; 0.90; 0.91; 1" dur="25s" repeatCount="indefinite" />
        <rect x="0" y="0" width="240" height="100" class="ui-box" />
        <g transform="translate(15, 20)">
            <path d="M14,2 L18,5 L18,15 L14,18 L3,10 Z" fill="#007ACC"/>
            <path d="M14,2 L3,10 L8,12 Z" fill="#00599C"/>
            <path d="M14,18 L3,10 L8,8 Z" fill="#00599C"/>
        </g>
        <text x="45" y="36" class="skill-text">VS Code</text>
        <g transform="translate(145, 20)">
            <circle cx="10" cy="10" r="10" fill="#FB7A24"/>
            <path d="M6,6 L14,14 M14,6 L6,14" stroke="#FFFFFF" stroke-width="3"/>
        </g>
        <text x="175" y="36" class="skill-text">XAMPP</text>
        <g transform="translate(15, 60)">
            <circle cx="7" cy="5" r="4" fill="#F24E1E"/>
            <circle cx="14" cy="5" r="4" fill="#FF7262"/>
            <circle cx="7" cy="11" r="4" fill="#A259FF"/>
            <circle cx="14" cy="11" r="4" fill="#1ABCFE"/>
            <circle cx="7" cy="17" r="4" fill="#0ACF83"/>
        </g>
        <text x="45" y="76" class="skill-text">Figma</text>
        <g transform="translate(145, 60)">
            <circle cx="10" cy="10" r="10" fill="#00C4CC"/>
            <text x="4" y="15" font-family="Arial" font-weight="bold" font-size="14" fill="#FFFFFF">C</text>
        </g>
        <text x="175" y="76" class="skill-text">Canva</text>
    </g>
    '''

    # ---- Animated character with richer shading/detail ----
    svg += '''
    <g>
        <animateTransform attributeName="transform" type="translate"
            values="
                -30,215; 135,215; 135,140; 135,140; 135,215;
                295,215; 295,355; 295,355; 295,215;
                455,215; 455,150; 455,150; 455,215;
                615,215; 615,335; 615,335; 615,215;
                785,215; 785,130; 785,130; 785,215; 930,215
            "
            keyTimes="
                0; 0.04; 0.06; 0.15; 0.17; 0.21; 0.24; 0.33; 0.36;
                0.40; 0.43; 0.52; 0.55; 0.59; 0.62; 0.71; 0.74; 0.78;
                0.81; 0.90; 0.93; 1
            "
            dur="25s" repeatCount="indefinite" />

        <g transform="scale(2.2)" image-rendering="pixelated">
            <ellipse cx="7" cy="23" rx="7" ry="1.6" fill="#000000" opacity="0.25"/>
            <rect x="3" y="0" width="10" height="2" fill="#1a1a1a"/>
            <rect x="1" y="2" width="13" height="4" fill="#1a1a1a"/>
            <rect x="2" y="2" width="4" height="2" fill="#3a3a3a"/>
            <rect x="1" y="6" width="3" height="3" fill="#1a1a1a"/>
            <rect x="12" y="6" width="2" height="3" fill="#1a1a1a"/>
            <rect x="4" y="6" width="8" height="7" fill="#f5b591"/>
            <rect x="2" y="9" width="2" height="2" fill="#f5b591"/>
            <rect x="7" y="8" width="1" height="2" fill="#1a1a1a"/>
            <rect x="11" y="8" width="1" height="2" fill="#1a1a1a"/>
            <rect x="8" y="11" width="3" height="1" fill="#c98868"/>
            <rect x="1" y="13" width="13" height="5" fill="#37474f"/>
            <rect x="1" y="13" width="4" height="5" fill="#2c3a40"/>
            <rect x="1" y="15" width="2" height="3" fill="#37474f"/>
            <rect x="12" y="15" width="2" height="3" fill="#37474f"/>
            <rect x="1" y="18" width="2" height="1" fill="#f5b591"/>
            <rect x="6" y="13" width="3" height="4" fill="#ffffff"/>
            <rect x="7" y="14" width="1" height="3" fill="#c8ff57"/>
            <rect x="3" y="18" width="9" height="4" fill="#616161"/>
            <rect x="3" y="18" width="9" height="1.5" fill="#757575"/>
            <rect x="3" y="22" width="3" height="1" fill="#1a1a1a"/>
            <rect x="9" y="22" width="3" height="1" fill="#1a1a1a"/>
        </g>
    </g>
    '''

    svg += '</svg>'

    with open("skills_map_v2.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Generated: skills_map_v2.svg (detailed RPG village with shingled roofs, trees, fences, pond, lamps)")


if __name__ == "__main__":
    generate_animated_skills_svg()
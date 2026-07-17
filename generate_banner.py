import random
import os
import html

# --- NEON TERMINAL PALETTE ---
BG_COLOR = "#000000"
COLOR_CYAN = "#78dec7"
COLOR_PINK = "#f2a6c3"
COLOR_GREEN = "#aef3a4"
COLOR_WHITE = "#e2e8f0"

def load_random_ascii():
    folder_name = "ascii_art"
    if not os.path.exists(folder_name): os.makedirs(folder_name)
    art_files = [f for f in os.listdir(folder_name) if f.endswith(".txt")]
    if not art_files: return ["  [!] No art in /ascii_art/"]
    chosen_file = random.choice(art_files)
    with open(os.path.join(folder_name, chosen_file), "r", encoding="utf-8") as f:
        return f.read().splitlines()

def generate_svg():
    chosen_art = load_random_ascii()
    
    padding = 10
    available_w = 420 - (padding * 2)
    available_h = 302 - (padding * 2)
    
    num_lines = len(chosen_art) if len(chosen_art) > 0 else 1
    max_len = max([len(line) for line in chosen_art] + [1])
    
    font_w = available_w / (max_len * 0.55) 
    font_h = available_h / (num_lines * 1.1)
    ascii_font_size = min(font_w, font_h, 16)
    line_height = ascii_font_size * 1.1

    bio_lines = [
        {"label": "👤 USER", "val": "irti-11 (Syed Irtiza Ali)"},
        {"label": "🎓 DEPT", "val": "Computer Systems Engineering"},
        {"label": "🏫 CAMPUS", "val": "Dawood UET"},
        {"label": "📍 LOCATION", "val": "Karachi, Pakistan"},
        {"label": "🛠️ STACK", "val": "[ C++ | Python | PHP | MySQL ]"}
    ]

    svg_width, svg_height = 850, 340 
    
    # Typing speed constant
    type_duration = 0.8 

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&amp;display=swap');
        .bg {{ fill: {BG_COLOR}; }}
        text {{ font-family: 'Fira Code', monospace; fill: {COLOR_WHITE}; }}
        .label {{ font-weight: 600; fill: {COLOR_PINK}; font-size: 14px; }}
        .val {{ fill: {COLOR_WHITE}; font-size: 14px; }}
        .stack-val {{ fill: {COLOR_GREEN}; font-weight: 600; font-size: 14px; }}
        .cursor {{ fill: {COLOR_CYAN}; font-weight: bold; font-size: 16px; }}
        @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
        .blink {{ animation: blink 1s step-end infinite; }}
    </style>
    <rect width="100%" height="100%" class="bg" rx="8"/>
    <text x="25" y="24" style="fill:#6272a4; font-size:12px;">session: sys_fetch@irti-11</text>
    <line x1="0" y1="38" x2="{svg_width}" y2="38" style="stroke:#1e222a; stroke-width:1;" />
    <line x1="420" y1="38" x2="420" y2="{svg_height}" style="stroke:#1e222a; stroke-width:1;" />

    <svg x="{padding}" y="{38 + padding}" width="{available_w}" height="{available_h}">
        <g style="font-size: {ascii_font_size:.2f}px; fill: {COLOR_CYAN};">
'''
    y_offset = ascii_font_size
    for line in chosen_art:
        svg += f'            <text x="0" y="{y_offset:.2f}" style="white-space: pre;">{html.escape(line)}</text>\n'
        y_offset += line_height

    svg += f'''        </g>
        <rect x="0" y="0" width="{available_w}" height="{available_h}" fill="{BG_COLOR}">
            <animate attributeName="height" from="{available_h}" to="0" dur="1.5s" fill="freeze" />
        </rect>
    </svg>
'''

    bio_y = 100
    for idx, item in enumerate(bio_lines):
        delay = 1.5 + (idx * 0.8)
        text_width = len(item["val"]) * 9 
        
        svg += f'''        <g>
            <text x="450" y="{bio_y}" class="label">{item["label"]}</text>
            
            <g clip-path="url(#mask{idx})">
                <text x="560" y="{bio_y}" class="{"stack-val" if "STACK" in item["label"] else "val"}">{item["val"]}</text>
            </g>
            
            <!-- Persistent Cursor that glides -->
            <text x="560" y="{bio_y}" class="cursor blink">
                <animate attributeName="x" from="560" to="{560 + text_width}" begin="{delay}s" dur="{type_duration}s" fill="freeze" />
                <!-- This forces the cursor to be hidden after the animation ends -->
                <animate attributeName="visibility" from="visible" to="hidden" begin="{delay + type_duration}s" dur="0.1s" fill="freeze" />
                |
            </text>
        </g>
        
        <clipPath id="mask{idx}">
            <rect x="560" y="{bio_y - 20}" width="0" height="30">
                <animate attributeName="width" from="0" to="{text_width + 10}" begin="{delay}s" dur="{type_duration}s" fill="freeze" />
            </rect>
        </clipPath>
'''
        bio_y += 45

    svg += '</svg>'
    
    with open("terminal_banner.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("✨ Generated: Gliding cursor that persists after typing.")

if __name__ == "__main__":
    generate_svg()
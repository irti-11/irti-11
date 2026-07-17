import random
import os
import html

# --- NEON TERMINAL PALETTE ---
BG_COLOR = "#0c0f12"
COLOR_CYAN = "#78dec7"
COLOR_PINK = "#f2a6c3"
COLOR_GREEN = "#aef3a4"
COLOR_WHITE = "#e2e8f0"

def load_random_ascii():
    folder_name = "ascii_art"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    art_files = [f for f in os.listdir(folder_name) if f.endswith(".txt")]
    
    if not art_files:
        return ["  [!] Drop your .txt art files into /ascii_art/"]
        
    chosen_file = random.choice(art_files)
    file_path = os.path.join(folder_name, chosen_file)
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().splitlines()

def generate_svg():
    chosen_art = load_random_ascii()
    
    # --- AUTO-SCALING ALGORITHM ---
    num_lines = len(chosen_art) if len(chosen_art) > 0 else 1
    max_len = max([len(line) for line in chosen_art] + [1])
    
    # We force the font to scale down to fit the 400px width of the left pane
    font_w = 400 / (max_len * 0.6) 
    font_h = 290 / (num_lines * 1.2)
    ascii_font_size = min(font_w, font_h, 14) # Caps at 14px 
    line_height = ascii_font_size * 1.2

    # --- YOUR SYSTEM CREDENTIALS ---
    bio_lines = [
        {"label": "👤 USER", "val": "irti-11 (Syed Irtiza Ali)"},
        {"label": "🎓 DEPT", "val": "Computer Systems Engineering"},
        {"label": "🏫 CAMPUS", "val": "Dawood UET"},
        {"label": "📍 LOCATION", "val": "Karachi, Pakistan"},
        {"label": "🛠️ STACK", "val": "[ C++ | Python | PHP | MySQL ]"}
    ]

    svg_width = 850
    svg_height = 340 

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&amp;display=swap');
        
        .bg {{ fill: {BG_COLOR}; }}
        text {{ font-family: 'Fira Code', monospace; fill: {COLOR_WHITE}; }}
        
        /* Terminal UI Styles */
        .dot {{ rx: 5; ry: 5; }}
        .dot-red {{ fill: #ff5f56; }}
        .dot-yellow {{ fill: #ffbd2e; }}
        .dot-green {{ fill: #27c93f; }}
        .window-title {{ fill: #6272a4; font-size: 12px; }}
        .divider {{ stroke: #1e222a; stroke-width: 1; }}

        .label {{ font-weight: 600; fill: {COLOR_PINK}; font-size: 14px; }}
        .arrow {{ fill: {COLOR_CYAN}; font-size: 14px; }}
        .val {{ fill: {COLOR_WHITE}; font-size: 14px; }}
        .stack-val {{ fill: {COLOR_GREEN}; font-weight: 600; font-size: 14px; }}
    </style>

    <!-- Background Frame -->
    <rect width="100%" height="100%" class="bg" rx="8"/>

    <!-- Terminal Window Bar -->
    <circle cx="25" cy="20" r="6" class="dot dot-red"/>
    <circle cx="45" cy="20" r="6" class="dot dot-yellow"/>
    <circle cx="65" cy="20" r="6" class="dot dot-green"/>
    <text x="90" y="24" class="window-title">session: sys_fetch@irti-11</text>
    <line x1="0" y1="38" x2="{svg_width}" y2="38" class="divider" />
    <line x1="420" y1="38" x2="420" y2="{svg_height}" class="divider" />

    <!-- LEFT PANE: Nested SVG acts as an unbreakable wall so art NEVER bleeds right -->
    <svg x="0" y="38" width="420" height="302">
        <g style="font-size: {ascii_font_size:.2f}px; fill: {COLOR_CYAN};">
'''

    y_offset = 15 + ascii_font_size
    for line in chosen_art:
        escaped_line = html.escape(line)
        svg += f'            <text x="15" y="{y_offset:.2f}" style="white-space: pre;">{escaped_line}</text>\n'
        y_offset += line_height

    svg += f'''        </g>
        <!-- PRINTER ANIMATION: A solid block sliding downwards to reveal the text -->
        <rect x="0" y="0" width="420" height="302" fill="{BG_COLOR}">
            <animate attributeName="y" from="0" to="302" dur="2s" fill="freeze" />
            <animate attributeName="height" from="302" to="0" dur="2s" fill="freeze" />
        </rect>
    </svg>

    <!-- RIGHT PANE: System Information Output -->
    <g id="bio-group">
'''

    bio_y = 95
    base_delay = 2.0  # Waits exactly 2 seconds for the printer animation to finish
    
    for idx, item in enumerate(bio_lines):
        val_class = "stack-val" if "STACK" in item["label"] else "val"
        delay = base_delay + (idx * 0.7) # Each line types out 0.7 seconds after the previous
        
        svg += f'''        <g>
            <text x="450" y="{bio_y}" class="label">{item["label"]}</text>
            <text x="530" y="{bio_y}" class="arrow">➔</text>
            <text x="555" y="{bio_y}" class="{val_class}">{item["val"]}</text>
        </g>
        <!-- TYPEWRITER ANIMATION: Blocks sliding to the right to reveal text stroke-by-stroke -->
        <rect x="440" y="{bio_y - 15}" width="400" height="25" fill="{BG_COLOR}">
            <animate attributeName="x" from="440" to="850" begin="{delay}s" dur="0.6s" fill="freeze" />
            <animate attributeName="width" from="400" to="0" begin="{delay}s" dur="0.6s" fill="freeze" />
        </rect>
'''
        bio_y += 45

    svg += '''    </g>
</svg>
'''
    
    with open("terminal_banner.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("✨ Engine upgraded: Hard boundaries and Native SVG Animations applied.")

if __name__ == "__main__":
    generate_svg()
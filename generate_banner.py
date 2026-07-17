import random
import os
import html

# --- NEON TERMINAL PALETTE ---
BG_COLOR = "#0c0f12"
COLOR_CYAN = "#78dec7"
COLOR_PINK = "#f2a6c3"
COLOR_PEACH = "#ffd09b"
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
    
    # --- AUTO-SCALING ALGORITHM FOR ASCII ---
    num_lines = len(chosen_art)
    if num_lines == 0: num_lines = 1
    max_len = max([len(line) for line in chosen_art] + [1])
    
    # Strict bounding box dimensions for the left pane
    max_box_width = 380 
    max_box_height = 290
    
    # Calculate the maximum possible font size that fits both horizontally and vertically
    font_w = max_box_width / (max_len * 0.6) # 0.6 is the average width ratio of monospace chars
    font_h = max_box_height / (num_lines * 1.15) 
    
    # Select the smallest constraint, capping at 14px so small art doesn't look huge
    ascii_font_size = min(font_w, font_h, 14)
    line_height = ascii_font_size * 1.15
    
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

    # --- DYNAMIC SVG MASKS (CLIP-PATHS) FOR ANIMATION ---
    defs = f'''<defs>
        <clipPath id="ascii-clip">
            <rect x="0" y="38" class="print-rect"/>
        </clipPath>
    '''
    
    # Generate sequential typewriter masks for each bio line
    for idx in range(len(bio_lines)):
        delay = 1.2 + (idx * 0.5) # Waits 1.2s for the printer to finish, then chains the typing
        defs += f'''    <clipPath id="bio-clip-{idx}">
            <rect x="440" y="{70 + (idx * 45)}" height="40" class="type-rect" style="animation-delay: {delay}s;"/>
        </clipPath>
    '''
    defs += "</defs>"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
    {defs}
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&amp;display=swap');
        
        .bg {{ fill: {BG_COLOR}; }}
        text {{
            font-family: 'Fira Code', monospace;
            font-size: 14px; 
            fill: {COLOR_WHITE};
        }}
        
        /* Terminal UI Styles */
        .dot {{ rx: 5; ry: 5; }}
        .dot-red {{ fill: #ff5f56; }}
        .dot-yellow {{ fill: #ffbd2e; }}
        .dot-green {{ fill: #27c93f; }}
        .window-title {{ fill: #6272a4; font-size: 12px; }}
        .divider {{ stroke: #1e222a; stroke-width: 1; }}

        /* 1. Printer Animation Keyframes */
        @keyframes printDown {{
            0% {{ height: 0; }}
            100% {{ height: 310px; }}
        }}
        .print-rect {{
            width: 420px;
            height: 0;
            /* steps() forces it to reveal exactly one text line at a time */
            animation: printDown 1.2s steps({num_lines}, end) forwards;
        }}

        /* 2. Typewriter Animation Keyframes */
        @keyframes typeLine {{
            0% {{ width: 0; }}
            100% {{ width: 400px; }}
        }}
        .type-rect {{
            width: 0;
            /* steps() simulates individual keystrokes */
            animation: typeLine 0.5s steps(40, end) forwards;
        }}
        
        .label {{ font-weight: 600; fill: {COLOR_PINK}; }}
        .arrow {{ fill: {COLOR_CYAN}; }}
        .val {{ fill: {COLOR_WHITE}; }}
        .stack-val {{ fill: {COLOR_GREEN}; font-weight: 600; }}
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

    <!-- LEFT PANE: Auto-Scaling Printer Output -->
    <g id="ascii-group" clip-path="url(#ascii-clip)" style="font-size: {ascii_font_size:.2f}px;">
    '''

    y_offset = 45 + line_height
    for line in chosen_art:
        escaped_line = html.escape(line)
        svg += f'    <text x="15" y="{y_offset:.2f}" style="fill: {COLOR_CYAN}; white-space: pre;">{escaped_line}</text>\n'
        y_offset += line_height

    svg += '    </g>\n\n    <!-- RIGHT PANE: Sequenced Typewriter Bio -->\n    <g id="bio-group">\n'

    bio_y = 95
    for idx, item in enumerate(bio_lines):
        val_class = "stack-val" if "STACK" in item["label"] else "val"
        
        # Wrapping each text line in its own timed clip-path mask
        svg += f'''        <g clip-path="url(#bio-clip-{idx})">
            <text x="450" y="{bio_y}" class="label">{item["label"]}</text>
            <text x="530" y="{bio_y}" class="arrow">➔</text>
            <text x="555" y="{bio_y}" class="{val_class}">{item["val"]}</text>
        </g>\n'''
        bio_y += 45

    svg += '''    </g>
</svg>
'''
    
    with open("terminal_banner.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("✨ Upgraded generating engine: Scaling + Typewriter Masks applied.")

if __name__ == "__main__":
    generate_svg()
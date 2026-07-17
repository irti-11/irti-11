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
        text {{
            font-family: 'Fira Code', monospace;
            font-size: 13px; 
            fill: {COLOR_WHITE};
        }}
        
        /* Terminal UI Styles */
        .dot {{ rx: 5; ry: 5; }}
        .dot-red {{ fill: #ff5f56; }}
        .dot-yellow {{ fill: #ffbd2e; }}
        .dot-green {{ fill: #27c93f; }}
        .window-title {{ fill: #6272a4; font-size: 12px; }}
        .divider {{ stroke: #1e222a; stroke-width: 1; }}

        /* Cascading Animation Rules */
        .ascii-line {{
            opacity: 0;
            animation: fadeInLine 0.3s ease-out forwards;
        }}
        
        .label {{ font-weight: 600; fill: {COLOR_PINK}; }}
        .arrow {{ fill: {COLOR_CYAN}; }}
        .val {{ fill: {COLOR_WHITE}; }}
        .stack-val {{ fill: {COLOR_GREEN}; font-weight: 600; }}

        @keyframes fadeInLine {{
            to {{ opacity: 1; }}
        }}
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

    <!-- LEFT PANE: Dynamic Text Art Rendering -->
    <g id="ascii-group">
    '''

    y_offset = 75
    for i, line in enumerate(chosen_art):
        escaped_line = html.escape(line)
        delay = i * 0.08  
        
        svg += f'    <text x="25" y="{y_offset}" class="ascii-line" style="animation-delay: {delay:.2f}s; fill: {COLOR_CYAN}; white-space: pre;">{escaped_line}</text>\n'
        y_offset += 18
        if y_offset > (svg_height - 20): 
            break

    svg += '    </g>\n\n    <!-- RIGHT PANE: System Information Output -->\n    <g id="bio-group">\n'

    bio_y = 95
    base_delay = min(len(chosen_art) * 0.06, 1.2) 
    
    for idx, item in enumerate(bio_lines):
        item_delay = base_delay + (idx * 0.2)
        val_class = "stack-val" if "STACK" in item["label"] else "val"
        
        svg += f'''        <g class="ascii-line" style="animation-delay: {item_delay:.2f}s;">
            <text x="450" y="{bio_y}" class="label">{item["label"]}</text>
            <text x="530" y="{bio_y}" class="arrow">➔</text>
            <text x="555" y="{bio_y}" class="{val_class}">{item["val"]}</text>
        </g>\n'''
        bio_y += 38

    svg += '''    </g>
</svg>
'''
    
    with open("terminal_banner.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("✨ Generated terminal_banner.svg successfully.")

if __name__ == "__main__":
    generate_svg()
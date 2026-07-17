def generate_animated_skills_svg():
    svg_w, svg_h = 850, 480
    
    # Environment Palette
    grass_color = "#7ec850"
    grass_dark = "#6ab040"
    path_color = "#e2b270"
    path_border = "#c3904e"
    house_wood = "#d9ad7c"
    chest_color = "#8d6e63"
    chest_lock = "#fbc02d"
    text_color = "#ffffff"

    # Generate pixel grass textures
    grass_texture = ""
    import random
    random.seed(99) 
    for _ in range(200):
        x = random.randint(0, svg_w)
        y = random.randint(0, svg_h)
        grass_texture += f'<rect x="{x}" y="{y}" width="12" height="12" fill="{grass_dark}" opacity="0.5"/>\n'

    # Core SVG Structure
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@600&amp;display=swap');
        text {{ font-family: 'Fira Code', monospace; fill: {text_color}; font-weight: bold; image-rendering: pixelated; }}
        .ui-box {{ fill: #111111; fill-opacity: 0.95; stroke: #fbc02d; stroke-width: 3; rx: 8; filter: drop-shadow(0px 6px 12px rgba(0,0,0,0.8)); }}
        .skill-text {{ font-size: 14px; fill: #ffffff; }}
        .zone-label {{ font-size: 13px; fill: #ffffff; text-shadow: 1px 1px 0px #000, -1px -1px 0px #000, 1px -1px 0px #000, -1px 1px 0px #000; }}
        .db-label {{ font-size: 13px; fill: #ffffff; text-shadow: 1px 1px 0px #000, -1px -1px 0px #000, 1px -1px 0px #000, -1px 1px 0px #000; }}
    </style>
    
    <!-- Background Grass -->
    <rect width="100%" height="100%" fill="{grass_color}"/>
    <g>{grass_texture}</g>

    <!-- Winding Dirt Paths -->
    <!-- Main Spine Road -->
    <rect x="0" y="220" width="{svg_w}" height="40" fill="{path_color}" />
    <rect x="0" y="216" width="{svg_w}" height="4" fill="{path_border}" />
    <rect x="0" y="260" width="{svg_w}" height="4" fill="{path_border}" />
    
    <!-- Path UP to House 1: Languages -->
    <rect x="110" y="150" width="30" height="70" fill="{path_color}" />
    <rect x="106" y="150" width="4" height="70" fill="{path_border}" />
    <rect x="140" y="150" width="4" height="70" fill="{path_border}" />

    <!-- Path DOWN to House 2: Database -->
    <rect x="270" y="260" width="30" height="80" fill="{path_color}" />
    <rect x="266" y="260" width="4" height="80" fill="{path_border}" />
    <rect x="300" y="260" width="4" height="80" fill="{path_border}" />

    <!-- Path UP to House 3: Frontend -->
    <rect x="430" y="160" width="30" height="60" fill="{path_color}" />
    <rect x="426" y="160" width="4" height="60" fill="{path_border}" />
    <rect x="460" y="160" width="4" height="60" fill="{path_border}" />

    <!-- Path DOWN to House 4: Version Control -->
    <rect x="590" y="260" width="30" height="60" fill="{path_color}" />
    <rect x="586" y="260" width="4" height="60" fill="{path_border}" />
    <rect x="620" y="260" width="4" height="60" fill="{path_border}" />

    <!-- Path UP to House 5: Tools -->
    <rect x="740" y="140" width="30" height="80" fill="{path_color}" />
    <rect x="736" y="140" width="4" height="80" fill="{path_border}" />
    <rect x="770" y="140" width="4" height="80" fill="{path_border}" />


    <!-- STAGGERED VILLAGE BUILDINGS -->

    <!-- House 1: LANGUAGES (Top Left, Pitched Red Roof) -->
    <g transform="translate(85, 80)">
        <rect x="10" y="30" width="80" height="40" fill="{house_wood}" stroke="#3e2723" stroke-width="2"/>
        <rect x="25" y="45" width="30" height="25" fill="#5d4037" />
        <rect x="30" y="0" width="40" height="10" fill="#d32f2f" />
        <rect x="20" y="10" width="60" height="10" fill="#d32f2f" />
        <rect x="10" y="20" width="80" height="10" fill="#d32f2f" />
        <rect x="0"  y="30" width="100" height="10" fill="#d32f2f" />
        <rect x="30" y="60" width="20" height="14" fill="{chest_color}" rx="2" stroke="#3e2723" stroke-width="1"/>
        <rect x="38" y="65" width="4" height="4" fill="{chest_lock}" />
        <text x="15" y="-10" class="zone-label">LANGUAGES</text>
    </g>

    <!-- House 2: DATABASE (Bottom Left, Flat Fortified Grey Roof) -->
    <g transform="translate(245, 340)">
        <rect x="10" y="20" width="80" height="50" fill="{house_wood}" stroke="#3e2723" stroke-width="2"/>
        <rect x="25" y="20" width="30" height="25" fill="#5d4037" />
        <rect x="5" y="10" width="90" height="10" fill="#607d8b" />
        <rect x="5" y="0" width="15" height="10" fill="#607d8b" />
        <rect x="42" y="0" width="15" height="10" fill="#607d8b" />
        <rect x="80" y="0" width="15" height="10" fill="#607d8b" />
        <rect x="30" y="10" width="20" height="14" fill="{chest_color}" rx="2" stroke="#3e2723" stroke-width="1"/>
        <rect x="38" y="15" width="4" height="4" fill="{chest_lock}" />
        <text x="18" y="-10" class="db-label">DATABASE</text>
    </g>

    <!-- House 3: FRONTEND (Top Middle, Slanted Blue Roof) -->
    <g transform="translate(405, 90)">
        <rect x="10" y="30" width="80" height="40" fill="{house_wood}" stroke="#3e2723" stroke-width="2"/>
        <rect x="25" y="45" width="30" height="25" fill="#5d4037" />
        <polygon points="10,30 90,30 90,0 40,0" fill="#1976d2" stroke="#0d47a1" stroke-width="2"/>
        <rect x="30" y="60" width="20" height="14" fill="{chest_color}" rx="2" stroke="#3e2723" stroke-width="1"/>
        <rect x="38" y="65" width="4" height="4" fill="{chest_lock}" />
        <text x="20" y="-10" class="zone-label">FRONTEND</text>
    </g>

    <!-- House 4: VERSION CONTROL (Bottom Right, A-Frame Green Roof) -->
    <g transform="translate(565, 320)">
        <rect x="10" y="30" width="80" height="40" fill="{house_wood}" stroke="#3e2723" stroke-width="2"/>
        <rect x="25" y="30" width="30" height="25" fill="#5d4037" />
        <polygon points="0,30 100,30 50,0" fill="#2e7d32" stroke="#1b5e20" stroke-width="2"/>
        <rect x="30" y="20" width="20" height="14" fill="{chest_color}" rx="2" stroke="#3e2723" stroke-width="1"/>
        <rect x="38" y="25" width="4" height="4" fill="{chest_lock}" />
        <text x="-2" y="-10" class="zone-label">VERSION CONTROL</text>
    </g>

    <!-- House 5: TOOLS (Top Right, Double-Wide Purple Roof) -->
    <g transform="translate(715, 70)">
        <rect x="0" y="30" width="90" height="40" fill="{house_wood}" stroke="#3e2723" stroke-width="2"/>
        <rect x="25" y="45" width="30" height="25" fill="#5d4037" />
        <rect x="-10" y="15" width="110" height="15" fill="#7b1fa2" />
        <rect x="0" y="0" width="90" height="15" fill="#7b1fa2" />
        <rect x="30" y="60" width="20" height="14" fill="{chest_color}" rx="2" stroke="#3e2723" stroke-width="1"/>
        <rect x="38" y="65" width="4" height="4" fill="{chest_lock}" />
        <text x="25" y="-10" class="zone-label">TOOLS</text>
    </g>


    <!-- DYNAMIC POPUPS WITH REAL VECTOR LOGOS -->
    
    <!-- Popup 1: Languages -->
    <g opacity="0" transform="translate(20, 20)">
        <animate attributeName="opacity" values="0; 0; 1; 1; 0; 0" keyTimes="0; 0.05; 0.06; 0.15; 0.16; 1" dur="25s" repeatCount="indefinite" />
        <rect x="0" y="0" width="250" height="100" class="ui-box" />
        <!-- HTML5 SVG -->
        <g transform="translate(15, 20)">
            <path d="M2,0 L18,0 L16,18 L10,22 L4,18 Z" fill="#E34F26"/>
            <path d="M10,2 L15,2 L14,12 L10,14 L6,12 L6,10 L10,11 L12,10 L12,5 L10,5 L6,5 Z" fill="#FFFFFF"/>
        </g>
        <text x="45" y="36" class="skill-text">HTML5</text>
        <!-- CSS3 SVG -->
        <g transform="translate(135, 20)">
            <path d="M2,0 L18,0 L16,18 L10,22 L4,18 Z" fill="#1572B6"/>
            <path d="M10,2 L15,2 L14,12 L10,14 L6,12 L6,10 L10,11 L12,10 L12,5 L10,5 L6,5 Z" fill="#FFFFFF"/>
        </g>
        <text x="165" y="36" class="skill-text">CSS3</text>
        <!-- JS SVG -->
        <g transform="translate(15, 60)">
            <rect width="20" height="20" rx="3" fill="#F7DF1E"/>
            <text x="3" y="15" font-family="Arial" font-weight="bold" font-size="12" fill="#000000">JS</text>
        </g>
        <text x="45" y="76" class="skill-text">JavaScript</text>
        <!-- PHP SVG -->
        <g transform="translate(135, 60)">
            <ellipse cx="10" cy="10" rx="12" ry="7" fill="#777BB4"/>
            <text x="1" y="14" font-family="Arial" font-weight="bold" font-size="10" fill="#FFFFFF">php</text>
        </g>
        <text x="165" y="76" class="skill-text">PHP</text>
    </g>

    <!-- Popup 2: Database -->
    <g opacity="0" transform="translate(110, 390)">
        <animate attributeName="opacity" values="0; 0; 1; 1; 0; 0" keyTimes="0; 0.23; 0.24; 0.33; 0.34; 1" dur="25s" repeatCount="indefinite" />
        <rect x="0" y="0" width="130" height="55" class="ui-box" />
        <!-- MySQL SVG Abstraction -->
        <g transform="translate(15, 17)">
            <path d="M2,10 Q10,20 18,10 Q10,0 2,10 Z" fill="#4479A1"/>
            <text x="3" y="13" font-family="Arial" font-weight="bold" font-size="7" fill="#FFFFFF">SQL</text>
        </g>
        <text x="45" y="33" class="skill-text">MySQL</text>
    </g>

    <!-- Popup 3: Frontend -->
    <g opacity="0" transform="translate(350, 20)">
        <animate attributeName="opacity" values="0; 0; 1; 1; 0; 0" keyTimes="0; 0.42; 0.43; 0.52; 0.53; 1" dur="25s" repeatCount="indefinite" />
        <rect x="0" y="0" width="240" height="55" class="ui-box" />
        <!-- Responsive Design SVG -->
        <g transform="translate(15, 17)">
            <rect x="0" y="2" width="14" height="12" rx="2" fill="none" stroke="#00C4CC" stroke-width="2"/>
            <rect x="12" y="8" width="8" height="10" rx="1" fill="#111111" stroke="#E34F26" stroke-width="2"/>
        </g>
        <text x="45" y="33" class="skill-text">Responsive Design</text>
    </g>

    <!-- Popup 4: Version Control -->
    <g opacity="0" transform="translate(480, 400)">
        <animate attributeName="opacity" values="0; 0; 1; 1; 0; 0" keyTimes="0; 0.61; 0.62; 0.71; 0.72; 1" dur="25s" repeatCount="indefinite" />
        <rect x="0" y="0" width="210" height="55" class="ui-box" />
        <!-- Git SVG -->
        <g transform="translate(15, 17)">
            <path d="M10,0 L20,10 L10,20 L0,10 Z" fill="#F05032"/>
            <circle cx="10" cy="5" r="2" fill="#FFFFFF"/>
            <circle cx="15" cy="10" r="2" fill="#FFFFFF"/>
            <circle cx="10" cy="15" r="2" fill="#FFFFFF"/>
            <path d="M10,7 L10,13 M10,13 L15,10" stroke="#FFFFFF" stroke-width="2"/>
        </g>
        <text x="45" y="33" class="skill-text">Git</text>
        <!-- GitHub SVG -->
        <g transform="translate(115, 17)">
            <circle cx="10" cy="10" r="10" fill="#FFFFFF"/>
            <path d="M10,2 C5.5,2 2,5.5 2,10 C2,13.5 4.3,16.5 7.4,17.6 C7.8,17.7 7.9,17.4 7.9,17.2 C7.9,16.8 7.9,15.8 7.9,14.6 C5.6,15.1 5.2,13.5 5.2,13.5 C4.8,12.6 4.3,12.3 4.3,12.3 C3.6,11.8 4.4,11.8 4.4,11.8 C5.2,11.9 5.6,12.6 5.6,12.6 C6.4,14 7.6,13.6 8,13.4 C8.1,12.9 8.3,12.5 8.5,12.3 C6.7,12.1 4.7,11.4 4.7,8.2 C4.7,7.3 5,6.6 5.5,6 C5.4,5.8 5.1,4.9 5.6,3.8 C5.6,3.8 6.3,3.6 7.9,4.7 C8.6,4.5 9.3,4.4 10,4.4 C10.7,4.4 11.4,4.5 12.1,4.7 C13.7,3.6 14.4,3.8 14.4,3.8 C14.9,4.9 14.6,5.8 14.5,6 C15,6.6 15.3,7.3 15.3,8.2 C15.3,11.4 13.4,12.1 11.5,12.3 C11.8,12.6 12,13.1 12,13.9 C12,15 12,15.9 12,16.2 C12,16.5 12.2,16.8 12.6,16.7 C15.7,15.6 18,12.6 18,9 C18,4.5 14.4,1 10,1 Z" fill="#181717"/>
        </g>
        <text x="145" y="33" class="skill-text">GitHub</text>
    </g>

    <!-- Popup 5: Tools -->
    <g opacity="0" transform="translate(580, 10)">
        <animate attributeName="opacity" values="0; 0; 1; 1; 0; 0" keyTimes="0; 0.80; 0.81; 0.90; 0.91; 1" dur="25s" repeatCount="indefinite" />
        <rect x="0" y="0" width="240" height="100" class="ui-box" />
        <!-- VS Code SVG -->
        <g transform="translate(15, 20)">
            <path d="M14,2 L18,5 L18,15 L14,18 L3,10 Z" fill="#007ACC"/>
            <path d="M14,2 L3,10 L8,12 Z" fill="#00599C"/>
            <path d="M14,18 L3,10 L8,8 Z" fill="#00599C"/>
        </g>
        <text x="45" y="36" class="skill-text">VS Code</text>
        <!-- XAMPP SVG -->
        <g transform="translate(145, 20)">
            <circle cx="10" cy="10" r="10" fill="#FB7A24"/>
            <path d="M6,6 L14,14 M14,6 L6,14" stroke="#FFFFFF" stroke-width="3"/>
        </g>
        <text x="175" y="36" class="skill-text">XAMPP</text>
        <!-- Figma SVG -->
        <g transform="translate(15, 60)">
            <circle cx="7" cy="5" r="4" fill="#F24E1E"/>
            <circle cx="14" cy="5" r="4" fill="#FF7262"/>
            <circle cx="7" cy="11" r="4" fill="#A259FF"/>
            <circle cx="14" cy="11" r="4" fill="#1ABCFE"/>
            <circle cx="7" cy="17" r="4" fill="#0ACF83"/>
        </g>
        <text x="45" y="76" class="skill-text">Figma</text>
        <!-- Canva SVG -->
        <g transform="translate(145, 60)">
            <circle cx="10" cy="10" r="10" fill="#00C4CC"/>
            <text x="4" y="15" font-family="Arial" font-weight="bold" font-size="14" fill="#FFFFFF">C</text>
        </g>
        <text x="175" y="76" class="skill-text">Canva</text>
    </g>


    <!-- ANIMATED CHARACTER ALONG NEW ZIG-ZAG PATH -->
    <g>
        <animateTransform attributeName="transform" type="translate"
            values="
                -30,205;  
                115,205;  
                115,130;  
                115,130;  
                115,205;  
                275,205;  
                275,340;  
                275,340;  
                275,205;  
                435,205;  
                435,140;  
                435,140;  
                435,205;  
                595,205;
                595,320;
                595,320;
                595,205;
                745,205;
                745,120;
                745,120;
                745,205;
                880,205
            "
            keyTimes="
                0;
                0.04;
                0.06;
                0.15;
                0.17;
                0.21;
                0.24;
                0.33;
                0.36;
                0.40;
                0.43;
                0.52;
                0.55;
                0.59;
                0.62;
                0.71;
                0.74;
                0.78;
                0.81;
                0.90;
                0.93;
                1
            "
            dur="25s" repeatCount="indefinite" />

        <!-- High-Fidelity Pixel Suit Character (Scaled x2) -->
        <g transform="scale(2)" image-rendering="pixelated">
            <rect x="3" y="0" width="10" height="2" fill="#000000"/>
            <rect x="1" y="2" width="13" height="4" fill="#000000"/>
            <rect x="1" y="6" width="3" height="3" fill="#000000"/>
            <rect x="12" y="6" width="2" height="3" fill="#000000"/>
            <rect x="4" y="6" width="8" height="7" fill="#fcc2b2"/>
            <rect x="2" y="9" width="2" height="2" fill="#fcc2b2"/>
            <rect x="7" y="8" width="1" height="2" fill="#000000"/>
            <rect x="11" y="8" width="1" height="2" fill="#000000"/>
            <rect x="8" y="11" width="3" height="1" fill="#000000"/>
            <rect x="1" y="13" width="13" height="5" fill="#434343"/>
            <rect x="1" y="15" width="2" height="3" fill="#434343"/>
            <rect x="12" y="15" width="2" height="3" fill="#434343"/>
            <rect x="1" y="18" width="2" height="1" fill="#fcc2b2"/>
            <rect x="6" y="13" width="3" height="4" fill="#ffffff"/>
            <rect x="7" y="14" width="1" height="3" fill="#000000"/>
            <rect x="3" y="18" width="9" height="4" fill="#808080"/>
            <rect x="3" y="22" width="3" height="1" fill="#000000"/>
            <rect x="9" y="22" width="3" height="1" fill="#000000"/>
        </g>
    </g>

    </svg>'''

    with open("skills_map.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("✨ Generated: Staggered RPG Multi-Level Village Map with custom Vector Tech SVGs.")

if __name__ == "__main__":
    generate_animated_skills_svg()
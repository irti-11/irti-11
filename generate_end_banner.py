#!/usr/bin/env python3
"""
generate_se7en_banner.py
Generates an animated GitHub End Banner inspired by the SE7EN poster, 
featuring premium blurred backgrounds and bouncing stack mechanics.
"""

WIDTH, HEIGHT = 1200, 420
OUTFILE = "se7en_end_banner.svg"

# Palette & Fonts
BG_COLOR = "#070000"  # Deep black/red base
TEXT_MAIN = "#f2f2f2" # Gritty white
ACCENT_RED = "#8a0303" 
ACCENT_DARK_RED = "#3b0000"

# Tech stack exactly as requested
STACK_BLOCKS = [
    {"label": "HTML",       "color": "#ffffff", "w": 60,  "start_x": 140,  "delay": "0s",    "dur": "5.5s", "path": "M 0,0 L 40,280 L 100,60 L 60,280 L 0,0"},
    {"label": "CSS",        "color": "#ffffff", "w": 60,  "start_x": 340,  "delay": "1s",    "dur": "6.2s", "path": "M 0,0 L -50,280 L 60,100 L -30,280 L 0,0"},
    {"label": "JavaScript", "color": "#ffffff", "w": 90,  "start_x": 540,  "delay": "0.5s",  "dur": "5.8s", "path": "M 0,0 L 50,280 L -40,120 L 30,280 L 0,0"},
    {"label": "PHP",        "color": "#ffffff", "w": 60,  "start_x": 760,  "delay": "1.8s",  "dur": "6.5s", "path": "M 0,0 L -60,280 L 70,80 L -20,280 L 0,0"},
    {"label": "MySQL",      "color": "#ffffff", "w": 70,  "start_x": 960,  "delay": "0.8s",  "dur": "5.1s", "path": "M 0,0 L 40,280 L -50,90 L 50,280 L 0,0"},
]

def generate_svg():
    # Premium blurred background orbs
    background_blurs = f'''
    <circle cx="200" cy="210" r="180" fill="{ACCENT_DARK_RED}" filter="url(#premium-blur)" opacity="0.8" />
    <circle cx="900" cy="100" r="250" fill="{ACCENT_RED}" filter="url(#premium-blur)" opacity="0.4" />
    <circle cx="600" cy="350" r="200" fill="#a80000" filter="url(#premium-blur)" opacity="0.3" />
    '''

    # Moving Paddle Line (Gritty white to match the theme)
    paddle_svg = f'''
    <g transform="translate(0, 360)">
      <rect x="0" y="0" width="180" height="4" fill="#ffffff" filter="url(#glow)">
        <animateTransform 
          attributeName="transform" 
          type="translate" 
          values="50,0; 970,0; 50,0" 
          dur="7s" 
          repeatCount="indefinite" 
          calcMode="spline" 
          keySplines="0.4 0.1 0.6 0.9; 0.4 0.1 0.6 0.9" />
      </rect>
    </g>
    '''

    # Tech Stack Bouncing Boxes
    blocks_svg = ""
    for block in STACK_BLOCKS:
        blocks_svg += f'''
        <g transform="translate({block['start_x']}, -20)">
          <g>
            <animateTransform 
              attributeName="transform" 
              type="translate" 
              path="{block['path']}" 
              dur="{block['dur']}" 
              begin="{block['delay']}" 
              repeatCount="indefinite" />
            
            <rect x="-{block['w']//2}" y="-15" width="{block['w']}" height="30" 
                  fill="transparent" stroke="{block['color']}" stroke-width="1.5" stroke-dasharray="4 2" />
            <text x="0" y="5" text-anchor="middle" font-family="'Courier New', monospace" 
                  font-weight="bold" font-size="14" fill="{block['color']}">{block['label']}</text>
          </g>
        </g>
        '''

    svg_content = f'''<svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}"
     xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Syed Irtiza Ali Banner">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&amp;display=swap');
      
      .se7en-text {{
        font-family: 'Permanent Marker', cursive, sans-serif;
        text-transform: uppercase;
        letter-spacing: 6px;
      }}
    </style>
    
    <!-- Premium background blur filter -->
    <filter id="premium-blur" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="60" />
    </filter>
    
    <!-- Slight glow for the text and paddle -->
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Deep dark canvas -->
  <rect width="{WIDTH}" height="{HEIGHT}" fill="{BG_COLOR}" />

  <!-- Moody, blurred background elements -->
  {background_blurs}

  <!-- SE7EN Style Text Layers (Slight offsets for the scratchy, chaotic brush look) -->
  <g transform="rotate(-3, {WIDTH/2}, {HEIGHT/2})">
    <text x="{WIDTH/2 + 3}" y="{HEIGHT/2 + 23}" text-anchor="middle" class="se7en-text" font-size="110" fill="#a80000" opacity="0.6">
      SYED IRTIZA ALI
    </text>
    <text x="{WIDTH/2 - 2}" y="{HEIGHT/2 + 18}" text-anchor="middle" class="se7en-text" font-size="110" fill="#520000" opacity="0.8">
      SYED IRTIZA ALI
    </text>
    <text x="{WIDTH/2}" y="{HEIGHT/2 + 20}" text-anchor="middle" class="se7en-text" font-size="110" fill="{TEXT_MAIN}" filter="url(#glow)">
      SYED IRTIZA ALI
    </text>
  </g>

  <!-- Interactive/Moving Game Line -->
  {paddle_svg}
  
  <!-- Falling & Bouncing Stack Blocks -->
  {blocks_svg}

</svg>
'''
    return svg_content

if __name__ == "__main__":
    with open(OUTFILE, "w", encoding="utf-8") as f:
        f.write(generate_svg())
    print(f"Successfully generated SE7EN banner at {OUTFILE}")
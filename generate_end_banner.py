#!/usr/init/env python3
"""
generate_end_banner.py - PREMIUM BLURRED BACKGROUND & WAVE DROP VERSION

Generates an SVG banner with a sleek, heavily blurred ambient background,
prominent wave drop-in animation for pixels, and clean floating text.
"""

import random

# ----------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------

SEED = 42
random.seed(SEED)

WIDTH, HEIGHT = 1200, 420
OUTFILE = "end_banner.svg"

BG_COLOR = "#030804"
GRID_COLOR = "#123018"
GRID_OPACITY = 0.25  # Softer, more premium grid lines
GRID_STEP = 20

FG_GREENS = ["#3ddc5b", "#4fe873", "#5cf27f", "#33c94f"]
BG_GREENS = ["#15471a", "#1e5c26", "#123817"]

TEXT_COLOR = "#eafff0"
FONT = "'Caveat', 'Segoe Script', cursive"

CELL = 22
GAP = 2

TEXT_ZONE = (0.14, 0.34, 0.86, 0.68)

# Timeline
T = 13.0
REVEAL_START = 0.04
REVEAL_END = 0.42
TEXT_IN_START = 0.44
TEXT_IN_END = 0.64
SHINE_GATE_IN = 0.46
SHINE_GATE_OUT = 0.90
HOLD_END = 0.92
SCENE_FADE_END = 0.99

EASE_OUT = "0.16 1 0.3 1"
EASE_SMOOTH = "0.42 0 0.58 1"
LINEAR_HOLD = "0 0 1 1"


def fmt(n):
    if isinstance(n, float):
        return f"{n:.3f}".rstrip("0").rstrip(".")
    return str(n)


def semis(values):
    return ";".join(values)


# ----------------------------------------------------------------------
# DENSE MULTI-LAYER CLUSTER GENERATION
# ----------------------------------------------------------------------

def build_layers():
    exact_map = [
        "  1111                  1111                                111  111 ",
        " 111111                111111                              11111 1111",
        "  1111   1              1111    1                 1         1111  111 ",
        "       1111                    1111              1111           ",
        "      111111                  111111            111111          ",
        "        11                      11                11            ",
        "                  111                             111           ",
        "                 11111 1 11                      11111 1 11     ",
        "     1          11111111 1 11         1         11111111 1 11   ",
        " 111111    111 111 1111 1           11111    111 111 1111 1     11",
        " 11 1111 11111 1111 11 1111   11    11 1111 11111 1111 11 1111   11 11",
        " 1111  1 11     1111 11             1111  1 11     1111 11      1 1",
        "        1     1                         1     1            1111",
        "                                                            11 1",
        "                            111                    1111       ",
        "                            11 1     1      1      1111       ",
        "                             1111 1 1111 11 11 1                ",
        "                              111 1 1111  1 11 1                ",
        "                              11   1      1                   "
    ]

    fg_blocks = []
    bg_blocks = []

    for row_idx, row_str in enumerate(exact_map):
        for col_idx, char in enumerate(row_str):
            if char == '1':
                x = col_idx * CELL + GAP / 2
                y = row_idx * CELL + GAP / 2
                size = CELL - GAP

                if random.random() < 0.70:
                    color = random.choice(FG_GREENS)
                    fg_blocks.append({"x": x, "y": y, "size": size, "color": color})
                else:
                    color = random.choice(BG_GREENS)
                    bg_blocks.append({"x": x + 2, "y": y + 2, "size": size - 2, "color": color})

    return fg_blocks, bg_blocks


# ----------------------------------------------------------------------
# ANIMATION BUILDERS (PROMINENT WAVE DROP)
# ----------------------------------------------------------------------

def render_block_layer(blocks, layer_type, uid_prefix):
    layer_svgs = []
    for i, b in enumerate(blocks):
        x, y, size, color = b["x"], b["y"], b["size"], b["color"]

        dist_from_right = (WIDTH - (x + size / 2)) / WIDTH
        jitter = random.uniform(-0.015, 0.015)
        
        delay_offset = 0.05 if layer_type == "bg" else 0.0
        t_in = REVEAL_START + delay_offset + dist_from_right * (REVEAL_END - REVEAL_START - 0.12) + jitter
        t_in = max(REVEAL_START, min(t_in, REVEAL_END - 0.12))
        t_settled = min(t_in + 0.15, REVEAL_END)

        max_opacity = "0.30" if layer_type == "bg" else "1"
        key_times = [0, t_in, t_settled, 1]
        
        op_values = ["0", "0", max_opacity, max_opacity]
        op_splines = [LINEAR_HOLD, EASE_OUT, LINEAR_HOLD]

        # Wave drop effect: items start higher up and settle smoothly into place
        start_y_offset = -45 if layer_type == "fg" else -30
        trans_values = f"0,{start_y_offset}; 0,{start_y_offset}; 0,0; 0,0"
        trans_splines = [LINEAR_HOLD, EASE_OUT, LINEAR_HOLD]

        kt_str = semis(fmt(k) for k in key_times)
        op_str = semis(op_values)
        ospl_str = semis(op_splines)
        tr_str = semis(trans_values)
        trspl_str = semis(trans_splines)
        
        css_class = "bg-pix" if layer_type == "bg" else "fg-pix"

        layer_svgs.append(
            f'<g opacity="0">'
            f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" '
            f'calcMode="spline" keyTimes="{kt_str}" values="{op_str}" keySplines="{ospl_str}"/>'
            f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(size)}" height="{fmt(size)}" '
            f'rx="1" fill="{color}" class="{css_class}" data-uid="{uid_prefix}-{i}">'
            f'<animateTransform attributeName="transform" type="translate" dur="{T}s" repeatCount="indefinite" '
            f'calcMode="spline" keyTimes="{kt_str}" values="{tr_str}" keySplines="{trspl_str}"/>'
            f'</rect>'
            f'</g>'
        )
    return "\n    ".join(layer_svgs)


def build_grid_pattern():
    return f'''    <pattern id="crtGrid" width="{GRID_STEP}" height="{GRID_STEP}" patternUnits="userSpaceOnUse">
      <path d="M {GRID_STEP} 0 L 0 0 0 {GRID_STEP}" fill="none"
            stroke="{GRID_COLOR}" stroke-width="1" opacity="{GRID_OPACITY}"/>
    </pattern>'''


def build_shine(fg_blocks):
    clip_rects = "".join(
        f'<rect x="{fmt(b["x"])}" y="{fmt(b["y"])}" width="{fmt(b["size"])}" height="{fmt(b["size"])}" rx="1"/>'
        for b in fg_blocks
    )

    gate_kt = [0, SHINE_GATE_IN, SHINE_GATE_IN + 0.03, SHINE_GATE_OUT, SHINE_GATE_OUT + 0.03, 1]
    gate_vals = ["0", "0", "1", "1", "0", "0"]
    gate_splines = [LINEAR_HOLD, EASE_SMOOTH, LINEAR_HOLD, EASE_SMOOTH, LINEAR_HOLD]
    gate_kt_str = semis(fmt(k) for k in gate_kt)
    gate_val_str = semis(gate_vals)
    gate_spl_str = semis(gate_splines)

    band_w = WIDTH * 0.9
    sweep_dur = (SHINE_GATE_OUT - SHINE_GATE_IN) * T

    max_pos = WIDTH + band_w
    trans_values = f"0,0; {fmt(max_pos)},0; 0,0"
    trans_kt = "0; 0.5; 1"
    trans_splines = f"{EASE_SMOOTH}; {EASE_SMOOTH}"

    defs_markup = f'''    <clipPath id="pixClip">
      {clip_rects}
    </clipPath>
    <linearGradient id="shineGrad" x1="0" y1="0" x2="1" y2="0.35">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="45%" stop-color="#eafff0" stop-opacity="0"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.55"/>
      <stop offset="55%" stop-color="#eafff0" stop-opacity="0"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>'''

    render_markup = f'''<g clip-path="url(#pixClip)" opacity="0">
    <animate attributeName="opacity" dur="{T}s" repeatCount="indefinite"
      calcMode="spline" keyTimes="{gate_kt_str}" values="{gate_val_str}" keySplines="{gate_spl_str}"/>
    <rect x="{fmt(-band_w)}" y="0" width="{fmt(band_w)}" height="{HEIGHT}" fill="url(#shineGrad)"
          style="mix-blend-mode:screen">
      <animateTransform attributeName="transform" type="translate"
        dur="{fmt(sweep_dur)}s" repeatCount="indefinite"
        values="{trans_values}" keyTimes="{trans_kt}"
        calcMode="spline" keySplines="{trans_splines}"/>
    </rect>
  </g>'''

    return defs_markup, render_markup


# ----------------------------------------------------------------------
# CLEAN FLOATING TERMINAL TYPING TEXT EFFECT (NO BOX)
# ----------------------------------------------------------------------

def build_text():
    cx = WIDTH / 2
    x0, y0, x1, y1 = TEXT_ZONE
    zone_cy = HEIGHT * (y0 + y1) / 2

    kt = [0, TEXT_IN_START, TEXT_IN_END, HOLD_END, SCENE_FADE_END, 1]
    w_vals = ["0", "0", f"{WIDTH}", f"{WIDTH}", "0", "0"]
    splines = [LINEAR_HOLD, EASE_SMOOTH, LINEAR_HOLD, EASE_SMOOTH, LINEAR_HOLD]

    kt_str = semis(fmt(k) for k in kt)
    w_str = semis(w_vals)
    spl_str = semis(splines)

    return f'''    <!-- Typing reveal clip path -->
    <clipPath id="textTypingClip">
      <rect x="0" y="0" width="0" height="{HEIGHT}">
        <animate attributeName="width" dur="{T}s" repeatCount="indefinite"
          calcMode="spline" keyTimes="{kt_str}" values="{w_str}" keySplines="{spl_str}"/>
      </rect>
    </clipPath>

    <!-- Clean floating text group without any background box -->
    <g id="animatedProfileText" clip-path="url(#textTypingClip)">
      <text x="{fmt(cx)}" y="{fmt(zone_cy - 10)}" text-anchor="middle" font-family="{FONT}"
            font-weight="700" font-size="34" fill="{TEXT_COLOR}">End of profile. Currently deepening my skills in PHP, MySQL,</text>
      <text x="{fmt(cx)}" y="{fmt(zone_cy + 34)}" text-anchor="middle" font-family="{FONT}"
            font-weight="700" font-size="34" fill="{TEXT_COLOR}">and JavaScript — one shipped project at a time</text>
    </g>'''


# ----------------------------------------------------------------------
# ASSEMBLE SVG
# ----------------------------------------------------------------------

def build_svg():
    fg_blocks, bg_blocks = build_layers()
    
    bg_svgs = render_block_layer(bg_blocks, "bg", "bg")
    fg_svgs = render_block_layer(fg_blocks, "fg", "fg")
    
    text_svg = build_text()
    shine_defs, shine_render = build_shine(fg_blocks)
    grid_pattern = build_grid_pattern()

    scene_kt = [0, HOLD_END, SCENE_FADE_END, 1]
    scene_vals = ["1", "1", "0", "0"]
    scene_splines = [LINEAR_HOLD, EASE_SMOOTH, LINEAR_HOLD]
    scene_kt_str = semis(fmt(k) for k in scene_kt)
    scene_val_str = semis(scene_vals)
    scene_spl_str = semis(scene_splines)

    # Enhanced background blur (stdDeviation="5.0") for a gorgeous ambient depth
    filters_def = f'''    <filter id="fg-glow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="2.2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="bg-blur" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="5.0" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>'''

    svg = f'''<svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}"
     preserveAspectRatio="xMidYMid meet"
     xmlns="http://www.w3.org/2000/svg" role="img" aria-label="End of profile banner">
  <title>End of profile</title>
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&amp;display=swap');
      .fg-pix {{ filter: url(#fg-glow); }}
      .bg-pix {{ filter: url(#bg-blur); }}
    </style>
{grid_pattern}
{filters_def}
{shine_defs}
{text_svg}
  </defs>

  <rect width="{WIDTH}" height="{HEIGHT}" fill="{BG_COLOR}"/>
  <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#crtGrid)"/>

  <g opacity="1">
    <animate attributeName="opacity" dur="{T}s" repeatCount="indefinite"
      calcMode="spline" keyTimes="{scene_kt_str}" values="{scene_val_str}"
      keySplines="{scene_spl_str}"/>

    {bg_svgs}
    {fg_svgs}
    {shine_render}
  </g>

  <use href="#animatedProfileText" /> 
</svg>'''
    return svg


def main():
    svg = build_svg()
    with open(OUTFILE, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote premium blurred background banner to {OUTFILE} ({len(svg):,} bytes)")


if __name__ == "__main__":
    main()
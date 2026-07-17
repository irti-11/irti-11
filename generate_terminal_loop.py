import html

COLOR_CYAN = "#78dec7"
COLOR_PINK = "#f2a6c3"
COLOR_GREEN = "#aef3a4"
COLOR_WHITE = "#e2e8f0"
COLOR_DIM = "#6272a4"
BG_COLOR = "#0d1117"

FONT_SIZE = 12
CHAR_W = FONT_SIZE * 0.6
LINE_H = 20
PAD_TOP = 34

SCENES = [
    [("$ npm run dev", COLOR_WHITE, ""),
     ("compiled successfully", COLOR_GREEN, "\u2713 "),
     ("watching for changes...", COLOR_DIM, "> ")],

    [("$ git status", COLOR_WHITE, ""),
     ("working tree clean", COLOR_GREEN, "\u2713 "),
     ("branch up to date", COLOR_DIM, "> ")],

    [("$ pytest", COLOR_WHITE, ""),
     ("12 passed in 0.8s", COLOR_GREEN, "\u2713 "),
     ("no warnings found", COLOR_DIM, "> ")],

    [("$ php artisan serve", COLOR_WHITE, ""),
     ("server started :8000", COLOR_GREEN, "\u2713 "),
     ("ctrl+c to stop", COLOR_DIM, "> ")],
]

TYPE_DUR = 0.75
LINE_GAP = 0.15
HOLD = 1.5
CLEAR_DUR = 0.3
SCENE_GAP = 0.3


def frac(t, cycle):
    return round(t / cycle, 5)


def generate_terminal_loop(width=300, height=90):
    # --- build global timeline ---
    scene_windows = []   # (scene, [ (start,end) per line ], hold_start, clear_start, clear_end)
    t = 0.0
    for scene in SCENES:
        line_times = []
        for _, _, _ in scene:
            start = t
            end = t + TYPE_DUR
            line_times.append((start, end))
            t = end + LINE_GAP
        hold_start = t - LINE_GAP
        clear_start = hold_start + HOLD
        clear_end = clear_start + CLEAR_DUR
        scene_windows.append((scene, line_times, hold_start, clear_start, clear_end))
        t = clear_end + SCENE_GAP

    cycle = round(t, 3)

    body = ""
    cursor_vis_times = []
    cursor_vis_values = []
    cursor_x_times = []
    cursor_x_values = []
    cursor_y_times = []
    cursor_y_values = []

    for s_idx, (scene, line_times, hold_start, clear_start, clear_end) in enumerate(scene_windows):
        for l_idx, ((text, color, prefix), (start, end)) in enumerate(zip(scene, line_times)):
            full_text = prefix + text
            w = len(full_text) * CHAR_W
            y = PAD_TOP + l_idx * LINE_H

            # width goes 0 -> w during [start,end], holds at w until clear_start, back to 0 by clear_end
            kt = [0, frac(start, cycle), frac(end, cycle), frac(clear_start, cycle), frac(clear_end, cycle)]
            vals = [0, 0, w, w, 0]
            if kt[-1] < 1:
                kt.append(1)
                vals.append(0)
            kt_str = ";".join(str(x) for x in kt)
            val_str = ";".join(f"{v:.1f}" for v in vals)

            body += f'''    <g clip-path="url(#s{s_idx}l{l_idx})">
        <text x="20" y="{y}" style="font-family:'Fira Code',monospace; font-size:{FONT_SIZE}px; fill:{color};">{html.escape(full_text)}</text>
    </g>
    <clipPath id="s{s_idx}l{l_idx}">
        <rect x="20" y="{y - FONT_SIZE}" width="0" height="{LINE_H}">
            <animate attributeName="width" keyTimes="{kt_str}" values="{val_str}"
                     dur="{cycle}s" repeatCount="indefinite" calcMode="linear" />
        </rect>
    </clipPath>
'''
        # cursor: visible from last line's end -> clear_start, positioned at end of last line
        last_text, last_color, last_prefix = scene[-1]
        last_w = len(last_prefix + last_text) * CHAR_W
        last_y = PAD_TOP + (len(scene) - 1) * LINE_H
        show_t = frac(hold_start, cycle)
        hide_t = frac(clear_start, cycle)

        cursor_vis_times += [show_t, hide_t]
        cursor_vis_values += ["visible", "hidden"]
        cursor_x_times += [show_t]
        cursor_x_values += [f"{20 + last_w + 4:.1f}"]
        cursor_y_times += [show_t]
        cursor_y_values += [str(last_y)]

    # assemble cursor animate strings (discrete jumps)
    vis_kt = ";".join(str(x) for x in cursor_vis_times)
    vis_vals = ";".join(cursor_vis_values)
    x_kt = ";".join(str(x) for x in cursor_x_times)
    x_vals = ";".join(cursor_x_values)
    y_kt = ";".join(str(x) for x in cursor_y_times)
    y_vals = ";".join(cursor_y_values)

    body += f'''    <text x="{cursor_x_values[0]}" y="{cursor_y_values[0]}" class="blink" style="font-family:'Fira Code',monospace; font-size:{FONT_SIZE}px; fill:{COLOR_CYAN}; visibility:hidden;">
        <animate attributeName="visibility" keyTimes="{vis_kt}" values="{vis_vals}" dur="{cycle}s" repeatCount="indefinite" calcMode="discrete" />
        <animate attributeName="x" keyTimes="{x_kt}" values="{x_vals}" dur="{cycle}s" repeatCount="indefinite" calcMode="discrete" />
        <animate attributeName="y" keyTimes="{y_kt}" values="{y_vals}" dur="{cycle}s" repeatCount="indefinite" calcMode="discrete" />
        |
    </text>
'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}" preserveAspectRatio="xMinYMin meet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&amp;display=swap');
        @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
    </style>
    <rect width="100%" height="100%" fill="{BG_COLOR}" rx="8" />
    <circle cx="16" cy="14" r="4" fill="#ff5f56" />
    <circle cx="30" cy="14" r="4" fill="#ffbd2e" />
    <circle cx="44" cy="14" r="4" fill="#27c93f" />
{body}</svg>'''

    with open("terminal_loop.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"✨ Generated: terminal_loop.svg — {len(SCENES)} scenes, {cycle}s full cycle")


if __name__ == "__main__":
    generate_terminal_loop()
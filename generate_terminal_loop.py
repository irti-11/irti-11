import html

# Same palette as banner + equalizer
COLOR_CYAN = "#78dec7"
COLOR_PINK = "#f2a6c3"
COLOR_GREEN = "#aef3a4"
COLOR_WHITE = "#e2e8f0"
COLOR_DIM = "#6272a4"
BG_COLOR = "#0d1117"

def build_keytimes(start, end, clear_start, clear_end, cycle):
    """Returns (keyTimes, values) for a clip-rect width animation: 0 -> W -> hold -> 0"""
    pts = []
    if start > 0:
        pts.append((0, 0))
    pts.append((start, 0))
    pts.append((end, 1))          # 1 = full width (scaled later)
    pts.append((clear_start, 1))
    pts.append((clear_end, 0))
    if clear_end < cycle:
        pts.append((cycle, 0))

    # dedupe + normalize to 0..1 fractions
    seen = []
    for t, v in pts:
        frac = round(t / cycle, 4)
        if seen and seen[-1][0] == frac:
            seen[-1] = (frac, v)
        else:
            seen.append((frac, v))
    times = ";".join(str(t) for t, _ in seen)
    values = ";".join(str(v) for _, v in seen)
    return times, values


def generate_terminal_loop(width=300, height=90):
    lines = [
        {"text": "$ npm run dev", "color": COLOR_WHITE, "dur": 1.0},
        {"text": "compiled successfully", "color": COLOR_GREEN, "dur": 0.9, "prefix": "\u2713 "},
        {"text": "watching for changes...", "color": COLOR_DIM, "dur": 1.0, "prefix": "> "},
    ]

    gap = 0.2
    hold_after = 1.8
    clear_dur = 0.3
    font_size = 12
    line_h = 20
    pad_top = 34
    char_w = font_size * 0.6

    # sequential timeline
    t = 0.0
    for ln in lines:
        ln["start"] = t
        ln["end"] = t + ln["dur"]
        t = ln["end"] + gap
    last_end = t - gap
    clear_start = last_end + hold_after
    clear_end = clear_start + clear_dur
    cycle = round(clear_end, 3)

    body = ""
    y = pad_top
    for idx, ln in enumerate(lines):
        full_text = ln.get("prefix", "") + ln["text"]
        w = len(full_text) * char_w
        times, values = build_keytimes(ln["start"], ln["end"], clear_start, clear_end, cycle)

        body += f'''    <g clip-path="url(#tline{idx})">
        <text x="20" y="{y}" style="font-family:'Fira Code',monospace; font-size:{font_size}px; fill:{ln["color"]};">{html.escape(full_text)}</text>
    </g>
    <clipPath id="tline{idx}">
        <rect x="20" y="{y - font_size}" width="0" height="{line_h}">
            <animate attributeName="width" keyTimes="{times}"
                     values="{';'.join(str(float(v) * w) for v in values.split(';'))}"
                     dur="{cycle}s" repeatCount="indefinite" calcMode="linear" />
        </rect>
    </clipPath>
'''
        y += line_h

    # blinking cursor after the last line, visible only during the hold window
    cursor_show = round(last_end / cycle, 4)
    cursor_hide = round(clear_start / cycle, 4)
    last_w = (len(lines[-1].get("prefix", "") + lines[-1]["text"])) * char_w
    cursor_x = 20 + last_w + 4
    cursor_y = pad_top + (len(lines) - 1) * line_h

    body += f'''    <text x="{cursor_x:.1f}" y="{cursor_y}" class="blink" style="font-family:'Fira Code',monospace; font-size:{font_size}px; fill:{COLOR_CYAN};">
        <animate attributeName="opacity" keyTimes="0;{cursor_show};{cursor_show};{cursor_hide};{cursor_hide};1"
                 values="0;0;1;1;0;0" dur="{cycle}s" repeatCount="indefinite" calcMode="discrete" />
        |
    </text>
'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
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
    print("✨ Generated: terminal_loop.svg (looping fake terminal)")


if __name__ == "__main__":
    generate_terminal_loop()
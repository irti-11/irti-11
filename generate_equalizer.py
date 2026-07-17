import random

# Same palette as your banner
COLOR_CYAN = "#78dec7"
COLOR_PINK = "#f2a6c3"
COLOR_GREEN = "#aef3a4"
COLOR_WHITE = "#e2e8f0"

PALETTE = [COLOR_CYAN, COLOR_PINK, COLOR_GREEN, COLOR_WHITE]

def generate_equalizer_svg(width=300, height=90, num_bars=18, seed=None):
    if seed is not None:
        random.seed(seed)

    bar_gap = 4
    bar_w = (width - (bar_gap * (num_bars - 1))) / num_bars
    baseline = height  # bars grow upward from the bottom

    bars_svg = ""
    for i in range(num_bars):
        x = i * (bar_w + bar_gap)
        color = PALETTE[i % len(PALETTE)]

        # Generate a random sequence of heights to mimic a live audio signal
        steps = random.randint(4, 6)
        heights = [random.uniform(height * 0.15, height * 0.95) for _ in range(steps)]
        heights.append(heights[0])  # loop back smoothly

        dur = round(random.uniform(0.6, 1.3), 2)   # each bar has its own speed
        delay = round(random.uniform(0, 0.5), 2)   # slight offset so bars don't sync

        # Build the keyTimes-based values for height and y (y = baseline - height)
        n = len(heights)
        key_times = [round(j / (n - 1), 3) for j in range(n)]
        height_values = ";".join(f"{h:.1f}" for h in heights)
        y_values = ";".join(f"{baseline - h:.1f}" for h in heights)

        bars_svg += f'''    <rect x="{x:.1f}" y="{baseline - heights[0]:.1f}" width="{bar_w:.1f}" height="{heights[0]:.1f}" rx="2" fill="{color}">
        <animate attributeName="height" values="{height_values}" keyTimes="{';'.join(str(t) for t in key_times)}"
                 dur="{dur}s" begin="{delay}s" repeatCount="indefinite" calcMode="spline"
                 keySplines="{' '.join(['0.4 0 0.6 1'] * (n - 1))}" />
        <animate attributeName="y" values="{y_values}" keyTimes="{';'.join(str(t) for t in key_times)}"
                 dur="{dur}s" begin="{delay}s" repeatCount="indefinite" calcMode="spline"
                 keySplines="{' '.join(['0.4 0 0.6 1'] * (n - 1))}" />
    </rect>
'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    <rect width="100%" height="100%" fill="transparent" />
{bars_svg}</svg>'''

    with open("equalizer.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("✨ Generated: equalizer.svg (cava-style animated bars)")


if __name__ == "__main__":
    generate_equalizer_svg()
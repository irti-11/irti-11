#!/usr/bin/env python3
"""
generate_led_matrix.py

Fetches real GitHub contribution data via the GraphQL API and renders it as
an animated "CRT terminal" LED matrix SVG (led_matrix.svg) for embedding in
a GitHub profile README.

Visual concept: a phosphor-green CRT display. On load, a bright scan bar
sweeps left-to-right across the grid (like a monitor initializing / a raster
scan reading the tape), lighting each week-column as it passes. Scanlines
and a soft vignette sit over the whole thing for the terminal feel. Once the
sweep finishes, high-activity cells occasionally re-flicker like an idling
CRT.

Requires:
    - env var GH_PAT: a GitHub Personal Access Token with read access to
      contribution data.
    - env var GITHUB_USERNAME (optional): defaults to "irti-11".
    - pip package: requests

Output:
    - led_matrix.svg written to the current working directory.
"""

import os
import sys
import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

USERNAME = os.environ.get("GITHUB_USERNAME", "irti-11")
GH_PAT = os.environ.get("GH_PAT")

GRAPHQL_URL = "https://api.github.com/graphql"
OUTPUT_FILE = "led_matrix.svg"

CELL_SIZE = 11
CELL_GAP = 3
CELL_RADIUS = 2
MARGIN = 12

# --- CRT / phosphor palette -------------------------------------------------
BG_COLOR = "#02100a"          # near-black, faint green cast — the tube glass
UNLIT_COLOR = "#0a1c12"       # dark phosphor, cell not excited
SCANLINE_COLOR = "#000000"
VIGNETTE_COLOR = "#000a05"

LEVEL_COLORS = {
    1: "#0f3d22",
    2: "#1c7a3e",
    3: "#33b854",
    4: "#7dffa0",
}
HOT_CORE_COLOR = "#eafff2"    # near-white phosphor flare, level-4 only
SCAN_BAR_COLOR = "#8dffb3"    # bright sweeping raster line

TOTAL_WAVE_DURATION = 2.4     # total time for the scan bar to cross the grid
ENTRANCE_DURATION = 0.5
FLICKER_DURATION = 0.6
FLICKER_START_GAP = 0.15

# idle CRT flicker after boot: high-level cells randomly re-pulse
IDLE_FLICKER_LEVELS = (3, 4)
IDLE_FLICKER_PERIOD = 9.0     # seconds between idle re-flickers per cell

CONTRIBUTION_QUERY = """
query($userName:String!) {
  user(login: $userName){
    contributionsCollection {
      contributionCalendar {
        weeks {
          contributionDays {
            contributionCount
            contributionLevel
          }
        }
      }
    }
  }
}
"""

LEVEL_MAP = {
    "NONE": 0,
    "FIRST_QUARTILE": 1,
    "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3,
    "FOURTH_QUARTILE": 4,
}


# ---------------------------------------------------------------------------
# Data fetching
# ---------------------------------------------------------------------------

def fetch_contribution_weeks(username: str, token: str):
    if not token:
        raise RuntimeError(
            "GH_PAT environment variable is not set. The GitHub Actions "
            "workflow must pass it in as an env var for this script."
        )

    headers = {
        "Authorization": f"bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {"query": CONTRIBUTION_QUERY, "variables": {"userName": username}}

    resp = requests.post(GRAPHQL_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if "errors" in data:
        raise RuntimeError(f"GitHub GraphQL API returned errors: {data['errors']}")

    try:
        raw_weeks = (
            data["data"]["user"]["contributionsCollection"]
            ["contributionCalendar"]["weeks"]
        )
    except (KeyError, TypeError) as exc:
        raise RuntimeError(f"Unexpected GraphQL response shape: {data}") from exc

    weeks = []
    for week in raw_weeks:
        days = []
        for day in week["contributionDays"]:
            level = LEVEL_MAP.get(day.get("contributionLevel"), 0)
            days.append(level)
        weeks.append(days)

    return weeks


# ---------------------------------------------------------------------------
# SVG building
# ---------------------------------------------------------------------------

def build_filters():
    filters = []
    blur_std = {1: 0.6, 2: 1.0, 3: 1.5, 4: 2.2}
    halo_std = {1: 1.4, 2: 2.0, 3: 2.8, 4: 4.2}

    for level in (1, 2, 3, 4):
        color = LEVEL_COLORS[level]
        filters.append(f'''
    <filter id="glow-{level}" x="-200%" y="-200%" width="500%" height="500%">
      <feFlood flood-color="{color}" flood-opacity="1" result="flood"/>
      <feComposite in="flood" in2="SourceGraphic" operator="in" result="coloredCore"/>
      <feGaussianBlur in="coloredCore" stdDeviation="{halo_std[level]}" result="halo"/>
      <feGaussianBlur in="coloredCore" stdDeviation="{blur_std[level]}" result="softBlur"/>
      <feMerge>
        <feMergeNode in="halo"/>
        <feMergeNode in="softBlur"/>
        <feMergeNode in="coloredCore"/>
      </feMerge>
    </filter>''')

    filters.append(f'''
    <filter id="hot-core" x="-200%" y="-200%" width="500%" height="500%">
      <feFlood flood-color="{HOT_CORE_COLOR}" flood-opacity="0.85" result="flood"/>
      <feComposite in="flood" in2="SourceGraphic" operator="in" result="coloredCore"/>
      <feGaussianBlur in="coloredCore" stdDeviation="0.8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="coloredCore"/>
      </feMerge>
    </filter>''')

    filters.append(f'''
    <filter id="scan-bar-glow" x="-300%" y="-50%" width="700%" height="200%">
      <feFlood flood-color="{SCAN_BAR_COLOR}" flood-opacity="1" result="flood"/>
      <feComposite in="flood" in2="SourceGraphic" operator="in" result="core"/>
      <feGaussianBlur in="core" stdDeviation="3.2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="core"/>
      </feMerge>
    </filter>''')

    return "\n".join(filters)


def build_defs_extras(width, height):
    """Scanline pattern + vignette gradient, shared across the whole grid."""
    return f'''
    <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="4" fill="transparent"/>
      <rect width="4" height="1" fill="{SCANLINE_COLOR}" opacity="0.18"/>
    </pattern>
    <radialGradient id="vignette" cx="50%" cy="50%" r="75%">
      <stop offset="55%" stop-color="{VIGNETTE_COLOR}" stop-opacity="0"/>
      <stop offset="100%" stop-color="{VIGNETTE_COLOR}" stop-opacity="0.55"/>
    </radialGradient>'''


def build_cell(week_idx, day_idx, level, num_weeks, num_days, cx, cy, half):
    col_delay = week_idx * (TOTAL_WAVE_DURATION / num_weeks)
    row_offset = (day_idx / num_days) * (TOTAL_WAVE_DURATION / num_weeks) * 0.5
    delay = col_delay + row_offset

    if level == 0:
        pulse_color = LEVEL_COLORS[1]  # dim phosphor shimmer as the scan passes
        return f'''
  <g transform="translate({cx:.2f},{cy:.2f})">
    <rect x="{-half:.2f}" y="{-half:.2f}" width="{CELL_SIZE}" height="{CELL_SIZE}"
      rx="{CELL_RADIUS}" ry="{CELL_RADIUS}" fill="{UNLIT_COLOR}"/>
    <g opacity="0">
      <animate attributeName="opacity" begin="{delay:.3f}s" dur="0.7s"
        values="0;0.85;0" calcMode="spline" keySplines="0.2 0.8 0.3 1;0.4 0 0.6 1" fill="freeze"/>
      <g>
        <animateTransform attributeName="transform" type="scale" begin="{delay:.3f}s"
          dur="0.7s" values="0.5;1.1;0.9" calcMode="spline"
          keySplines="0.25 1 0.4 1;0.4 0 0.6 1" fill="freeze"/>
        <rect x="{-half:.2f}" y="{-half:.2f}" width="{CELL_SIZE}" height="{CELL_SIZE}"
          rx="{CELL_RADIUS}" ry="{CELL_RADIUS}" fill="{pulse_color}" filter="url(#glow-1)"/>
      </g>
    </g>
  </g>'''

    color = LEVEL_COLORS[level]
    flicker_begin = delay + ENTRANCE_DURATION + FLICKER_START_GAP

    core_rect = (
        f'<rect x="{-half:.2f}" y="{-half:.2f}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
        f'rx="{CELL_RADIUS}" ry="{CELL_RADIUS}" fill="{color}" filter="url(#glow-{level})"/>'
    )

    hot_overlay = ""
    if level == 4:
        inset = CELL_SIZE * 0.28
        hot_overlay = (
            f'<rect x="{-half + inset:.2f}" y="{-half + inset:.2f}" '
            f'width="{CELL_SIZE - inset * 2:.2f}" height="{CELL_SIZE - inset * 2:.2f}" '
            f'rx="{max(CELL_RADIUS - 1, 0)}" ry="{max(CELL_RADIUS - 1, 0)}" '
            f'fill="{HOT_CORE_COLOR}" filter="url(#hot-core)"/>'
        )

    flicker_values = "1;1;0.82;1;0.9;1" if level >= 3 else "1;1;0.88;1"

    # Idle re-flicker loop for high-level cells, starts only after boot settles.
    idle_loop = ""
    if level in IDLE_FLICKER_LEVELS:
        # Stagger idle starts per-cell so the whole grid doesn't flicker in
        # sync. SMIL has no clean "wait, then repeat forever" primitive, so
        # this is approximated as one long-period repeating animation whose
        # first cycle absorbs the stagger delay via keyTimes.
        idle_start = flicker_begin + FLICKER_DURATION + 1.0 + (delay * 1.7) % IDLE_FLICKER_PERIOD
        idle_loop = f'''
        <animate attributeName="opacity" begin="{idle_start:.3f}s" dur="{IDLE_FLICKER_PERIOD}s"
          values="1;1;0.7;1;1" keyTimes="0;0.3;0.33;0.36;1"
          calcMode="linear" repeatCount="indefinite" fill="freeze"/>'''

    return f'''
  <g transform="translate({cx:.2f},{cy:.2f})" opacity="0">
    <animate attributeName="opacity" begin="{delay:.3f}s" dur="{ENTRANCE_DURATION}s"
      values="0;1" calcMode="spline" keySplines="0.16 1 0.3 1" fill="freeze"/>
    <g>
      <animateTransform attributeName="transform" type="scale" begin="{delay:.3f}s"
        dur="{ENTRANCE_DURATION}s" values="0.3;1.15;1" keyTimes="0;0.7;1"
        calcMode="spline" keySplines="0.33 0 0.2 1;0.33 0 0.2 1" fill="freeze"/>
      <g>
        {core_rect}
        {hot_overlay}
        <animate attributeName="opacity" begin="{flicker_begin:.3f}s" dur="{FLICKER_DURATION}s"
          values="{flicker_values}" calcMode="linear" repeatCount="1" fill="freeze"/>
        {idle_loop}
      </g>
    </g>
  </g>'''


def build_scan_bar(width, height, num_weeks):
    """A bright vertical raster line that sweeps left-to-right once, matching
    the same timing the cells use to light up column-by-column, then fades."""
    x_start = MARGIN - 4
    x_end = width - MARGIN + 4
    bar_width = 2.5
    fade_start = TOTAL_WAVE_DURATION
    fade_dur = 0.6

    return f'''
  <g opacity="1">
    <rect x="{x_start:.2f}" y="0" width="{bar_width}" height="{height:.2f}"
      fill="{SCAN_BAR_COLOR}" filter="url(#scan-bar-glow)">
      <animate attributeName="x" begin="0s" dur="{TOTAL_WAVE_DURATION}s"
        values="{x_start:.2f};{x_end:.2f}" calcMode="linear" fill="freeze"/>
      <animate attributeName="opacity" begin="{fade_start:.3f}s" dur="{fade_dur}s"
        values="1;0" calcMode="linear" fill="freeze"/>
    </rect>
  </g>'''


def build_svg(weeks):
    num_weeks = len(weeks)
    if num_weeks == 0:
        raise RuntimeError("No contribution weeks returned by the API.")

    pitch = CELL_SIZE + CELL_GAP
    half = CELL_SIZE / 2

    width = MARGIN * 2 + num_weeks * pitch - CELL_GAP
    height = MARGIN * 2 + 7 * pitch - CELL_GAP

    cells = []
    for week_idx, week in enumerate(weeks):
        for day_idx in range(7):
            level = week[day_idx] if day_idx < len(week) else 0
            cx = MARGIN + week_idx * pitch + half
            cy = MARGIN + day_idx * pitch + half
            cells.append(build_cell(week_idx, day_idx, level, num_weeks, 7, cx, cy, half))

    filters = build_filters()
    defs_extras = build_defs_extras(width, height)
    cells_markup = "\n".join(cells)
    scan_bar = build_scan_bar(width, height, num_weeks)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width:.2f}" height="{height:.2f}"
     viewBox="0 0 {width:.2f} {height:.2f}" role="img" aria-label="GitHub contribution CRT matrix">
  <defs>
{filters}
{defs_extras}
  </defs>
  <rect x="0" y="0" width="{width:.2f}" height="{height:.2f}" fill="{BG_COLOR}"/>
{cells_markup}
{scan_bar}
  <rect x="0" y="0" width="{width:.2f}" height="{height:.2f}" fill="url(#scanlines)" pointer-events="none"/>
  <rect x="0" y="0" width="{width:.2f}" height="{height:.2f}" fill="url(#vignette)" pointer-events="none"/>
</svg>'''
    return svg


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    try:
        weeks = fetch_contribution_weeks(USERNAME, GH_PAT)
        svg = build_svg(weeks)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(svg)
        lit = sum(1 for week in weeks for level in week if level > 0)
        total = sum(len(week) for week in weeks)
        print(
            f"OK: wrote {OUTPUT_FILE} — {len(weeks)} weeks, {total} days, "
            f"{lit} lit LEDs, for user '{USERNAME}'."
        )
    except Exception as exc:  # noqa: BLE001 - top-level script guard
        print(f"FAILED: could not generate {OUTPUT_FILE} — {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
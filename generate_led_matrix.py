#!/usr/bin/env python3
"""
generate_led_matrix.py

Fetches real GitHub contribution data via the GraphQL API and renders it as
an animated "LED matrix" SVG (led_matrix.svg) for embedding in a GitHub
profile README.

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

BG_COLOR = "#050810"
UNLIT_COLOR = "#161b22"

LEVEL_COLORS = {
    1: "#0e4429",
    2: "#006d32",
    3: "#26a641",
    4: "#39d353",
}
HOT_CORE_COLOR = "#c8ffdb"

TOTAL_WAVE_DURATION = 2.4
ENTRANCE_DURATION = 0.5
FLICKER_DURATION = 0.6
FLICKER_START_GAP = 0.15

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
    halo_std = {1: 1.4, 2: 2.0, 3: 2.8, 4: 4.0}

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

    return "\n".join(filters)


def build_cell(week_idx, day_idx, level, num_weeks, num_days, cx, cy, half):
    col_delay = week_idx * (TOTAL_WAVE_DURATION / num_weeks)
    row_offset = (day_idx / num_days) * (TOTAL_WAVE_DURATION / num_weeks) * 0.5
    delay = col_delay + row_offset

    if level == 0:
        return f'''
  <g transform="translate({cx:.2f},{cy:.2f})" opacity="0">
    <animate attributeName="opacity" begin="{delay:.3f}s" dur="0.55s"
      values="0;1" calcMode="spline" keySplines="0.2 0.8 0.3 1" fill="freeze"/>
    <g>
      <animateTransform attributeName="transform" type="scale" begin="{delay:.3f}s"
        dur="0.55s" values="0.55;1" calcMode="spline" keySplines="0.25 1 0.4 1" fill="freeze"/>
      <rect x="{-half:.2f}" y="{-half:.2f}" width="{CELL_SIZE}" height="{CELL_SIZE}"
        rx="{CELL_RADIUS}" ry="{CELL_RADIUS}" fill="{UNLIT_COLOR}">
        <animate attributeName="fill" begin="{delay:.3f}s" dur="0.55s"
          values="#2a3140;{UNLIT_COLOR}" calcMode="spline" keySplines="0.3 0 0.4 1" fill="freeze"/>
      </rect>
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
      </g>
    </g>
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
    cells_markup = "\n".join(cells)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width:.2f}" height="{height:.2f}"
     viewBox="0 0 {width:.2f} {height:.2f}" role="img" aria-label="GitHub contribution LED matrix">
  <defs>
{filters}
  </defs>
  <rect x="0" y="0" width="{width:.2f}" height="{height:.2f}" fill="{BG_COLOR}"/>
{cells_markup}
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
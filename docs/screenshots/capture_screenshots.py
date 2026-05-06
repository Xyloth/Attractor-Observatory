"""Capture polished room screenshots from the running Streamlit app.

Connects to the Control Room at localhost:8765 (started by the Launcher
or `streamlit run`), navigates to each room via the URL anchor wired in
CB-007 (``?room=<id>``), and saves a screenshot to this directory.

Usage::

    python docs/screenshots/capture_screenshots.py

Requires playwright + chromium (``pip install playwright`` then
``python -m playwright install chromium``).
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright


HERE = Path(__file__).resolve().parent
APP_URL = "http://localhost:8765"
VIEWPORT = {"width": 1680, "height": 1050}
WAIT_AFTER_LOAD_MS = 1800


# (room_id, output filename, optional pre-screenshot scroll y)
ROOMS = [
    ("pulse_deck",          "01-pulse-deck.png",          0),
    ("world_observatory",   "02-world-observatory.png",   0),
    ("campaign_command",    "03-campaign-command.png",    0),
    ("ai_operations_tower", "04-ai-operations-tower.png", 0),
    ("project_graph",       "05-project-graph.png",       0),
    ("basin_floor_lab",     "06-basin-floor-lab.png",     0),
    ("doctrine_console",    "07-doctrine-console.png",    0),
]


def main() -> int:
    out_dir = HERE
    out_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        # Use the headless shell already downloaded.
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport=VIEWPORT,
            device_scale_factor=2,  # retina-grade for README crispness
            color_scheme="dark",
        )
        page = context.new_page()

        for room_id, filename, scroll_y in ROOMS:
            url = f"{APP_URL}/?room={room_id}"
            print(f"[capture] {room_id} -> {filename}", flush=True)
            try:
                page.goto(url, wait_until="networkidle", timeout=20000)
            except Exception as exc:
                print(f"[capture]   goto failed: {exc}", flush=True)
                continue
            # Streamlit renders progressively; give plotly + iframes a beat.
            page.wait_for_timeout(WAIT_AFTER_LOAD_MS)
            if scroll_y:
                page.evaluate(f"window.scrollTo(0, {scroll_y})")
                page.wait_for_timeout(400)
            try:
                page.screenshot(
                    path=str(out_dir / filename),
                    full_page=False,  # viewport-only for hero shots
                    type="png",
                )
            except Exception as exc:
                print(f"[capture]   screenshot failed: {exc}", flush=True)
                continue
            print(f"[capture]   wrote {(out_dir / filename).relative_to(HERE.parent.parent)}", flush=True)

        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())

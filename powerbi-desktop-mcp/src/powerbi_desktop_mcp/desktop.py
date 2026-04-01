"""
Power BI Desktop connection manager.

Uses pywinauto with the UIA (UI Automation) backend to connect to a running
Power BI Desktop process. UIA works with WPF/XAML controls by accessibility
name and control type — not screen coordinates — making automation stable
across window resizes and layout changes.

All tool modules import `get_window()` from here. The connection is
re-established on every call (pywinauto handles caching internally).
"""

import os
import subprocess
import time
import logging
from typing import Any

import psutil
from pywinauto import Application
from pywinauto.base_wrapper import BaseWrapper
from pywinauto.timings import TimeoutError as PWTimeoutError

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

PBI_EXE = os.getenv(
    "PBI_DESKTOP_EXE",
    r"C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe",
)

_WINDOW_TITLE_RE = r".*Power BI Desktop.*"


# ── Process checks ────────────────────────────────────────────────────────────

def is_running() -> bool:
    """Return True if PBIDesktop.exe is currently running."""
    return any(
        "PBIDesktop" in p.name()
        for p in psutil.process_iter(["name"])
    )


def get_pid() -> int | None:
    """Return the PID of the running Power BI Desktop process, or None."""
    for p in psutil.process_iter(["name", "pid"]):
        if "PBIDesktop" in p.info["name"]:
            return p.info["pid"]
    return None


# ── Connection ────────────────────────────────────────────────────────────────

def get_app() -> Application:
    """
    Connect to a running Power BI Desktop instance.
    Raises RuntimeError if Power BI Desktop is not running.
    """
    if not is_running():
        raise RuntimeError(
            "Power BI Desktop is not running. "
            "Use launch_powerbi_desktop() to start it first."
        )
    try:
        return Application(backend="uia").connect(
            title_re=_WINDOW_TITLE_RE,
            timeout=10,
        )
    except PWTimeoutError:
        raise RuntimeError(
            "Could not connect to Power BI Desktop window. "
            "The application may be loading — try again in a few seconds."
        )


def get_window() -> BaseWrapper:
    """Return the main Power BI Desktop window wrapper."""
    return get_app().top_window()


def get_window_title() -> str:
    """Return the current window title (includes unsaved-changes indicator)."""
    try:
        return get_window().window_text()
    except Exception:
        return ""


# ── Launch ────────────────────────────────────────────────────────────────────

def launch(exe_path: str | None = None, wait_seconds: int = 15) -> str:
    """
    Launch Power BI Desktop and wait for its window to appear.
    Returns the window title when ready.
    """
    path = exe_path or PBI_EXE
    if is_running():
        return f"Already running: {get_window_title()}"

    logger.info("Launching Power BI Desktop from: %s", path)
    subprocess.Popen([path])

    deadline = time.time() + wait_seconds
    while time.time() < deadline:
        time.sleep(1)
        if is_running():
            # Give the window a moment to fully render
            time.sleep(3)
            return f"Launched: {get_window_title()}"

    raise RuntimeError(
        f"Power BI Desktop did not start within {wait_seconds}s. "
        f"Check the exe path: {path}"
    )


# ── Helpers shared across tool modules ───────────────────────────────────────

def find_button(name: str, timeout: int = 5) -> BaseWrapper:
    """Find a button anywhere in the main window by its accessible name."""
    win = get_window()
    try:
        return win.child_window(title=name, control_type="Button")
    except Exception:
        raise RuntimeError(
            f"Button '{name}' not found in Power BI Desktop. "
            "Check that the correct ribbon tab is active."
        )


def send_keys(keys: str) -> None:
    """Send keyboard input to the Power BI Desktop window."""
    win = get_window()
    win.set_focus()
    win.type_keys(keys, with_spaces=True)


def wait_for_dialog(title_re: str, timeout: int = 10) -> BaseWrapper:
    """Wait for a dialog window to appear and return it."""
    app = get_app()
    try:
        app.wait_cpu_usage_lower(threshold=5, timeout=timeout)
        return app.window(title_re=title_re)
    except PWTimeoutError:
        raise RuntimeError(f"Dialog matching '{title_re}' did not appear within {timeout}s.")

"""
MCP tools: Report canvas interactions and visual management.

The Power BI Desktop report canvas is a custom WPF surface. pywinauto can
locate the canvas container by control type and get its bounding rectangle.
Visual interactions use canvas-relative coordinates (% of canvas size) which
remain stable as the window is resized — unlike absolute screen coordinates.

Screenshots use Pillow to capture the canvas region from the screen.
"""

import base64
import io
import json
import time
from typing import Any

from mcp.server import FastMCP
from .. import desktop


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    def list_canvas_visuals() -> str:
        """
        List all visual containers currently on the report canvas by walking
        the UIA accessibility tree within the canvas area. Returns each visual's
        accessible name, control type, and bounding rectangle.

        Note: Power BI Desktop assigns names like 'Card' or 'Bar chart' to
        visual containers. The exact naming depends on the visual type and any
        title set by the report author.
        """
        win = desktop.get_window()
        win.set_focus()
        visuals = []
        try:
            canvas = _find_canvas(win)
            for child in canvas.descendants(control_type="Custom"):
                name = child.window_text()
                rect = child.rectangle()
                visuals.append({
                    "name": name,
                    "control_type": child.element_info.control_type,
                    "bounds": {
                        "left": rect.left, "top": rect.top,
                        "right": rect.right, "bottom": rect.bottom,
                        "width": rect.width(), "height": rect.height(),
                    },
                })
        except Exception as e:
            return json.dumps({"error": str(e), "visuals": []})
        return json.dumps({"visual_count": len(visuals), "visuals": visuals})

    @mcp.tool()
    def select_visual(visual_name: str) -> str:
        """
        Click a visual on the report canvas to select it. After selection,
        the Visualizations and Format panes update to show that visual's settings.

        Args:
            visual_name: Accessible name of the visual (from list_canvas_visuals).
        """
        win = desktop.get_window()
        win.set_focus()
        try:
            canvas = _find_canvas(win)
            visual = canvas.child_window(title=visual_name, control_type="Custom")
            visual.click_input()
            time.sleep(0.3)
            return json.dumps({"status": "ok", "selected": visual_name})
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    def click_canvas_position(x_percent: float, y_percent: float) -> str:
        """
        Click at a position on the report canvas specified as a percentage of
        canvas width and height (0.0–1.0). This is more stable than absolute
        screen coordinates because it adapts to window size.

        Use list_canvas_visuals() to find named visuals instead when possible.

        Args:
            x_percent: Horizontal position as fraction of canvas width (0.0 = left, 1.0 = right).
            y_percent: Vertical position as fraction of canvas height (0.0 = top, 1.0 = bottom).
        """
        win = desktop.get_window()
        win.set_focus()
        canvas = _find_canvas(win)
        rect = canvas.rectangle()
        w = rect.right - rect.left
        h = rect.bottom - rect.top
        cx = int(w * max(0.0, min(1.0, x_percent)))
        cy = int(h * max(0.0, min(1.0, y_percent)))
        canvas.click_input(coords=(cx, cy))
        time.sleep(0.3)
        return json.dumps({
            "status": "ok",
            "canvas_x_percent": x_percent,
            "canvas_y_percent": y_percent,
            "clicked_pixel": {"x": rect.left + cx, "y": rect.top + cy},
        })

    @mcp.tool()
    def delete_selected_visual() -> str:
        """
        Delete the currently selected visual by pressing the Delete key.
        Use select_visual() first to select the target visual.
        """
        win = desktop.get_window()
        win.set_focus()
        win.type_keys("{DELETE}")
        time.sleep(0.3)
        return json.dumps({"status": "ok", "action": "visual_deleted"})

    @mcp.tool()
    def add_field_to_visual(
        table_name: str,
        field_name: str,
        field_well: str = "",
    ) -> str:
        """
        Add a data field to the selected visual by expanding the table in the
        Fields pane and checking (clicking) the field. Power BI automatically
        assigns it to the appropriate field well.

        To assign to a specific well (e.g. 'Axis', 'Values', 'Legend'),
        provide the field_well parameter — this right-clicks the field and
        uses the 'Add to <well>' context menu.

        Args:
            table_name: Table name in the Fields pane (e.g. 'Sales').
            field_name: Field or measure name (e.g. 'Total Revenue').
            field_well: Optional target well name. Leave empty for auto-assign.
        """
        win = desktop.get_window()
        win.set_focus()

        # Ensure Fields pane is visible
        try:
            fields_pane = win.child_window(title="Fields", control_type="Pane")
        except Exception:
            # Toggle Fields pane on
            view_tab = win.child_window(title="View", control_type="TabItem")
            view_tab.click_input()
            time.sleep(0.3)
            fields_btn = win.child_window(title="Fields", control_type="Button")
            fields_btn.click_input()
            time.sleep(0.3)

        # Expand table node
        table_node = win.child_window(title=table_name, control_type="TreeItem")
        if table_node.get_toggle_state() == 0:  # collapsed
            table_node.click_input()
            time.sleep(0.3)

        # Find the field
        field_item = win.child_window(title=field_name, control_type="TreeItem")

        if field_well:
            field_item.right_click_input()
            time.sleep(0.2)
            well_item = win.child_window(
                title_re=f".*{field_well}.*", control_type="MenuItem"
            )
            well_item.click_input()
        else:
            field_item.click_input()

        time.sleep(0.3)
        return json.dumps({
            "status": "ok",
            "table": table_name,
            "field": field_name,
            "well": field_well or "auto",
        })

    @mcp.tool()
    def screenshot_canvas() -> str:
        """
        Take a screenshot of the report canvas area and return it as a
        base64-encoded PNG. Useful for visually inspecting the report state
        or verifying that a visual was added correctly.
        """
        return _capture_region("canvas")

    @mcp.tool()
    def screenshot_fullscreen() -> str:
        """
        Take a screenshot of the entire Power BI Desktop window and return
        it as a base64-encoded PNG.
        """
        return _capture_region("window")

    @mcp.tool()
    def inspect_accessibility_tree(max_depth: int = 3) -> str:
        """
        Dump the UIA accessibility tree of the Power BI Desktop window up to
        a given depth. Useful for discovering control names and types to use
        in other tools when automation needs debugging.

        Args:
            max_depth: How many levels deep to traverse (default 3, max 5).
        """
        win = desktop.get_window()
        win.set_focus()
        depth = max(1, min(max_depth, 5))
        tree = _dump_tree(win, current_depth=0, max_depth=depth)
        return json.dumps(tree, indent=2)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _find_canvas(win: Any) -> Any:
    """Locate the report canvas control in the window."""
    # Try by known title first
    for title in ["Report Canvas", "ReportCanvas", "Canvas"]:
        try:
            c = win.child_window(title=title, control_type="Custom")
            if c.exists(timeout=2):
                return c
        except Exception:
            pass
    # Fall back to first large Custom control (the canvas is typically the largest)
    candidates = win.descendants(control_type="Custom")
    if candidates:
        # Sort by area, take the largest
        def area(c):
            r = c.rectangle()
            return (r.right - r.left) * (r.bottom - r.top)
        return max(candidates, key=area)
    raise RuntimeError(
        "Could not find the report canvas. Ensure Report view is active."
    )


def _capture_region(region: str) -> str:
    """Capture a screen region as base64 PNG. Requires Pillow."""
    from PIL import ImageGrab  # type: ignore

    win = desktop.get_window()
    win.set_focus()
    time.sleep(0.2)

    if region == "canvas":
        try:
            canvas = _find_canvas(win)
            rect = canvas.rectangle()
            bbox = (rect.left, rect.top, rect.right, rect.bottom)
        except Exception:
            rect = win.rectangle()
            bbox = (rect.left, rect.top, rect.right, rect.bottom)
    else:
        rect = win.rectangle()
        bbox = (rect.left, rect.top, rect.right, rect.bottom)

    img = ImageGrab.grab(bbox=bbox)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return json.dumps({
        "format": "png",
        "region": region,
        "width": img.width,
        "height": img.height,
        "image_base64": b64,
    })


def _dump_tree(node: Any, current_depth: int, max_depth: int) -> dict:
    """Recursively dump UIA tree as a dict."""
    info = {
        "name": node.window_text(),
        "control_type": str(node.element_info.control_type),
        "auto_id": getattr(node.element_info, "automation_id", ""),
    }
    if current_depth < max_depth:
        children = []
        try:
            for child in node.children():
                children.append(_dump_tree(child, current_depth + 1, max_depth))
        except Exception:
            pass
        if children:
            info["children"] = children
    return info

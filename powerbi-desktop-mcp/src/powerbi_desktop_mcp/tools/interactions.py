"""
MCP tools: Report viewer interactions.

These tools simulate end-user interactions with a rendered Power BI report:
slicers, filters pane, drill-down/up on visuals, cross-filtering, bookmarks.
They work in Report view and are useful for testing report behaviour or
navigating data during a session.
"""

import json
import time

from mcp.server import FastMCP
from .. import desktop


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    def set_slicer_value(slicer_visual_name: str, value: str) -> str:
        """
        Select a specific value in a slicer visual on the report canvas.
        The slicer must be of type 'list' (single-select or multi-select).

        Args:
            slicer_visual_name: Accessible name of the slicer visual.
            value: The text value to select in the slicer.
        """
        win = desktop.get_window()
        win.set_focus()
        try:
            # Locate the slicer container, then find the item within it
            slicer = win.child_window(
                title=slicer_visual_name, control_type="Custom"
            )
            item = slicer.child_window(title=value, control_type="ListItem")
            item.click_input()
            time.sleep(0.3)
            return json.dumps({
                "status": "ok",
                "slicer": slicer_visual_name,
                "selected_value": value,
            })
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "hint": "Check that the slicer name is exact and the value exists.",
            })

    @mcp.tool()
    def clear_slicer(slicer_visual_name: str) -> str:
        """
        Clear all selections in a slicer visual by clicking its
        'Clear selections' (eraser) icon.

        Args:
            slicer_visual_name: Accessible name of the slicer visual.
        """
        win = desktop.get_window()
        win.set_focus()
        try:
            slicer = win.child_window(
                title=slicer_visual_name, control_type="Custom"
            )
            # The clear button has title "Clear selections" or an eraser icon tooltip
            clear_btn = slicer.child_window(
                title_re=".*[Cc]lear.*", control_type="Button"
            )
            clear_btn.click_input()
            time.sleep(0.3)
            return json.dumps({"status": "ok", "slicer": slicer_visual_name, "action": "cleared"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    def apply_report_filter(field_name: str, values: str) -> str:
        """
        Apply a filter in the Filters pane for a specific field.
        Opens the Filters pane if not visible, finds the field filter card,
        and checks the specified values.

        Args:
            field_name: Name of the field in the Filters pane.
            values: Comma-separated list of values to filter by, e.g. '2023,2024'.
        """
        win = desktop.get_window()
        win.set_focus()

        # Ensure Filters pane is open
        try:
            filters_pane = win.child_window(
                title_re=".*[Ff]ilters.*", control_type="Pane"
            )
            if not filters_pane.is_visible():
                raise Exception("not visible")
        except Exception:
            # Toggle it via ribbon
            view_tab = win.child_window(title="View", control_type="TabItem")
            view_tab.click_input()
            time.sleep(0.3)
            filters_btn = win.child_window(title="Filters", control_type="Button")
            filters_btn.click_input()
            time.sleep(0.5)

        # Find the filter card for the field
        field_card = win.child_window(
            title_re=f".*{field_name}.*", control_type="Group"
        )

        value_list = [v.strip() for v in values.split(",") if v.strip()]
        checked = []
        for val in value_list:
            try:
                item = field_card.child_window(title=val, control_type="CheckBox")
                if item.get_toggle_state() == 0:  # unchecked
                    item.click_input()
                    time.sleep(0.2)
                checked.append(val)
            except Exception:
                pass

        return json.dumps({
            "status": "ok",
            "field": field_name,
            "values_applied": checked,
            "values_requested": value_list,
        })

    @mcp.tool()
    def clear_all_filters() -> str:
        """
        Clear all active filters in the Filters pane by clicking the
        'Clear filter' button at the report level.
        """
        win = desktop.get_window()
        win.set_focus()
        try:
            clear_btn = win.child_window(
                title_re=".*[Cc]lear.*filter.*", control_type="Button"
            )
            clear_btn.click_input()
            time.sleep(0.3)
            return json.dumps({"status": "ok", "action": "all_filters_cleared"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    def drill_down(visual_name: str) -> str:
        """
        Click the drill-down arrow on a visual to drill into the next hierarchy level.
        The visual must have a hierarchy defined (e.g. Year > Quarter > Month).

        Args:
            visual_name: Accessible name of the visual.
        """
        win = desktop.get_window()
        win.set_focus()
        try:
            visual = win.child_window(title=visual_name, control_type="Custom")
            # Hover first to reveal header controls
            visual.move_mouse_input()
            time.sleep(0.3)
            drill_btn = visual.child_window(
                title_re=".*[Dd]rill.*[Dd]own.*", control_type="Button"
            )
            drill_btn.click_input()
            time.sleep(0.5)
            return json.dumps({"status": "ok", "action": "drill_down", "visual": visual_name})
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    def drill_up(visual_name: str) -> str:
        """
        Click the drill-up arrow on a visual to go up one hierarchy level.

        Args:
            visual_name: Accessible name of the visual.
        """
        win = desktop.get_window()
        win.set_focus()
        try:
            visual = win.child_window(title=visual_name, control_type="Custom")
            visual.move_mouse_input()
            time.sleep(0.3)
            drill_btn = visual.child_window(
                title_re=".*[Dd]rill.*[Uu]p.*", control_type="Button"
            )
            drill_btn.click_input()
            time.sleep(0.5)
            return json.dumps({"status": "ok", "action": "drill_up", "visual": visual_name})
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    def expand_all_down(visual_name: str) -> str:
        """
        Click 'Expand all down one level' on a visual hierarchy to show
        all hierarchy members at the next level simultaneously.

        Args:
            visual_name: Accessible name of the visual.
        """
        win = desktop.get_window()
        win.set_focus()
        try:
            visual = win.child_window(title=visual_name, control_type="Custom")
            visual.move_mouse_input()
            time.sleep(0.3)
            expand_btn = visual.child_window(
                title_re=".*[Ee]xpand.*", control_type="Button"
            )
            expand_btn.click_input()
            time.sleep(0.5)
            return json.dumps({"status": "ok", "action": "expand_all_down", "visual": visual_name})
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    def apply_bookmark(bookmark_name: str) -> str:
        """
        Apply a saved bookmark to restore a specific report state (filters,
        selections, page, visual visibility).

        Args:
            bookmark_name: Name of the bookmark as shown in the Bookmarks pane.
        """
        win = desktop.get_window()
        win.set_focus()
        try:
            # Ensure Bookmarks pane is visible
            bm_pane = win.child_window(
                title_re=".*[Bb]ookmarks.*", control_type="Pane"
            )
            if not bm_pane.is_visible():
                view_tab = win.child_window(title="View", control_type="TabItem")
                view_tab.click_input()
                time.sleep(0.3)
                bm_btn = win.child_window(title="Bookmarks", control_type="Button")
                bm_btn.click_input()
                time.sleep(0.3)

            bm_item = win.child_window(
                title=bookmark_name, control_type="ListItem"
            )
            bm_item.click_input()
            time.sleep(0.5)
            return json.dumps({"status": "ok", "bookmark": bookmark_name})
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    def show_data_for_visual(visual_name: str) -> str:
        """
        Right-click a visual and select 'Show as a table' to reveal the
        underlying data in a tabular view below the visual.

        Args:
            visual_name: Accessible name of the visual.
        """
        win = desktop.get_window()
        win.set_focus()
        try:
            visual = win.child_window(title=visual_name, control_type="Custom")
            visual.right_click_input()
            time.sleep(0.3)
            show_data = win.child_window(
                title_re=".*[Ss]how.*[Dd]ata.*|.*[Ss]how as a table.*",
                control_type="MenuItem",
            )
            show_data.click_input()
            time.sleep(0.5)
            return json.dumps({"status": "ok", "visual": visual_name, "action": "show_data"})
        except Exception as e:
            return json.dumps({"error": str(e)})

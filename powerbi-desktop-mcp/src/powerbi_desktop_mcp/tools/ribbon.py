"""
MCP tools: Power BI Desktop ribbon and pane interactions.

The Power BI Desktop ribbon is a standard WPF TabControl. Each tab (Home,
Insert, Modeling, View, Optimize, Help) exposes buttons as UIA Button
controls with accessible names.

All tools here use pywinauto UIA backend — buttons are found by their
accessible title, not screen coordinates.
"""

import json
import time

from mcp.server import FastMCP
from .. import desktop


# Ribbon tab names in Power BI Desktop
_RIBBON_TABS = ["Home", "Insert", "Modeling", "View", "Optimize", "Help"]

# Pane names as they appear in the View ribbon
_PANES = {
    "filters": "Filters",
    "bookmarks": "Bookmarks",
    "fields": "Fields",
    "selection": "Selection",
    "performance analyzer": "Performance analyzer",
    "sync slicers": "Sync slicers",
    "q&a setup": "Q&A setup",
}


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    def click_ribbon_tab(tab_name: str) -> str:
        """
        Activate a ribbon tab in Power BI Desktop.

        Args:
            tab_name: One of 'Home', 'Insert', 'Modeling', 'View', 'Optimize', 'Help'.
        """
        win = desktop.get_window()
        win.set_focus()
        tab = win.child_window(title=tab_name, control_type="TabItem")
        tab.click_input()
        time.sleep(0.3)
        return json.dumps({"status": "ok", "tab": tab_name})

    @mcp.tool()
    def click_ribbon_button(button_name: str, ribbon_tab: str = "") -> str:
        """
        Click a ribbon button in Power BI Desktop by its accessible name.
        Optionally activate a specific tab first.

        Common button names by tab:
          Home:     'New visual', 'Text box', 'More visuals', 'Get data',
                    'Transform data', 'Refresh', 'New measure', 'New column',
                    'New table', 'Manage relationships', 'Publish'
          Insert:   'New visual', 'Text box', 'Buttons', 'Shapes', 'Image',
                    'More visuals', 'Paginated report'
          Modeling: 'New measure', 'New column', 'New table', 'New parameter',
                    'Manage relationships', 'Manage roles', 'View as'
          View:     'Filters', 'Bookmarks', 'Fields', 'Selection',
                    'Performance analyzer', 'Mobile layout', 'Page view',
                    'Gridlines', 'Snap to grid', 'Lock objects', 'Themes'
          Optimize: 'Pause visuals', 'Optimize', 'Optimization presets'

        Args:
            button_name: Accessible name of the button (case-sensitive).
            ribbon_tab: Optional tab to activate first (e.g. 'Insert').
        """
        win = desktop.get_window()
        win.set_focus()

        if ribbon_tab:
            tab = win.child_window(title=ribbon_tab, control_type="TabItem")
            tab.click_input()
            time.sleep(0.3)

        btn = win.child_window(title=button_name, control_type="Button")
        btn.click_input()
        time.sleep(0.3)
        return json.dumps({"status": "ok", "button": button_name})

    @mcp.tool()
    def add_new_visual() -> str:
        """
        Add a blank visual placeholder to the current report page.
        Equivalent to clicking Insert → New visual (or the canvas icon).
        After this, use change_visual_type() to set the visual type,
        then add_field_to_visual() to bind data.
        """
        win = desktop.get_window()
        win.set_focus()
        # Try Insert tab first, fall back to Home
        try:
            tab = win.child_window(title="Insert", control_type="TabItem")
            tab.click_input()
            time.sleep(0.3)
            btn = win.child_window(title="New visual", control_type="Button")
            btn.click_input()
        except Exception:
            tab = win.child_window(title="Home", control_type="TabItem")
            tab.click_input()
            time.sleep(0.3)
            btn = win.child_window(title="New visual", control_type="Button")
            btn.click_input()
        time.sleep(0.5)
        return json.dumps({"status": "ok", "action": "new_visual_added"})

    @mcp.tool()
    def change_visual_type(visual_type_name: str) -> str:
        """
        Change the type of the currently selected visual by clicking its icon
        in the Visualizations pane.

        Common visual type names (accessible labels in the Visualizations pane):
          'Stacked bar chart', 'Clustered bar chart', 'Stacked column chart',
          'Clustered column chart', 'Line chart', 'Area chart',
          'Stacked area chart', 'Line and stacked column chart',
          'Line and clustered column chart', 'Ribbon chart', 'Waterfall chart',
          'Funnel', 'Scatter chart', 'Pie chart', 'Donut chart',
          'Treemap', 'Map', 'Filled map', 'Azure map', 'Decomposition tree',
          'Key influencers', 'Table', 'Matrix', 'Card', 'Multi-row card',
          'KPI', 'Slicer', 'Shape', 'Image', 'Text box', 'Q&A',
          'Smart narrative', 'Paginated report visual', 'R script visual',
          'Python visual', 'ArcGIS Maps for Power BI', 'Gauge'

        Args:
            visual_type_name: Accessible label of the visual icon in the pane.
        """
        win = desktop.get_window()
        win.set_focus()
        # The Visualizations pane contains a group of toggle buttons for visual types
        vis_btn = win.child_window(
            title=visual_type_name, control_type="Button"
        )
        vis_btn.click_input()
        time.sleep(0.3)
        return json.dumps({"status": "ok", "visual_type": visual_type_name})

    @mcp.tool()
    def toggle_pane(pane_name: str) -> str:
        """
        Show or hide a side panel via the View ribbon tab.

        Args:
            pane_name: One of 'Filters', 'Bookmarks', 'Fields', 'Selection',
                       'Performance analyzer', 'Sync slicers', 'Q&A setup'.
        """
        win = desktop.get_window()
        win.set_focus()
        view_tab = win.child_window(title="View", control_type="TabItem")
        view_tab.click_input()
        time.sleep(0.3)

        # Panes are toggle buttons in the View ribbon
        pane_btn = win.child_window(title=pane_name, control_type="Button")
        pane_btn.click_input()
        time.sleep(0.3)
        return json.dumps({"status": "ok", "pane": pane_name, "action": "toggled"})

    @mcp.tool()
    def undo() -> str:
        """Undo the last action in Power BI Desktop (Ctrl+Z)."""
        desktop.send_keys("^z")
        time.sleep(0.3)
        return json.dumps({"status": "ok", "action": "undo"})

    @mcp.tool()
    def redo() -> str:
        """Redo the last undone action in Power BI Desktop (Ctrl+Y)."""
        desktop.send_keys("^y")
        time.sleep(0.3)
        return json.dumps({"status": "ok", "action": "redo"})

    @mcp.tool()
    def list_ribbon_tabs() -> str:
        """
        List all available ribbon tabs in the current Power BI Desktop window.
        Useful for discovering what tabs are present in the current version.
        """
        win = desktop.get_window()
        win.set_focus()
        tabs = []
        for tab_name in _RIBBON_TABS:
            try:
                t = win.child_window(title=tab_name, control_type="TabItem")
                tabs.append({"name": tab_name, "found": t.exists()})
            except Exception:
                tabs.append({"name": tab_name, "found": False})
        return json.dumps({"tabs": tabs})

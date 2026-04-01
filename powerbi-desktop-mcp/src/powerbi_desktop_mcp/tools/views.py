"""
MCP tools: View switching and page management in Power BI Desktop.

Power BI Desktop has three main views (Report, Data, Model) accessible via
icons in the left sidebar. Report pages are tabs at the bottom of the canvas.
"""

import json
import time

from mcp.server import FastMCP
from .. import desktop


# Left-sidebar view button accessible names
_VIEW_BUTTONS = {
    "report": "Report view",
    "data": "Data view",
    "model": "Model view",
}


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    def switch_view(view: str) -> str:
        """
        Switch between the three main views in Power BI Desktop.

        Args:
            view: One of 'report', 'data', or 'model' (case-insensitive).
        """
        key = view.lower().strip()
        if key not in _VIEW_BUTTONS:
            return json.dumps({
                "error": f"Unknown view '{view}'. Use: report, data, model."
            })
        win = desktop.get_window()
        win.set_focus()
        btn_title = _VIEW_BUTTONS[key]
        btn = win.child_window(title=btn_title, control_type="Button")
        btn.click_input()
        time.sleep(0.5)
        return json.dumps({"status": "ok", "view": key})

    @mcp.tool()
    def list_report_pages() -> str:
        """
        List all page tabs at the bottom of the report canvas.
        Returns page names in order. Use navigate_to_page() to switch pages.
        """
        win = desktop.get_window()
        win.set_focus()
        # Page tabs are TabItem controls in a TabControl at the bottom
        pages = []
        try:
            # Try to find the page bar tab control
            tab_ctrl = win.child_window(control_type="TabControl", found_index=0)
            for item in tab_ctrl.children(control_type="TabItem"):
                name = item.window_text()
                if name and name != "+":
                    pages.append(name)
        except Exception:
            # Fallback: enumerate all TabItems in the window
            for item in win.descendants(control_type="TabItem"):
                name = item.window_text()
                if name and name not in _VIEW_BUTTONS.values() and "+" not in name:
                    pages.append(name)

        return json.dumps({"page_count": len(pages), "pages": pages})

    @mcp.tool()
    def navigate_to_page(page_name: str) -> str:
        """
        Switch to a specific report page by clicking its tab at the bottom
        of the canvas.

        Args:
            page_name: Exact name of the page tab (e.g. 'Overview', 'Page 1').
        """
        win = desktop.get_window()
        win.set_focus()
        tab = win.child_window(title=page_name, control_type="TabItem")
        tab.click_input()
        time.sleep(0.3)
        return json.dumps({"status": "ok", "page": page_name})

    @mcp.tool()
    def add_report_page() -> str:
        """
        Add a new blank page to the report by clicking the '+' tab button
        at the bottom of the canvas.
        """
        win = desktop.get_window()
        win.set_focus()
        # The new page button is a '+' TabItem or a Button near the page tabs
        try:
            add_btn = win.child_window(title="+", control_type="TabItem")
            add_btn.click_input()
        except Exception:
            # Some versions use a Button with tooltip "New page"
            add_btn = win.child_window(title="New page", control_type="Button")
            add_btn.click_input()
        time.sleep(0.5)
        return json.dumps({
            "status": "ok",
            "action": "page_added",
            "window_title": desktop.get_window_title(),
        })

    @mcp.tool()
    def rename_report_page(current_name: str, new_name: str) -> str:
        """
        Rename a report page by double-clicking its tab and typing a new name.

        Args:
            current_name: Current tab name (e.g. 'Page 1').
            new_name: Desired new name (e.g. 'Sales Overview').
        """
        win = desktop.get_window()
        win.set_focus()

        # Double-click the page tab to enter rename mode
        tab = win.child_window(title=current_name, control_type="TabItem")
        tab.double_click_input()
        time.sleep(0.3)

        # Select all existing text and type the new name
        desktop.send_keys("^a")
        time.sleep(0.1)
        # type_keys with special chars needs careful escaping
        win.type_keys(new_name, with_spaces=True)
        time.sleep(0.1)
        desktop.send_keys("{ENTER}")
        time.sleep(0.3)
        return json.dumps({"status": "ok", "old_name": current_name, "new_name": new_name})

    @mcp.tool()
    def delete_report_page(page_name: str) -> str:
        """
        Delete a report page by right-clicking its tab and selecting Delete.
        Cannot delete the last remaining page.

        Args:
            page_name: Name of the page to delete.
        """
        win = desktop.get_window()
        win.set_focus()
        tab = win.child_window(title=page_name, control_type="TabItem")
        tab.right_click_input()
        time.sleep(0.3)
        delete_item = win.child_window(title="Delete page", control_type="MenuItem")
        delete_item.click_input()
        time.sleep(0.3)
        # Confirm if a dialog appears
        try:
            confirm_btn = win.child_window(title="Delete", control_type="Button")
            if confirm_btn.exists(timeout=2):
                confirm_btn.click_input()
        except Exception:
            pass
        return json.dumps({"status": "ok", "deleted_page": page_name})

    @mcp.tool()
    def duplicate_report_page(page_name: str) -> str:
        """
        Duplicate a report page by right-clicking its tab and selecting
        'Duplicate page'.

        Args:
            page_name: Name of the page to duplicate.
        """
        win = desktop.get_window()
        win.set_focus()
        tab = win.child_window(title=page_name, control_type="TabItem")
        tab.right_click_input()
        time.sleep(0.3)
        dup_item = win.child_window(title="Duplicate page", control_type="MenuItem")
        dup_item.click_input()
        time.sleep(0.5)
        return json.dumps({"status": "ok", "duplicated_from": page_name})

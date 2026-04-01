"""
MCP tools: File operations for Power BI Desktop.

Covers: launch, connect, open file, save, save as, new report, publish to service.
All file dialog interactions use pywinauto to type paths into the Windows
Open/Save dialog — no coordinate clicking.
"""

import json
import os
import time

from mcp.server import FastMCP
from .. import desktop


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    def get_powerbi_status() -> str:
        """
        Check if Power BI Desktop is running and return its current window title.
        The title includes the open report name and an asterisk (*) if there are
        unsaved changes. Use this as a health-check before other tools.
        """
        if not desktop.is_running():
            return json.dumps({
                "running": False,
                "pid": None,
                "window_title": None,
                "message": "Power BI Desktop is not running.",
            })
        pid = desktop.get_pid()
        title = desktop.get_window_title()
        return json.dumps({
            "running": True,
            "pid": pid,
            "window_title": title,
            "has_unsaved_changes": "*" in title,
        })

    @mcp.tool()
    def launch_powerbi_desktop(exe_path: str = "") -> str:
        """
        Launch Power BI Desktop and wait for it to be ready.
        If it is already running, returns the current window title.

        Args:
            exe_path: Full path to PBIDesktop.exe. Leave empty to use the
                      PBI_DESKTOP_EXE environment variable or the default
                      installation path.
        """
        result = desktop.launch(exe_path or None)
        return json.dumps({"status": "ready", "message": result})

    @mcp.tool()
    def new_report() -> str:
        """
        Create a new blank report in Power BI Desktop (File → New).
        If the current report has unsaved changes, Power BI will prompt to save —
        handle that with save_report first if needed.
        """
        win = desktop.get_window()
        win.set_focus()
        # Use keyboard shortcut: Ctrl+N is not standard in PBI, use File menu
        file_btn = win.child_window(title="File", control_type="Button")
        file_btn.click_input()
        time.sleep(0.3)
        new_item = win.child_window(title="New", control_type="MenuItem")
        new_item.click_input()
        time.sleep(1)
        return json.dumps({
            "status": "ok",
            "window_title": desktop.get_window_title(),
        })

    @mcp.tool()
    def open_pbix_file(file_path: str) -> str:
        """
        Open a Power BI report file (.pbix or PBIR folder) in Power BI Desktop
        via File → Open. The file must exist on the Windows machine.

        Args:
            file_path: Full Windows path, e.g. C:\\Reports\\SalesReport.pbix
                       or C:\\Reports\\MyReport (for a PBIR folder).
        """
        win = desktop.get_window()
        win.set_focus()

        # File → Open
        file_btn = win.child_window(title="File", control_type="Button")
        file_btn.click_input()
        time.sleep(0.3)
        open_item = win.child_window(title="Open", control_type="MenuItem")
        open_item.click_input()
        time.sleep(0.5)

        # The Windows Open dialog
        open_dlg = desktop.wait_for_dialog(r".*Open.*", timeout=8)
        # Type the path directly into the filename field
        filename_field = open_dlg.child_window(
            title="File name:", control_type="Edit"
        )
        filename_field.set_text(file_path)
        time.sleep(0.2)
        open_btn = open_dlg.child_window(title="Open", control_type="Button")
        open_btn.click_input()

        # Wait for Power BI to finish loading the file
        time.sleep(4)
        return json.dumps({
            "status": "ok",
            "file_path": file_path,
            "window_title": desktop.get_window_title(),
        })

    @mcp.tool()
    def save_report() -> str:
        """
        Save the current report (Ctrl+S). Fast and non-interactive.
        If the report has never been saved, Power BI will open a Save As dialog —
        use save_report_as() instead for new files.
        """
        desktop.send_keys("^s")
        time.sleep(1)
        return json.dumps({
            "status": "ok",
            "window_title": desktop.get_window_title(),
        })

    @mcp.tool()
    def save_report_as(file_path: str) -> str:
        """
        Save the current report to a new path via File → Save As.
        Creates or overwrites the file at the specified Windows path.

        Args:
            file_path: Full Windows path for the new file, e.g.
                       C:\\Reports\\NewReport.pbix
        """
        win = desktop.get_window()
        win.set_focus()

        file_btn = win.child_window(title="File", control_type="Button")
        file_btn.click_input()
        time.sleep(0.3)
        saveas_item = win.child_window(title="Save as", control_type="MenuItem")
        saveas_item.click_input()
        time.sleep(0.5)

        save_dlg = desktop.wait_for_dialog(r".*Save.*", timeout=8)
        filename_field = save_dlg.child_window(
            title="File name:", control_type="Edit"
        )
        filename_field.set_text(file_path)
        time.sleep(0.2)
        save_btn = save_dlg.child_window(title="Save", control_type="Button")
        save_btn.click_input()

        time.sleep(2)
        return json.dumps({
            "status": "ok",
            "file_path": file_path,
            "window_title": desktop.get_window_title(),
        })

    @mcp.tool()
    def publish_to_service(workspace_name: str = "") -> str:
        """
        Publish the current report to Power BI Service via Home → Publish.
        A workspace selection dialog will appear — this tool selects the first
        matching workspace by name, or the first option if no name is given.

        Args:
            workspace_name: Name of the destination workspace (partial match OK).
                            Leave empty to select the first available workspace.
        """
        win = desktop.get_window()
        win.set_focus()

        # Ensure Home tab is active
        home_tab = win.child_window(title="Home", control_type="TabItem")
        home_tab.click_input()
        time.sleep(0.3)

        publish_btn = win.child_window(title="Publish", control_type="Button")
        publish_btn.click_input()
        time.sleep(1)

        # Workspace selection dialog
        try:
            ws_dlg = desktop.wait_for_dialog(r".*Publish.*", timeout=10)
            if workspace_name:
                ws_item = ws_dlg.child_window(
                    title_re=f".*{workspace_name}.*",
                    control_type="ListItem",
                )
            else:
                ws_item = ws_dlg.child_window(control_type="ListItem", found_index=0)
            ws_item.click_input()
            time.sleep(0.2)
            select_btn = ws_dlg.child_window(title="Select", control_type="Button")
            select_btn.click_input()
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Workspace dialog error: {e}. "
                           "The report may still publish — check Power BI Service.",
            })

        # Wait for publish to complete (success dialog)
        time.sleep(5)
        return json.dumps({
            "status": "ok",
            "workspace": workspace_name or "(first available)",
            "message": "Publish initiated. Check Power BI Service for the result.",
        })

    @mcp.tool()
    def close_report() -> str:
        """
        Close the current report via File → Close. If there are unsaved changes,
        Power BI will prompt — save first with save_report() if needed.
        """
        win = desktop.get_window()
        win.set_focus()
        file_btn = win.child_window(title="File", control_type="Button")
        file_btn.click_input()
        time.sleep(0.3)
        close_item = win.child_window(title="Close", control_type="MenuItem")
        close_item.click_input()
        time.sleep(1)
        return json.dumps({"status": "ok", "window_title": desktop.get_window_title()})

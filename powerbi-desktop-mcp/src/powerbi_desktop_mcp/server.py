"""
Power BI Desktop MCP Server — entry point.

Runs on the Windows machine where Power BI Desktop is installed.
Serves all UI automation tools over SSE (HTTP) so that Claude Code
on a remote Linux machine can connect to it.

Setup (on Windows):
    pip install -e .
    python -m powerbi_desktop_mcp.server
    # or: powerbi-desktop-mcp

Claude Code config (~/.claude.json on Linux):
    {
      "mcpServers": {
        "powerbi-desktop": {
          "type": "sse",
          "url": "http://<windows-machine-ip>:7890/sse"
        }
      }
    }
"""

import logging
import os
import sys

from dotenv import load_dotenv
from mcp.server import FastMCP

from .tools import file_ops, ribbon, views, canvas, interactions

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

PORT = int(os.getenv("PBI_DESKTOP_PORT", "7890"))

mcp = FastMCP(
    name="powerbi-desktop-mcp",
    instructions=(
        "MCP server for Power BI Desktop UI automation. "
        "Runs on the Windows machine hosting Power BI Desktop and uses "
        "the Windows UI Automation (UIA) accessibility API to interact with "
        "every UI element by name — not by screen coordinates.\n\n"
        "WORKFLOW for creating a report from scratch:\n"
        "1. get_powerbi_status → confirm Power BI Desktop is running\n"
        "2. new_report (or open_pbix_file with a PBIR template)\n"
        "3. add_new_visual → adds a blank visual placeholder\n"
        "4. change_visual_type('Bar chart') → set the visual type\n"
        "5. add_field_to_visual('Sales', 'Category') → bind data\n"
        "6. save_report_as('C:\\\\Reports\\\\MyReport.pbix')\n"
        "7. publish_to_service('My Workspace')\n\n"
        "WORKFLOW for viewer interactions:\n"
        "1. open_pbix_file → open the target report\n"
        "2. navigate_to_page('Overview') → go to the right page\n"
        "3. set_slicer_value / apply_report_filter → filter data\n"
        "4. drill_down / drill_up → explore hierarchies\n"
        "5. screenshot_canvas → capture current state as PNG\n\n"
        "Use inspect_accessibility_tree to debug when a control name is unknown."
    ),
)

# Register all tool groups
file_ops.register(mcp)
ribbon.register(mcp)
views.register(mcp)
canvas.register(mcp)
interactions.register(mcp)

logger.info("Power BI Desktop MCP ready — %d tools registered", len(mcp.list_tools()))


def main() -> None:
    logger.info("Starting SSE server on port %d", PORT)
    mcp.run(transport="sse", host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()

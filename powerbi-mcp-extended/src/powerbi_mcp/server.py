"""
Power BI MCP Extended — server entry point.

Registers all tool modules and starts the MCP server over stdio.

Usage:
    python -m powerbi_mcp.server
    # or after installing the package:
    powerbi-mcp
"""

import logging
import sys

from mcp.server import FastMCP

from .tools import workspaces, reports, dashboards, datasets, dax, analysis, report_builder, ai_assistant

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

mcp = FastMCP(
    name="powerbi-mcp-extended",
    instructions=(
        "Advanced Power BI MCP server extending Microsoft's official semantic modeling MCP. "
        "Provides REST API tools (workspaces, reports, dashboards, datasets, refresh), "
        "advanced DAX intelligence (benchmarking, dependency analysis, optimization suggestions), "
        "and data analysis tools (column profiling, sampling, custom DAX queries). "
        "\n\n"
        "Authentication: set PBI_AUTH_MODE=service_principal (default) or interactive. "
        "Required env vars: PBI_TENANT_ID, PBI_CLIENT_ID, PBI_CLIENT_SECRET (SP mode). "
        "\n\n"
        "This server complements microsoft/powerbi-modeling-mcp which handles semantic model "
        "write operations (create tables, measures, relationships). Use both together for "
        "full coverage.\n\n"
        "PBIR Report Builder: create_report_definition → add_page_to_report → "
        "add_visual_to_page → save_report_as_pbir → open with powerbi-desktop-mcp.\n\n"
        "AI Assistant (requires ANTHROPIC_API_KEY): generate_dax_measure (natural language "
        "→ DAX), suggest_report_layout (schema → page/visual plan), "
        "analyze_report_screenshot (vision analysis of canvas PNG), "
        "optimize_dax_with_ai (deep AI-driven DAX optimization), "
        "chat_with_data (NL Q&A → auto-generated EVALUATE query)."
    ),
)

# Register all tool groups
workspaces.register(mcp)
reports.register(mcp)
dashboards.register(mcp)
datasets.register(mcp)
dax.register(mcp)
analysis.register(mcp)
report_builder.register(mcp)
ai_assistant.register(mcp)

logger.info("Registered %d tools", len(mcp.list_tools()))


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

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

from .tools import workspaces, reports, dashboards, datasets, dax, analysis

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
        "full coverage."
    ),
)

# Register all tool groups
workspaces.register(mcp)
reports.register(mcp)
dashboards.register(mcp)
datasets.register(mcp)
dax.register(mcp)
analysis.register(mcp)

logger.info("Registered %d tools", len(mcp.list_tools()))


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

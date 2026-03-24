"""MCP tools: dashboard and tile management."""

import json
from mcp.server import FastMCP
from .. import client


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    async def list_dashboards(workspace_id: str) -> str:
        """
        List all dashboards in a Power BI workspace.

        Args:
            workspace_id: The GUID of the workspace.
        """
        results = await client.list_dashboards(workspace_id)
        return json.dumps(results, indent=2)

    @mcp.tool()
    async def get_dashboard_tiles(workspace_id: str, dashboard_id: str) -> str:
        """
        Get all tiles pinned to a Power BI dashboard, including the report/dataset
        each tile is sourced from.

        Args:
            workspace_id: The GUID of the workspace.
            dashboard_id: The GUID of the dashboard.
        """
        results = await client.get_dashboard_tiles(workspace_id, dashboard_id)
        # Enrich with a summary
        summary = {
            "tile_count": len(results),
            "tiles": results,
        }
        return json.dumps(summary, indent=2)

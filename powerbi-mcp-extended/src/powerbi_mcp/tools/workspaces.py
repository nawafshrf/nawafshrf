"""MCP tools: workspace management."""

import json
from mcp.server import FastMCP
from .. import client, config


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    async def list_workspaces(filter: str = "") -> str:
        """
        List Power BI workspaces (groups) accessible to the authenticated identity.

        Args:
            filter: Optional OData $filter expression, e.g. "name eq 'Sales'"
        """
        results = await client.list_workspaces(filter or None)
        return json.dumps(results, indent=2)

    @mcp.tool()
    async def get_workspace(workspace_id: str) -> str:
        """
        Get details of a specific Power BI workspace.

        Args:
            workspace_id: The GUID of the workspace.
        """
        result = await client.get_workspace(workspace_id)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def list_workspace_users(workspace_id: str) -> str:
        """
        List users and their roles in a Power BI workspace.

        Args:
            workspace_id: The GUID of the workspace.
        """
        results = await client.list_workspace_users(workspace_id)
        return json.dumps(results, indent=2)

    @mcp.tool()
    async def list_dataflows(workspace_id: str) -> str:
        """
        List all dataflows in a Power BI workspace.

        Args:
            workspace_id: The GUID of the workspace.
        """
        results = await client.list_dataflows(workspace_id)
        return json.dumps(results, indent=2)

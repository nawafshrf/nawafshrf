"""MCP tools: dataset management, refresh, lineage, and schema."""

import asyncio
import json
from mcp.server import FastMCP
from .. import client


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    async def list_datasets(workspace_id: str) -> str:
        """
        List all datasets in a Power BI workspace with their refresh status
        and configuration details.

        Args:
            workspace_id: The GUID of the workspace.
        """
        results = await client.list_datasets(workspace_id)
        return json.dumps(results, indent=2)

    @mcp.tool()
    async def get_dataset_schema(workspace_id: str, dataset_id: str) -> str:
        """
        Get the full schema of a Power BI dataset: tables, columns (with data types),
        and measures. Useful for understanding the data model before writing DAX.

        Args:
            workspace_id: The GUID of the workspace.
            dataset_id: The GUID of the dataset.
        """
        dataset, tables = await asyncio.gather(
            client.get_dataset(workspace_id, dataset_id),
            client.get_dataset_tables(workspace_id, dataset_id),
        )
        return json.dumps({"dataset": dataset, "tables": tables}, indent=2)


    @mcp.tool()
    async def get_dataset_datasources(workspace_id: str, dataset_id: str) -> str:
        """
        Get the data sources (SQL Server, SharePoint, etc.) connected to a dataset.
        Useful for lineage and impact analysis.

        Args:
            workspace_id: The GUID of the workspace.
            dataset_id: The GUID of the dataset.
        """
        results = await client.get_dataset_datasources(workspace_id, dataset_id)
        return json.dumps(results, indent=2)

    @mcp.tool()
    async def get_dataset_upstream_dataflows(
        workspace_id: str, dataset_id: str
    ) -> str:
        """
        Get the upstream dataflows that feed data into a dataset.
        Useful for data lineage tracking.

        Args:
            workspace_id: The GUID of the workspace.
            dataset_id: The GUID of the dataset.
        """
        results = await client.get_dataset_upstream_dataflows(workspace_id, dataset_id)
        return json.dumps(results, indent=2)

    @mcp.tool()
    async def trigger_dataset_refresh(workspace_id: str, dataset_id: str) -> str:
        """
        Trigger an on-demand data refresh for a Power BI dataset.
        Returns immediately; use get_refresh_history to check completion.

        Args:
            workspace_id: The GUID of the workspace.
            dataset_id: The GUID of the dataset.
        """
        result = await client.trigger_dataset_refresh(workspace_id, dataset_id)
        return json.dumps({
            "message": "Refresh triggered successfully. Use get_refresh_history to monitor progress.",
            "result": result,
        }, indent=2)

    @mcp.tool()
    async def get_refresh_history(
        workspace_id: str, dataset_id: str, top: int = 10
    ) -> str:
        """
        Get the refresh history for a dataset, including start/end times,
        status (Completed/Failed), and error details.

        Args:
            workspace_id: The GUID of the workspace.
            dataset_id: The GUID of the dataset.
            top: Number of most recent refresh entries to return (default 10, max 60).
        """
        results = await client.get_refresh_history(workspace_id, dataset_id, min(top, 60))
        return json.dumps(results, indent=2)

    @mcp.tool()
    async def get_refresh_schedule(workspace_id: str, dataset_id: str) -> str:
        """
        Get the configured refresh schedule for a dataset, showing days of week,
        times, and timezone.

        Args:
            workspace_id: The GUID of the workspace.
            dataset_id: The GUID of the dataset.
        """
        result = await client.get_refresh_schedule(workspace_id, dataset_id)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_dataset_parameters(workspace_id: str, dataset_id: str) -> str:
        """
        Get the query parameters defined in a dataset (e.g. server name, database name).

        Args:
            workspace_id: The GUID of the workspace.
            dataset_id: The GUID of the dataset.
        """
        results = await client.get_dataset_parameters(workspace_id, dataset_id)
        return json.dumps(results, indent=2)


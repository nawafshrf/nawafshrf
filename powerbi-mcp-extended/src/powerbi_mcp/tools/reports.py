"""MCP tools: report management, export, and embed."""

import asyncio
import json
from mcp.server import FastMCP
from .. import client


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    async def list_reports(workspace_id: str) -> str:
        """
        List all reports in a Power BI workspace.

        Args:
            workspace_id: The GUID of the workspace.
        """
        results = await client.list_reports(workspace_id)
        return json.dumps(results, indent=2)

    @mcp.tool()
    async def get_report(workspace_id: str, report_id: str) -> str:
        """
        Get metadata for a specific Power BI report.

        Args:
            workspace_id: The GUID of the workspace.
            report_id: The GUID of the report.
        """
        result = await client.get_report(workspace_id, report_id)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_report_pages(workspace_id: str, report_id: str) -> str:
        """
        List all pages in a Power BI report with their names and display names.

        Args:
            workspace_id: The GUID of the workspace.
            report_id: The GUID of the report.
        """
        results = await client.get_report_pages(workspace_id, report_id)
        return json.dumps(results, indent=2)

    @mcp.tool()
    async def export_report(
        workspace_id: str,
        report_id: str,
        format: str,
        pages: str = "",
    ) -> str:
        """
        Export a Power BI report to PDF, PPTX, PNG, or other formats.
        This tool initiates the export, polls until complete, and returns
        the exported file as a base64-encoded string.

        Args:
            workspace_id: The GUID of the workspace.
            report_id: The GUID of the report.
            format: Export format — 'PDF', 'PPTX', 'PNG', 'XLSX', 'CSV'.
            pages: Comma-separated list of page names to include (empty = all pages).
        """
        page_list = [p.strip() for p in pages.split(",") if p.strip()] if pages else None

        # Initiate export
        job = await client.export_report(workspace_id, report_id, format.upper(), page_list)
        export_id = job.get("id")
        if not export_id:
            return json.dumps({"error": "Export job did not return an ID", "details": job})

        # Poll until done (max 5 min, 10s intervals)
        for attempt in range(30):
            await asyncio.sleep(10)
            status = await client.get_export_status(workspace_id, report_id, export_id)
            pct = status.get("percentComplete", 0)
            state = status.get("status", "")
            if state == "Succeeded":
                break
            if state == "Failed":
                return json.dumps({"error": "Export failed", "details": status})

        if state != "Succeeded":
            return json.dumps({"error": "Export timed out", "last_status": status})

        file_b64 = await client.get_export_file_base64(workspace_id, report_id, export_id)
        return json.dumps({
            "export_id": export_id,
            "format": format.upper(),
            "status": "Succeeded",
            "file_base64": file_b64,
            "note": "Decode the file_base64 field with base64 to get the raw file bytes.",
        })

    @mcp.tool()
    async def generate_embed_token(
        workspace_id: str,
        report_id: str,
        dataset_id: str,
    ) -> str:
        """
        Generate a Power BI embed token for embedding a report in a custom app.
        The token grants view access and is valid for ~60 minutes.

        Args:
            workspace_id: The GUID of the workspace.
            report_id: The GUID of the report.
            dataset_id: The GUID of the dataset backing the report.
        """
        result = await client.generate_embed_token_report(workspace_id, report_id, dataset_id)
        return json.dumps(result, indent=2)

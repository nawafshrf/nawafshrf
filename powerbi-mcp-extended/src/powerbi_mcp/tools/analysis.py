"""
MCP tools: Data analysis using Power BI semantic models.

These tools let an AI agent interrogate the data inside a published dataset
through the Power BI REST API executeQueries endpoint, enabling analysis
without requiring a direct database connection.
"""

import json
from mcp.server import FastMCP
from .. import client


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    async def summarize_dataset(workspace_id: str, dataset_id: str) -> str:
        """
        Produce a high-level summary of a Power BI dataset: table names,
        column counts, data types, and whether the table has any measures.

        Args:
            workspace_id: Workspace GUID.
            dataset_id: Dataset GUID.
        """
        tables = await client.get_dataset_tables(workspace_id, dataset_id)
        summary = []
        for table in tables:
            name = table.get("name", "")
            columns = table.get("columns", [])
            measures = table.get("measures", [])
            summary.append({
                "table": name,
                "column_count": len(columns),
                "measure_count": len(measures),
                "columns": [
                    {"name": c.get("name"), "dataType": c.get("dataType")}
                    for c in columns
                ],
                "measures": [
                    {"name": m.get("name"), "expression": m.get("expression", "")}
                    for m in measures
                ],
            })
        return json.dumps({"table_count": len(summary), "tables": summary}, indent=2)

    @mcp.tool()
    async def sample_table_data(
        workspace_id: str,
        dataset_id: str,
        table_name: str,
        row_limit: int = 100,
    ) -> str:
        """
        Return a sample of rows from a table in a Power BI dataset using DAX.
        Useful for understanding the shape and content of the data.

        Args:
            workspace_id: Workspace GUID.
            dataset_id: Dataset GUID.
            table_name: The exact name of the table in the data model.
            row_limit: Maximum rows to return (default 100, max 1000).
        """
        limit = max(1, min(row_limit, 1000))
        dax = f"EVALUATE TOPN({limit}, '{table_name}')"
        result = await client.execute_dax_query(workspace_id, dataset_id, dax)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def count_table_rows(
        workspace_id: str, dataset_id: str, table_name: str
    ) -> str:
        """
        Count the total number of rows in a table using DAX COUNTROWS.

        Args:
            workspace_id: Workspace GUID.
            dataset_id: Dataset GUID.
            table_name: The exact name of the table.
        """
        dax = f"EVALUATE ROW(\"RowCount\", COUNTROWS('{table_name}'))"
        result = await client.execute_dax_query(workspace_id, dataset_id, dax)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_distinct_values(
        workspace_id: str,
        dataset_id: str,
        table_name: str,
        column_name: str,
        top: int = 50,
    ) -> str:
        """
        Get distinct values in a column (up to `top` values), sorted alphabetically.
        Useful for understanding cardinality and filter options.

        Args:
            workspace_id: Workspace GUID.
            dataset_id: Dataset GUID.
            table_name: The exact name of the table.
            column_name: The exact name of the column.
            top: Maximum distinct values to return (default 50).
        """
        dax = (
            f"EVALUATE TOPN({top}, "
            f"DISTINCT('{table_name}'[{column_name}]), "
            f"'{table_name}'[{column_name}], ASC)"
        )
        result = await client.execute_dax_query(workspace_id, dataset_id, dax)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def analyze_column_profile(
        workspace_id: str,
        dataset_id: str,
        table_name: str,
        column_name: str,
    ) -> str:
        """
        Generate a data profile for a numeric column: count, distinct count,
        min, max, average, and sum. Great for quick data quality checks.

        Args:
            workspace_id: Workspace GUID.
            dataset_id: Dataset GUID.
            table_name: The exact name of the table.
            column_name: The exact name of a numeric column.
        """
        col = f"'{table_name}'[{column_name}]"
        dax = (
            f"EVALUATE ROW(\n"
            f"  \"Count\", COUNTROWS('{table_name}'),\n"
            f"  \"DistinctCount\", DISTINCTCOUNT({col}),\n"
            f"  \"BlankCount\", COUNTBLANK({col}),\n"
            f"  \"Min\", MIN({col}),\n"
            f"  \"Max\", MAX({col}),\n"
            f"  \"Average\", AVERAGE({col}),\n"
            f"  \"Sum\", SUM({col})\n"
            f")"
        )
        result = await client.execute_dax_query(workspace_id, dataset_id, dax)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def run_custom_dax_analysis(
        workspace_id: str,
        dataset_id: str,
        dax_query: str,
    ) -> str:
        """
        Run a fully custom DAX query for exploratory data analysis.
        The query must start with EVALUATE. Use this for joins, groupings,
        time intelligence, and any analysis not covered by the preset tools.

        Examples:
          EVALUATE SUMMARIZECOLUMNS('Date'[Year], "Revenue", [Total Revenue])
          EVALUATE TOPN(10, 'Products', [Sales Amount], DESC)

        Args:
            workspace_id: Workspace GUID.
            dataset_id: Dataset GUID.
            dax_query: A complete DAX query starting with EVALUATE.
        """
        if not dax_query.strip().upper().startswith("EVALUATE"):
            return json.dumps({
                "error": "DAX query must start with EVALUATE.",
                "hint": f"Try: EVALUATE {dax_query.strip()}"
            })
        result = await client.execute_dax_query(workspace_id, dataset_id, dax_query)
        return json.dumps(result, indent=2)

    @mcp.tool()
    async def get_activity_log(
        workspace_id: str,
        start_datetime: str,
        end_datetime: str,
        activity_filter: str = "",
    ) -> str:
        """
        Query the Power BI activity log for audit events in a time range.
        Requires admin permissions (Power BI admin or tenant admin).

        Common activity filters:
          - "activityEventType eq 'ViewReport'"
          - "activityEventType eq 'ExportReport'"
          - "activityEventType eq 'RefreshDataset'"

        Args:
            workspace_id: Workspace GUID (used for scoping, not a REST filter).
            start_datetime: ISO 8601 start, e.g. '2024-01-01T00:00:00'.
            end_datetime: ISO 8601 end, e.g. '2024-01-02T00:00:00'.
            activity_filter: Optional OData filter string.
        """
        events = await client.get_activity_events(
            start_datetime, end_datetime, activity_filter or None
        )
        # Filter to workspace if possible
        if workspace_id:
            events = [e for e in events if e.get("WorkspaceId") == workspace_id]
        return json.dumps({
            "event_count": len(events),
            "events": events,
        }, indent=2)

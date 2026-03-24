"""
Thin async HTTP client wrapping the Power BI REST API and Fabric API.

All methods return plain dicts/lists so MCP tools can serialize them directly.
Tokens are fetched fresh on each request (MSAL handles caching internally).
"""

import asyncio
import base64
import logging
from typing import Any

import httpx

from . import config
from .auth import get_access_token

logger = logging.getLogger(__name__)

_TIMEOUT = httpx.Timeout(60.0, connect=10.0)


def _headers() -> dict[str, str]:
    token = get_access_token()
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


async def _get(url: str, params: dict | None = None) -> Any:
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.get(url, headers=_headers(), params=params)
        resp.raise_for_status()
        return resp.json()


async def _post(url: str, body: dict | None = None) -> Any:
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.post(url, headers=_headers(), json=body or {})
        resp.raise_for_status()
        # Some endpoints return 202 Accepted with no body
        if resp.status_code == 202 or not resp.content:
            return {"status": "accepted"}
        return resp.json()


async def _post_raw(url: str, body: dict | None = None) -> bytes:
    """POST and return raw bytes (used for export endpoints)."""
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.post(url, headers=_headers(), json=body or {})
        resp.raise_for_status()
        return resp.content


async def _delete(url: str) -> dict:
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.delete(url, headers=_headers())
        resp.raise_for_status()
        return {"status": "deleted"}


# ── Workspaces ────────────────────────────────────────────────────────────────

async def list_workspaces(filter: str | None = None) -> list[dict]:
    params = {"$filter": filter} if filter else None
    data = await _get(f"{config.PBI_BASE_URL}/groups", params=params)
    return data.get("value", [])


async def get_workspace(workspace_id: str) -> dict:
    data = await _get(f"{config.PBI_BASE_URL}/groups/{workspace_id}")
    return data


async def list_workspace_users(workspace_id: str) -> list[dict]:
    data = await _get(f"{config.PBI_BASE_URL}/groups/{workspace_id}/users")
    return data.get("value", [])


# ── Reports ───────────────────────────────────────────────────────────────────

async def list_reports(workspace_id: str) -> list[dict]:
    data = await _get(f"{config.PBI_BASE_URL}/groups/{workspace_id}/reports")
    return data.get("value", [])


async def get_report(workspace_id: str, report_id: str) -> dict:
    return await _get(f"{config.PBI_BASE_URL}/groups/{workspace_id}/reports/{report_id}")


async def get_report_pages(workspace_id: str, report_id: str) -> list[dict]:
    data = await _get(
        f"{config.PBI_BASE_URL}/groups/{workspace_id}/reports/{report_id}/pages"
    )
    return data.get("value", [])


async def export_report(
    workspace_id: str,
    report_id: str,
    format: str,
    pages: list[str] | None = None,
) -> dict:
    """
    Initiate an export job. Returns the export job details including exportId.
    Poll get_export_status() until status == 'Succeeded', then call get_export_file().

    format: 'PDF' | 'PPTX' | 'PNG' | 'XLSX' | 'CSV' | 'XML' | 'MHTML'
    """
    body: dict[str, Any] = {"format": format}
    if pages:
        body["powerBIReportConfiguration"] = {
            "pages": [{"pageName": p} for p in pages]
        }
    return await _post(
        f"{config.PBI_BASE_URL}/groups/{workspace_id}/reports/{report_id}/ExportTo",
        body,
    )


async def get_export_status(
    workspace_id: str, report_id: str, export_id: str
) -> dict:
    return await _get(
        f"{config.PBI_BASE_URL}/groups/{workspace_id}/reports/{report_id}"
        f"/exports/{export_id}"
    )


async def get_export_file_base64(
    workspace_id: str, report_id: str, export_id: str
) -> str:
    """Return the exported file content as a base64 string."""
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        resp = await client.get(
            f"{config.PBI_BASE_URL}/groups/{workspace_id}/reports/{report_id}"
            f"/exports/{export_id}/file",
            headers=_headers(),
        )
        resp.raise_for_status()
        return base64.b64encode(resp.content).decode()


async def generate_embed_token_report(
    workspace_id: str, report_id: str, dataset_id: str
) -> dict:
    body = {
        "accessLevel": "view",
        "datasetId": dataset_id,
    }
    return await _post(
        f"{config.PBI_BASE_URL}/groups/{workspace_id}/reports/{report_id}/GenerateToken",
        body,
    )


# ── Dashboards ────────────────────────────────────────────────────────────────

async def list_dashboards(workspace_id: str) -> list[dict]:
    data = await _get(f"{config.PBI_BASE_URL}/groups/{workspace_id}/dashboards")
    return data.get("value", [])


async def get_dashboard_tiles(workspace_id: str, dashboard_id: str) -> list[dict]:
    data = await _get(
        f"{config.PBI_BASE_URL}/groups/{workspace_id}/dashboards/{dashboard_id}/tiles"
    )
    return data.get("value", [])


# ── Datasets ──────────────────────────────────────────────────────────────────

async def list_datasets(workspace_id: str) -> list[dict]:
    data = await _get(f"{config.PBI_BASE_URL}/groups/{workspace_id}/datasets")
    return data.get("value", [])


async def get_dataset(workspace_id: str, dataset_id: str) -> dict:
    return await _get(
        f"{config.PBI_BASE_URL}/groups/{workspace_id}/datasets/{dataset_id}"
    )


async def get_dataset_tables(workspace_id: str, dataset_id: str) -> list[dict]:
    data = await _get(
        f"{config.PBI_BASE_URL}/groups/{workspace_id}/datasets/{dataset_id}/tables"
    )
    return data.get("value", [])


async def get_dataset_datasources(workspace_id: str, dataset_id: str) -> list[dict]:
    data = await _get(
        f"{config.PBI_BASE_URL}/groups/{workspace_id}/datasets/{dataset_id}/datasources"
    )
    return data.get("value", [])


async def trigger_dataset_refresh(workspace_id: str, dataset_id: str) -> dict:
    return await _post(
        f"{config.PBI_BASE_URL}/groups/{workspace_id}/datasets/{dataset_id}/refreshes"
    )


async def get_refresh_history(
    workspace_id: str, dataset_id: str, top: int = 10
) -> list[dict]:
    data = await _get(
        f"{config.PBI_BASE_URL}/groups/{workspace_id}/datasets/{dataset_id}/refreshes",
        params={"$top": top},
    )
    return data.get("value", [])


async def get_refresh_schedule(workspace_id: str, dataset_id: str) -> dict:
    return await _get(
        f"{config.PBI_BASE_URL}/groups/{workspace_id}/datasets/{dataset_id}"
        "/refreshSchedule"
    )


async def execute_dax_query(workspace_id: str, dataset_id: str, dax: str) -> dict:
    """Execute a DAX query against a dataset via Power BI REST API."""
    body = {"queries": [{"query": dax}], "serializerSettings": {"includeNulls": True}}
    return await _post(
        f"{config.PBI_BASE_URL}/groups/{workspace_id}/datasets/{dataset_id}"
        "/executeQueries",
        body,
    )


async def get_dataset_parameters(workspace_id: str, dataset_id: str) -> list[dict]:
    data = await _get(
        f"{config.PBI_BASE_URL}/groups/{workspace_id}/datasets/{dataset_id}/parameters"
    )
    return data.get("value", [])


async def get_dataset_upstream_dataflows(
    workspace_id: str, dataset_id: str
) -> list[dict]:
    data = await _get(
        f"{config.PBI_BASE_URL}/groups/{workspace_id}/datasets/{dataset_id}"
        "/upstreamDataflows"
    )
    return data.get("value", [])


# ── Dataflows ─────────────────────────────────────────────────────────────────

async def list_dataflows(workspace_id: str) -> list[dict]:
    data = await _get(f"{config.PBI_BASE_URL}/groups/{workspace_id}/dataflows")
    return data.get("value", [])


# ── Usage metrics (admin) ─────────────────────────────────────────────────────

async def get_activity_events(
    start_datetime: str, end_datetime: str, filter: str | None = None
) -> list[dict]:
    """
    Fetch audit/activity events.
    start_datetime / end_datetime: ISO 8601 strings, e.g. '2024-01-01T00:00:00'
    """
    params: dict = {
        "startDateTime": f"'{start_datetime}'",
        "endDateTime": f"'{end_datetime}'",
    }
    if filter:
        params["$filter"] = filter
    data = await _get(f"{config.PBI_BASE_URL}/admin/activityevents", params=params)
    return data.get("activityEventEntities", [])

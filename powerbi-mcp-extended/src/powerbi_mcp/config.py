"""Configuration loaded from environment variables / .env file."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Auth ─────────────────────────────────────────────────────────────────────
AUTH_MODE: str = os.getenv("PBI_AUTH_MODE", "service_principal")
TENANT_ID: str = os.getenv("PBI_TENANT_ID", "")
CLIENT_ID: str = os.getenv("PBI_CLIENT_ID", "")
CLIENT_SECRET: str = os.getenv("PBI_CLIENT_SECRET", "")
TOKEN_CACHE_PATH: str = os.getenv("PBI_TOKEN_CACHE_PATH", ".token_cache.json")

# ── Power BI ─────────────────────────────────────────────────────────────────
DEFAULT_WORKSPACE_ID: str = os.getenv("PBI_DEFAULT_WORKSPACE_ID", "")
PBI_BASE_URL: str = "https://api.powerbi.com/v1.0/myorg"
PBI_SCOPE: list[str] = ["https://analysis.windows.net/powerbi/api/.default"]

# ── Fabric (for DAX query execution via REST) ────────────────────────────────
FABRIC_BASE_URL: str = "https://api.fabric.microsoft.com/v1"


def validate() -> None:
    """Raise if required config is missing."""
    missing = []
    for name, value in [("PBI_TENANT_ID", TENANT_ID), ("PBI_CLIENT_ID", CLIENT_ID)]:
        if not value:
            missing.append(name)
    if AUTH_MODE == "service_principal" and not CLIENT_SECRET:
        missing.append("PBI_CLIENT_SECRET")
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Copy .env.example to .env and fill in your values."
        )

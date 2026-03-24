"""
Authentication module supporting both service principal and interactive user auth.

Service principal (PBI_AUTH_MODE=service_principal):
  Uses client credentials flow — no user interaction, ideal for automation.
  Requires: PBI_TENANT_ID, PBI_CLIENT_ID, PBI_CLIENT_SECRET

Interactive (PBI_AUTH_MODE=interactive):
  Uses device code flow — prints a URL+code for the user to authenticate.
  Token is cached on disk to avoid re-login on every run.
  Requires: PBI_TENANT_ID, PBI_CLIENT_ID
"""

import json
import logging
from pathlib import Path

import msal

from . import config

logger = logging.getLogger(__name__)

_app_cache: dict = {}  # module-level cache for MSAL app instances


def _get_authority() -> str:
    return f"https://login.microsoftonline.com/{config.TENANT_ID}"


def _load_token_cache() -> msal.SerializableTokenCache:
    cache = msal.SerializableTokenCache()
    path = Path(config.TOKEN_CACHE_PATH)
    if path.exists():
        cache.deserialize(path.read_text())
    return cache


def _save_token_cache(cache: msal.SerializableTokenCache) -> None:
    if cache.has_state_changed:
        Path(config.TOKEN_CACHE_PATH).write_text(cache.serialize())


def _get_service_principal_app() -> msal.ConfidentialClientApplication:
    key = ("sp", config.CLIENT_ID, config.TENANT_ID)
    if key not in _app_cache:
        _app_cache[key] = msal.ConfidentialClientApplication(
            client_id=config.CLIENT_ID,
            client_credential=config.CLIENT_SECRET,
            authority=_get_authority(),
        )
    return _app_cache[key]


def _get_interactive_app(
    cache: msal.SerializableTokenCache,
) -> msal.PublicClientApplication:
    return msal.PublicClientApplication(
        client_id=config.CLIENT_ID,
        authority=_get_authority(),
        token_cache=cache,
    )


def get_access_token() -> str:
    """Return a valid Bearer token for the Power BI REST API."""
    config.validate()

    if config.AUTH_MODE == "service_principal":
        return _get_sp_token()
    elif config.AUTH_MODE == "interactive":
        return _get_interactive_token()
    else:
        raise ValueError(
            f"Unknown PBI_AUTH_MODE='{config.AUTH_MODE}'. "
            "Use 'service_principal' or 'interactive'."
        )


def _get_sp_token() -> str:
    app = _get_service_principal_app()
    result = app.acquire_token_for_client(scopes=config.PBI_SCOPE)
    _check_result(result)
    return result["access_token"]


def _get_interactive_token() -> str:
    cache = _load_token_cache()
    app = _get_interactive_app(cache)

    # Try silent first (cached token)
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(config.PBI_SCOPE, account=accounts[0])
        if result and "access_token" in result:
            _save_token_cache(cache)
            return result["access_token"]

    # Fall back to device code flow
    flow = app.initiate_device_flow(scopes=config.PBI_SCOPE)
    if "user_code" not in flow:
        raise RuntimeError(f"Device flow initiation failed: {flow.get('error_description')}")

    print("\n" + "=" * 60)
    print("Power BI Interactive Login Required")
    print("=" * 60)
    print(flow["message"])
    print("=" * 60 + "\n")

    result = app.acquire_token_by_device_flow(flow)
    _check_result(result)
    _save_token_cache(cache)
    return result["access_token"]


def _check_result(result: dict) -> None:
    if "access_token" not in result:
        error = result.get("error", "unknown_error")
        desc = result.get("error_description", "No description")
        raise RuntimeError(f"Authentication failed [{error}]: {desc}")

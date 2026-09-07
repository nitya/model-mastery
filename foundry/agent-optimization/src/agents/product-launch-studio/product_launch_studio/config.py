"""Strict environment configuration for local and hosted execution."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping
from urllib.parse import urlparse


class ConfigurationError(ValueError):
    """Raised when startup configuration is missing or inconsistent."""


def _required(values: Mapping[str, str], name: str) -> str:
    value = values.get(name, "").strip()
    if not value:
        raise ConfigurationError(f"Missing required environment variable: {name}")
    return value


def _https_url(values: Mapping[str, str], name: str) -> str:
    value = _required(values, name)
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ConfigurationError(f"{name} must be an absolute HTTPS URL")
    return value.rstrip("/")


@dataclass(frozen=True)
class AppSettings:
    """Resolved app settings. Hosted fields are never inferred or defaulted."""

    mode: str
    project_endpoint: str | None = None
    coordinator_deployment: str | None = None
    analyst_deployment: str | None = None
    strategist_deployment: str | None = None
    copywriter_mode: str | None = None
    copywriter_deployment: str | None = None
    image_deployment: str | None = None
    openai_endpoint: str | None = None
    managed_identity_client_id: str | None = None
    application_insights_connection_string: str | None = None

    @classmethod
    def from_environment(
        cls,
        environ: Mapping[str, str] | None = None,
        *,
        mode_override: str | None = None,
    ) -> "AppSettings":
        values = os.environ if environ is None else environ
        mode = (mode_override or values.get("APP_MODE", "")).strip().lower()
        if mode not in {"local", "hosted"}:
            raise ConfigurationError(
                "APP_MODE must be explicitly set to 'local' or 'hosted'"
            )
        if mode == "local":
            return cls(mode="local")

        copywriter_mode = _required(values, "COPYWRITER_DEPLOYMENT_MODE").lower()
        if copywriter_mode == "fixed":
            copywriter_deployment = _required(
                values, "CAMPAIGN_COPYWRITER_MODEL_DEPLOYMENT_NAME"
            )
        elif copywriter_mode == "routed":
            copywriter_deployment = _required(
                values, "CAMPAIGN_COPYWRITER_ROUTER_DEPLOYMENT_NAME"
            )
        else:
            raise ConfigurationError(
                "COPYWRITER_DEPLOYMENT_MODE must be 'fixed' or 'routed'"
            )

        return cls(
            mode="hosted",
            project_endpoint=_https_url(values, "FOUNDRY_PROJECT_ENDPOINT"),
            coordinator_deployment=_required(
                values, "COORDINATOR_MODEL_DEPLOYMENT_NAME"
            ),
            analyst_deployment=_required(
                values, "PRODUCT_ANALYST_MODEL_DEPLOYMENT_NAME"
            ),
            strategist_deployment=_required(
                values, "CAMPAIGN_STRATEGIST_MODEL_DEPLOYMENT_NAME"
            ),
            copywriter_mode=copywriter_mode,
            copywriter_deployment=copywriter_deployment,
            image_deployment=_required(values, "MAI_IMAGE_MODEL_DEPLOYMENT_NAME"),
            openai_endpoint=_https_url(values, "FOUNDRY_OPENAI_ENDPOINT"),
            managed_identity_client_id=values.get("AZURE_CLIENT_ID") or None,
            application_insights_connection_string=values.get(
                "APPLICATIONINSIGHTS_CONNECTION_STRING"
            )
            or None,
        )

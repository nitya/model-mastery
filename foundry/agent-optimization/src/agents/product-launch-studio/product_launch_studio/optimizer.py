"""Narrow Agent Optimizer integration for copywriter instructions only."""

from __future__ import annotations

from typing import Any


def load_copywriter_config() -> Any:
    try:
        from azure.ai.agentserver.optimization import load_config
    except ImportError as exc:
        raise RuntimeError(
            "Hosted mode requires azure-ai-agentserver-optimization"
        ) from exc

    # No arguments: the SDK resolves .agent_configs/baseline/ and an applied
    # candidate using its supported runtime convention.
    return load_config()

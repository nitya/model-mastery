"""Deterministic adapters used by workshops and unit tests."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Mapping

from .config import AppSettings
from .models import CampaignRequest
from .orchestration import ProductLaunchStudio, Role


class DeterministicRoleRunner:
    """Produces predictable structured handoffs without an LLM."""

    async def run(
        self,
        role: Role,
        instructions: str,
        handoff: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        evidence = handoff["evidence"]
        if role is Role.COORDINATOR:
            return {**handoff, "brief": f"Launch {handoff['product_name']}"}
        if role is Role.ANALYST:
            return {
                **handoff,
                "supported_facts": [
                    {"text": item["statement"], "evidence_ids": [item["id"]]}
                    for item in evidence
                ],
                "gaps": [],
            }
        if role is Role.STRATEGIST:
            return {
                **handoff,
                "strategy": {
                    "audience": handoff["audience"],
                    "channels": handoff["channels"],
                    "message_evidence_ids": [item["id"] for item in evidence],
                },
            }

        first = evidence[0]
        channels = ", ".join(handoff["channels"])
        return {
            **handoff,
            "copy": [
                {
                    "text": (
                        f"{handoff['product_name']} for {handoff['audience']}: "
                        f"{first['statement']}"
                    ),
                    "evidence_ids": [first["id"]],
                },
                {
                    "text": f"Available campaign channels: {channels}. {first['statement']}",
                    "evidence_ids": [first["id"]],
                },
            ],
        }


class DeterministicImageTool:
    """A no-network stand-in with the same semantic result shape as MAI."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    async def generate(self, prompt: str) -> Mapping[str, Any]:
        self.calls.append(prompt)
        digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]
        return {
            "tool": "mai-image-generation",
            "model": "local-deterministic",
            "uri": f"local://mai-image/{digest}.png",
            "prompt": prompt,
        }


def copywriter_instructions() -> str:
    path = (
        Path(__file__).resolve().parent.parent
        / ".agent_configs"
        / "baseline"
        / "instructions.md"
    )
    return path.read_text(encoding="utf-8")


async def run_local_request(
    payload: Mapping[str, Any],
    *,
    settings: AppSettings | None = None,
) -> dict[str, Any]:
    resolved = settings or AppSettings.from_environment(mode_override="local")
    if resolved.mode != "local":
        raise ValueError("run_local_request requires local mode")
    studio = ProductLaunchStudio(
        runner=DeterministicRoleRunner(),
        image_tool=DeterministicImageTool(),
        copywriter_instructions=copywriter_instructions(),
    )
    return await studio.create_campaign(CampaignRequest.from_mapping(payload))

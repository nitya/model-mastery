"""Deterministic, testable orchestration shared by local workshop execution."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Protocol

from .claims import ClaimGuard
from .instructions import (
    ANALYST_INSTRUCTIONS,
    COORDINATOR_INSTRUCTIONS,
    STRATEGIST_INSTRUCTIONS,
)
from .models import CampaignRequest
from .telemetry import span


class Role(str, Enum):
    COORDINATOR = "Campaign Coordinator"
    ANALYST = "Product Analyst"
    STRATEGIST = "Campaign Strategist"
    COPYWRITER = "Campaign Copywriter"


class RoleRunner(Protocol):
    async def run(
        self,
        role: Role,
        instructions: str,
        handoff: Mapping[str, Any],
    ) -> Mapping[str, Any]: ...


class ImageTool(Protocol):
    async def generate(self, prompt: str) -> Mapping[str, Any]: ...


@dataclass
class ProductLaunchStudio:
    runner: RoleRunner
    image_tool: ImageTool
    copywriter_instructions: str
    claim_guard: ClaimGuard = ClaimGuard()

    async def create_campaign(self, request: CampaignRequest) -> dict[str, Any]:
        canonical = request.context_payload()
        handoffs: list[dict[str, Any]] = []
        current: Mapping[str, Any] = canonical

        stages = (
            (Role.COORDINATOR, COORDINATOR_INSTRUCTIONS),
            (Role.ANALYST, ANALYST_INSTRUCTIONS),
            (Role.STRATEGIST, STRATEGIST_INSTRUCTIONS),
            (Role.COPYWRITER, self.copywriter_instructions),
        )
        for role, instructions in stages:
            # Reattach canonical evidence at every boundary. Agent output can
            # enrich the work but can neither erase nor rewrite source facts.
            handoff = {**dict(current), "evidence": canonical["evidence"]}
            with span("product_launch_studio.role", role=role.value):
                output = dict(await self.runner.run(role, instructions, handoff))
            current = {**output, "evidence": canonical["evidence"]}
            handoffs.append({"role": role.value, "payload": dict(current)})

        raw_copy = current.get("copy")
        if not isinstance(raw_copy, list):
            raw_copy = []
        approved_copy = self.claim_guard.validate(
            raw_copy,
            request.evidence,
            allowed_context=(
                request.product_name,
                request.audience,
                *request.channels,
            ),
        )

        image: Mapping[str, Any] | None = None
        if request.request_image:
            prompt = (
                f"Campaign visual for {request.product_name}: "
                + " ".join(item["text"] for item in approved_copy)
            )
            with span("product_launch_studio.image_tool", tool="mai-image-generation"):
                image = await self.image_tool.generate(prompt)

        return {
            "status": "approved",
            "product_name": request.product_name,
            "campaign": approved_copy,
            "evidence": canonical["evidence"],
            "image": dict(image) if image else None,
            "handoffs": handoffs,
        }

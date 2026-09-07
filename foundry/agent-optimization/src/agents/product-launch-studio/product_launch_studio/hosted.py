"""Microsoft Agent Framework Responses host wiring."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from .claims import ClaimGuard
from .config import AppSettings
from .image_tool import MAIImageGenerationTool
from .instructions import (
    ANALYST_INSTRUCTIONS,
    COORDINATOR_INSTRUCTIONS,
    STRATEGIST_INSTRUCTIONS,
)
from .models import CampaignRequest
from .optimizer import load_copywriter_config
from .telemetry import configure_telemetry


def _managed_identity(settings: AppSettings) -> Any:
    from azure.identity import ManagedIdentityCredential

    if settings.managed_identity_client_id:
        return ManagedIdentityCredential(client_id=settings.managed_identity_client_id)
    return ManagedIdentityCredential()


def build_hosted_agent(settings: AppSettings) -> Any:
    """Build a four-role workflow with deterministic evidence enforcement."""
    if settings.mode != "hosted":
        raise ValueError("build_hosted_agent requires hosted settings")

    from agent_framework import Agent, workflow
    from agent_framework.foundry import FoundryChatClient

    configure_telemetry(settings.application_insights_connection_string)
    credential = _managed_identity(settings)
    image_client = MAIImageGenerationTool(
        endpoint=settings.openai_endpoint or "",
        deployment=settings.image_deployment or "",
        credential=credential,
    )

    def client(model: str | None) -> Any:
        if not model:
            raise ValueError("A validated purpose-specific deployment is required")
        return FoundryChatClient(
            project_endpoint=settings.project_endpoint,
            model=model,
            credential=credential,
        )

    copywriter_config = load_copywriter_config()
    copywriter_prompt = copywriter_config.compose_instructions()
    if not copywriter_prompt.strip():
        raise RuntimeError("Agent Optimizer copywriter instructions are empty")

    coordinator = Agent(
        client=client(settings.coordinator_deployment),
        name="campaign_coordinator",
        instructions=COORDINATOR_INSTRUCTIONS,
        default_options={"store": False},
    )
    analyst = Agent(
        client=client(settings.analyst_deployment),
        name="product_analyst",
        instructions=ANALYST_INSTRUCTIONS,
        default_options={"store": False},
    )
    strategist = Agent(
        client=client(settings.strategist_deployment),
        name="campaign_strategist",
        instructions=STRATEGIST_INSTRUCTIONS,
        default_options={"store": False},
    )
    copywriter = Agent(
        client=client(settings.copywriter_deployment),
        name="campaign_copywriter",
        instructions=copywriter_prompt,
        default_options={"store": False},
    )

    def parse_agent_json(text: str, role: str) -> dict[str, Any]:
        candidate = text.strip()
        if candidate.startswith("```"):
            lines = candidate.splitlines()
            candidate = "\n".join(lines[1:-1]).strip()
        try:
            value = json.loads(candidate)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{role} returned invalid JSON") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{role} must return a JSON object")
        return value

    async def run_role(agent: Any, role: str, handoff: dict[str, Any]) -> dict[str, Any]:
        response = await agent.run(json.dumps(handoff))
        return parse_agent_json(response.text, role)

    @workflow
    async def campaign_workflow(request_json: str) -> str:
        request_value = json.loads(request_json)
        if not isinstance(request_value, dict):
            raise ValueError("The request must be a JSON object")
        request = CampaignRequest.from_mapping(request_value)
        canonical = request.context_payload()
        current = canonical

        for role_name, agent in (
            ("Campaign Coordinator", coordinator),
            ("Product Analyst", analyst),
            ("Campaign Strategist", strategist),
            ("Campaign Copywriter", copywriter),
        ):
            handoff = {**current, "evidence": canonical["evidence"]}
            output = await run_role(agent, role_name, handoff)
            # Never accept evidence rewritten or omitted by a model.
            current = {**current, **output, "evidence": canonical["evidence"]}

        copy_items = current.get("copy")
        if not isinstance(copy_items, list):
            raise ValueError("Campaign Copywriter must return a 'copy' list")
        approved = ClaimGuard().validate(
            copy_items,
            request.evidence,
            allowed_context=(
                request.product_name,
                request.audience,
                *request.channels,
            ),
        )

        image = None
        if request.request_image:
            prompt = (
                f"Campaign visual for {request.product_name}: "
                + " ".join(item["text"] for item in approved)
            )
            # MAI remains a tool called after copy validation, never an agent.
            image = await asyncio.to_thread(image_client.generate, prompt)

        return json.dumps(
            {
                "status": "approved",
                "product_name": request.product_name,
                "campaign": approved,
                "evidence": canonical["evidence"],
                "image": image,
            }
        )

    return campaign_workflow.build().as_agent()


def run_responses_server(settings: AppSettings) -> None:
    from agent_framework_foundry_hosting import ResponsesHostServer

    ResponsesHostServer(build_hosted_agent(settings)).run()

import asyncio

from product_launch_studio.local import DeterministicImageTool, DeterministicRoleRunner
from product_launch_studio.models import CampaignRequest
from product_launch_studio.orchestration import ProductLaunchStudio, Role


REQUEST = {
    "product_name": "TrailGlow",
    "audience": "hikers",
    "objective": "launch",
    "channels": ["social"],
    "request_image": True,
    "evidence": [
        {"statement": "TrailGlow weighs 500 grams.", "source": "spec"},
        {"statement": "TrailGlow includes a carry loop.", "source": "spec"},
    ],
}


class RecordingRunner(DeterministicRoleRunner):
    def __init__(self):
        self.calls = []

    async def run(self, role, instructions, handoff):
        self.calls.append((role, handoff))
        result = dict(await super().run(role, instructions, handoff))
        result["evidence"] = [{"id": "BAD", "statement": "invented", "source": "agent"}]
        return result


def test_four_roles_run_in_order_and_evidence_survives_every_handoff():
    runner = RecordingRunner()
    studio = ProductLaunchStudio(runner, DeterministicImageTool(), "grounded")
    result = asyncio.run(studio.create_campaign(CampaignRequest.from_mapping(REQUEST)))

    assert [call[0] for call in runner.calls] == [
        Role.COORDINATOR,
        Role.ANALYST,
        Role.STRATEGIST,
        Role.COPYWRITER,
    ]
    for _, handoff in runner.calls:
        assert [item["id"] for item in handoff["evidence"]] == ["E1", "E2"]
    assert [item["id"] for item in result["evidence"]] == ["E1", "E2"]


def test_image_tool_is_invoked_when_requested():
    image = DeterministicImageTool()
    studio = ProductLaunchStudio(DeterministicRoleRunner(), image, "grounded")
    result = asyncio.run(studio.create_campaign(CampaignRequest.from_mapping(REQUEST)))
    assert len(image.calls) == 1
    assert result["image"]["tool"] == "mai-image-generation"


def test_image_tool_is_not_invoked_when_not_requested():
    image = DeterministicImageTool()
    studio = ProductLaunchStudio(DeterministicRoleRunner(), image, "grounded")
    request = {**REQUEST, "request_image": False}
    result = asyncio.run(studio.create_campaign(CampaignRequest.from_mapping(request)))
    assert image.calls == []
    assert result["image"] is None

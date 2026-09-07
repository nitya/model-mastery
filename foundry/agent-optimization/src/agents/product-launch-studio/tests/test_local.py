import asyncio

from product_launch_studio.config import AppSettings
from product_launch_studio.local import run_local_request


def test_local_mode_needs_no_hosted_environment_or_sdk():
    settings = AppSettings.from_environment({}, mode_override="local")
    result = asyncio.run(
        run_local_request(
            {
                "product_name": "Demo",
                "audience": "beginners",
                "objective": "introduce",
                "channels": ["email"],
                "evidence": ["Demo is available in blue."],
            },
            settings=settings,
        )
    )
    assert result["status"] == "approved"
    assert result["campaign"][0]["evidence_ids"] == ["E1"]

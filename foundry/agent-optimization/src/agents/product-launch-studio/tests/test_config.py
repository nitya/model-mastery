import pytest

from product_launch_studio.config import AppSettings, ConfigurationError


BASE = {
    "APP_MODE": "hosted",
    "FOUNDRY_PROJECT_ENDPOINT": "https://example.services.ai.azure.com/api/projects/demo",
    "COORDINATOR_MODEL_DEPLOYMENT_NAME": "coordinator",
    "PRODUCT_ANALYST_MODEL_DEPLOYMENT_NAME": "analyst",
    "CAMPAIGN_STRATEGIST_MODEL_DEPLOYMENT_NAME": "strategist",
    "COPYWRITER_DEPLOYMENT_MODE": "fixed",
    "CAMPAIGN_COPYWRITER_MODEL_DEPLOYMENT_NAME": "copywriter",
    "MAI_IMAGE_MODEL_DEPLOYMENT_NAME": "mai-image",
    "FOUNDRY_OPENAI_ENDPOINT": "https://example.openai.azure.com/",
}


def test_mode_must_be_explicit():
    with pytest.raises(ConfigurationError, match="APP_MODE"):
        AppSettings.from_environment({})


def test_missing_hosted_value_is_an_explicit_error():
    values = dict(BASE)
    values.pop("PRODUCT_ANALYST_MODEL_DEPLOYMENT_NAME")
    with pytest.raises(
        ConfigurationError, match="PRODUCT_ANALYST_MODEL_DEPLOYMENT_NAME"
    ):
        AppSettings.from_environment(values)


def test_fixed_copywriter_selection_never_uses_router():
    values = {**BASE, "CAMPAIGN_COPYWRITER_ROUTER_DEPLOYMENT_NAME": "router"}
    settings = AppSettings.from_environment(values)
    assert settings.copywriter_mode == "fixed"
    assert settings.copywriter_deployment == "copywriter"


def test_routed_copywriter_selection_never_uses_fixed():
    values = {
        **BASE,
        "COPYWRITER_DEPLOYMENT_MODE": "routed",
        "CAMPAIGN_COPYWRITER_ROUTER_DEPLOYMENT_NAME": "router",
    }
    settings = AppSettings.from_environment(values)
    assert settings.copywriter_mode == "routed"
    assert settings.copywriter_deployment == "router"


def test_routed_mode_does_not_fall_back_to_fixed():
    values = {**BASE, "COPYWRITER_DEPLOYMENT_MODE": "routed"}
    with pytest.raises(
        ConfigurationError, match="CAMPAIGN_COPYWRITER_ROUTER_DEPLOYMENT_NAME"
    ):
        AppSettings.from_environment(values)

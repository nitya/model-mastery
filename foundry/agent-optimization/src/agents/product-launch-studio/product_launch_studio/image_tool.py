"""MAI image-generation implementation used only by hosted execution."""

from __future__ import annotations

from typing import Any


class MAIImageGenerationTool:
    """Calls the configured MAI deployment through Azure OpenAI's Images API."""

    def __init__(self, *, endpoint: str, deployment: str, credential: Any) -> None:
        from azure.identity import get_bearer_token_provider
        from openai import AzureOpenAI

        token_provider = get_bearer_token_provider(
            credential, "https://cognitiveservices.azure.com/.default"
        )
        self._client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_version="2025-04-01-preview",
            azure_ad_token_provider=token_provider,
        )
        self._deployment = deployment

    def generate(self, prompt: str) -> dict[str, Any]:
        result = self._client.images.generate(
            model=self._deployment,
            prompt=prompt,
            n=1,
            size="1024x1024",
        )
        image = result.data[0]
        return {
            "tool": "mai-image-generation",
            "model": self._deployment,
            "url": getattr(image, "url", None),
            "b64_json": getattr(image, "b64_json", None),
            "revised_prompt": getattr(image, "revised_prompt", None),
        }

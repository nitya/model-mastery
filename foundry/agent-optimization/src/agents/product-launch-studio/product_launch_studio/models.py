"""Small, explicit request and evidence models used at every handoff."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class EvidenceItem:
    id: str
    statement: str
    source: str


@dataclass(frozen=True)
class CampaignRequest:
    product_name: str
    audience: str
    objective: str
    channels: tuple[str, ...]
    evidence: tuple[EvidenceItem, ...]
    request_image: bool = False

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "CampaignRequest":
        def required_text(name: str) -> str:
            text = str(value.get(name, "")).strip()
            if not text:
                raise ValueError(f"Request field '{name}' is required")
            return text

        raw_evidence = value.get("evidence")
        if not isinstance(raw_evidence, Sequence) or isinstance(
            raw_evidence, (str, bytes)
        ):
            raise ValueError("Request field 'evidence' must be a non-empty list")

        evidence: list[EvidenceItem] = []
        for index, raw_item in enumerate(raw_evidence, start=1):
            if isinstance(raw_item, str):
                statement, source = raw_item.strip(), "request"
            elif isinstance(raw_item, Mapping):
                statement = str(raw_item.get("statement", "")).strip()
                source = str(raw_item.get("source", "request")).strip() or "request"
            else:
                raise ValueError(f"Evidence item {index} must be text or an object")
            if not statement:
                raise ValueError(f"Evidence item {index} needs a statement")
            evidence.append(EvidenceItem(f"E{index}", statement, source))
        if not evidence:
            raise ValueError("At least one evidence item is required")

        raw_channels = value.get("channels", ["social"])
        if not isinstance(raw_channels, Sequence) or isinstance(
            raw_channels, (str, bytes)
        ):
            raise ValueError("Request field 'channels' must be a list")
        channels = tuple(str(item).strip() for item in raw_channels if str(item).strip())
        if not channels:
            raise ValueError("At least one channel is required")

        return cls(
            product_name=required_text("product_name"),
            audience=required_text("audience"),
            objective=required_text("objective"),
            channels=channels,
            evidence=tuple(evidence),
            request_image=bool(value.get("request_image", False)),
        )

    def evidence_payload(self) -> list[dict[str, str]]:
        return [asdict(item) for item in self.evidence]

    def context_payload(self) -> dict[str, Any]:
        return {
            "product_name": self.product_name,
            "audience": self.audience,
            "objective": self.objective,
            "channels": list(self.channels),
            "request_image": self.request_image,
            "evidence": self.evidence_payload(),
        }

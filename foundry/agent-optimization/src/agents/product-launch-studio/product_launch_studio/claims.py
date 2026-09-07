"""Fail-closed checks for marketing copy before it leaves the studio."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .models import EvidenceItem

_RISKY_PHRASES = (
    "best",
    "guaranteed",
    "number one",
    "#1",
    "clinically proven",
    "zero impact",
    "safest",
    "fastest",
    "most sustainable",
)
_NUMBER = re.compile(r"(?<![A-Za-z])\d+(?:\.\d+)?%?")
_WORDS = re.compile(r"[a-z0-9]+")
_STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "up",
    "with",
}
_SAFE_FRAMING_WORDS = {
    "available",
    "campaign",
    "channels",
    "discover",
    "explore",
    "introducing",
    "learn",
    "meet",
    "product",
    "today",
}


@dataclass(frozen=True)
class ClaimIssue:
    text: str
    reason: str


class ClaimProtectionError(ValueError):
    """Raised when generated copy is not supported by cited evidence."""

    def __init__(self, issues: Sequence[ClaimIssue]):
        self.issues = tuple(issues)
        detail = "; ".join(f"{issue.reason}: {issue.text}" for issue in self.issues)
        super().__init__(f"Campaign copy was blocked: {detail}")


class ClaimGuard:
    """Validates structured copy items against the immutable evidence ledger."""

    def validate(
        self,
        copy_items: Sequence[Mapping[str, Any]],
        evidence: Sequence[EvidenceItem],
        *,
        allowed_context: Sequence[str] = (),
    ) -> list[dict[str, Any]]:
        evidence_by_id = {item.id: item for item in evidence}
        context_words = set(
            _WORDS.findall(" ".join(allowed_context).lower())
        )
        issues: list[ClaimIssue] = []
        validated: list[dict[str, Any]] = []

        if not copy_items:
            issues.append(ClaimIssue("", "at least one copy item is required"))

        for item in copy_items:
            text = str(item.get("text", "")).strip()
            raw_ids = item.get("evidence_ids", [])
            ids = [str(item_id) for item_id in raw_ids] if isinstance(raw_ids, list) else []
            unknown = [item_id for item_id in ids if item_id not in evidence_by_id]
            if not text:
                issues.append(ClaimIssue(text, "copy text is empty"))
                continue
            if not ids:
                issues.append(ClaimIssue(text, "no evidence citation"))
                continue
            if unknown:
                issues.append(
                    ClaimIssue(text, f"unknown evidence citation(s) {', '.join(unknown)}")
                )
                continue

            cited_text = " ".join(evidence_by_id[item_id].statement for item_id in ids)
            cited_lower = cited_text.lower()
            lowered = text.lower()

            for number in _NUMBER.findall(text):
                if number not in cited_text:
                    issues.append(
                        ClaimIssue(text, f"number '{number}' is absent from cited evidence")
                    )
            for phrase in _RISKY_PHRASES:
                if phrase in lowered and phrase not in cited_lower:
                    issues.append(
                        ClaimIssue(text, f"claim phrase '{phrase}' is unsupported")
                    )

            material_words = {
                word for word in _WORDS.findall(lowered) if word not in _STOPWORDS
            }
            cited_words = set(_WORDS.findall(cited_lower))
            unsupported_words = (
                material_words - cited_words - context_words - _SAFE_FRAMING_WORDS
            )
            if unsupported_words:
                issues.append(
                    ClaimIssue(
                        text,
                        "unsupported wording: " + ", ".join(sorted(unsupported_words)),
                    )
                )

            validated.append({"text": text, "evidence_ids": ids})

        if issues:
            raise ClaimProtectionError(issues)
        return validated

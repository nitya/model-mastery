import pytest

from product_launch_studio.claims import ClaimGuard, ClaimProtectionError
from product_launch_studio.models import EvidenceItem


EVIDENCE = (EvidenceItem("E1", "The battery lasted 8 hours in a lab test.", "lab"),)


def test_supported_claim_is_approved():
    result = ClaimGuard().validate(
        [{"text": "The battery lasted 8 hours in a lab test.", "evidence_ids": ["E1"]}],
        EVIDENCE,
    )
    assert result[0]["evidence_ids"] == ["E1"]


@pytest.mark.parametrize(
    "text",
    [
        "The battery lasts 24 hours.",
        "The best battery for every trip.",
        "Guaranteed battery performance.",
    ],
)
def test_unsupported_marketing_claim_is_blocked(text):
    with pytest.raises(ClaimProtectionError):
        ClaimGuard().validate([{"text": text, "evidence_ids": ["E1"]}], EVIDENCE)


def test_unknown_or_missing_evidence_is_blocked():
    with pytest.raises(ClaimProtectionError):
        ClaimGuard().validate(
            [{"text": "The battery lasted 8 hours.", "evidence_ids": ["E9"]}],
            EVIDENCE,
        )


def test_ordinary_but_unsupported_words_are_blocked():
    with pytest.raises(ClaimProtectionError, match="explodes"):
        ClaimGuard().validate(
            [
                {
                    "text": "The battery lasted 8 hours and never explodes.",
                    "evidence_ids": ["E1"],
                }
            ],
            EVIDENCE,
        )

import pandas as pd
import pytest
from pydantic import ValidationError

from support_copilot.data.build import to_contract_rows, validate
from support_copilot.data.contract import SupportTicket
from support_copilot.data.taxonomy import INTENTS


def make_ticket(**overrides):
    """A valid ticket, with any fields replaced by the test."""
    ticket = {
        "ticket_id": "t-1",
        "text": "where is my order",
        "intent": "track_order",
        "source": "bitext",
        "label_source": "bitext",
        "guideline_version": "1.0",
    }
    return {**ticket, **overrides}


def test_valid_ticket_passes():
    SupportTicket.model_validate(make_ticket())


@pytest.mark.parametrize(
    "overrides",
    [
        {"intent": "order_tracking"},  # renamed label
        {"text": ""},  # empty
        {"text": "  hi  "},  # too short once whitespace is stripped
        {"text": "x" * 2001},  # pasted email thread
        {"text": "email me at jane@example.com"},  # unmasked PII
        {"source": "scraped"},  # unknown provenance
        {"surprise_column": 1},  # schema drift
    ],
)
def test_contract_rejects_bad_rows(overrides):
    with pytest.raises(ValidationError):
        SupportTicket.model_validate(make_ticket(**overrides))


def test_taxonomy_has_33_unique_intents():
    assert len(INTENTS) == 33
    assert len(set(INTENTS)) == len(INTENTS)


def test_build_quarantines_bad_rows():
    raw = pd.DataFrame(
        {
            "instruction": ["where is my order", ""],
            "intent": ["track_order", "track_order"],
        }
    )
    passed, failed = validate(to_contract_rows(raw))
    assert len(passed) == 1
    assert len(failed) == 1
    assert "text" in failed.loc[0, "errors"]

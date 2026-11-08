"""Data contract: what every ticket row must look like before we use it."""

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from support_copilot.data.taxonomy import INTENTS

EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


class SupportTicket(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    # What the ticket is
    ticket_id: str = Field(min_length=1)
    text: str = Field(min_length=3, max_length=2000)
    intent: str

    # Provenance: where the row and its label came from
    source: Literal["bitext", "synthetic_llm", "real_ticket"]
    label_source: Literal["bitext", "manual", "llm"]
    guideline_version: str
    generator: str | None = None  # model and prompt version, for synthetic rows

    @field_validator("intent")
    @classmethod
    def intent_in_taxonomy(cls, value: str) -> str:
        if value not in INTENTS:
            raise ValueError(f"unknown intent {value!r}, not in the taxonomy")
        return value

    @field_validator("text")
    @classmethod
    def no_raw_email(cls, value: str) -> str:
        if EMAIL_PATTERN.search(value):
            raise ValueError("text contains an unmasked email address")
        return value

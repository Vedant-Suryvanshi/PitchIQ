# backend/schemas/startup.py
"""
Pydantic schemas for startup input validation.
These are used by FastAPI to parse + validate incoming request bodies.
If validation fails, FastAPI automatically returns a 422 with clear errors.
"""

from pydantic import BaseModel, Field, field_validator
import re


class StartupInput(BaseModel):
    """
    What the founder submits via the Generate form.
    Strict validation prevents garbage from reaching the agents.
    """

    description: str = Field(
        ...,
        min_length=50,
        max_length=5000,
        description="Startup idea in plain English. Min 50 chars.",
        examples=[
            "We are building an AI-powered legal contract review tool "
            "for small businesses in India who can't afford lawyers."
        ],
    )

    @field_validator("description")
    @classmethod
    def strip_and_normalize(cls, v: str) -> str:
        """
        Clean whitespace and normalize newlines.
        This runs before the min/max length check.
        """
        # Collapse multiple blank lines into one
        v = re.sub(r"\n{3,}", "\n\n", v.strip())
        return v

    @field_validator("description")
    @classmethod
    def no_html_tags(cls, v: str) -> str:
        """
        Reject input containing HTML tags.
        Protects against XSS injection attempts before security.py
        runs its deeper prompt injection check.
        """
        if re.search(r"<[^>]+>", v):
            raise ValueError("HTML tags are not allowed in startup descriptions.")
        return v


class StartupProfile(BaseModel):
    """
    Structured output from the Intake Agent.
    This is the data passed to all downstream agents.
    """
    startup_name:   str | None = None
    industry:       str | None = None
    business_model: str | None = None
    target_users:   str | None = None
    geography:      str | None = None
    problem:        str | None = None
    solution:       str | None = None
    raw_description: str       = ""   # Original founder description, preserved
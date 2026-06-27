# backend/schemas/memo.py
"""
Pydantic schemas for memo outputs and job status responses.
These shape what the frontend receives — never raw DB models.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class AgentStatus(str, Enum):
    QUEUED    = "queued"
    RUNNING   = "running"
    COMPLETED = "completed"
    FAILED    = "failed"
    SKIPPED   = "skipped"


class JobStatusResponse(BaseModel):
    """
    Returned by GET /api/status/{job_id}
    The frontend polls this every 2 seconds to update the progress UI.
    """
    job_id:        str
    status:        str
    agent_progress: dict[str, str]
    error_message: str | None = None
    created_at:    datetime
    updated_at:    datetime

    # Only populated when status == "completed"
    memo_available: bool = False


class MemoResponse(BaseModel):
    """
    Returned by GET /api/memo/{job_id}
    Contains the full investor memo and quality metadata.
    """
    job_id:           str
    startup_name:     str | None
    industry:         str | None
    memo_markdown:    str
    confidence_score: float | None = Field(
        None, ge=0.0, le=1.0,
        description="Quality Review Agent confidence (0–1)"
    )
    quality_flags:    list[str] = Field(
        default_factory=list,
        description="List of quality issues found by reviewer"
    )
    created_at:       datetime


class GenerateResponse(BaseModel):
    """
    Returned immediately when POST /api/generate is called.
    Returns a job_id the frontend uses to poll status.
    """
    job_id:  str
    message: str = "Memo generation started. Poll /api/status/{job_id} for progress."
    status:  str = "queued"
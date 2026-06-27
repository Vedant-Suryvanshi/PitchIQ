# backend/models.py
"""
PitchIQ Database Models
Updated for PostgreSQL with proper indexes and constraints
"""

from datetime import datetime, timezone
from enum import Enum as PyEnum
import uuid

from sqlalchemy import (
    String,
    Text,
    DateTime,
    Float,
    Enum,
    ForeignKey,
    JSON,
    Index,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class JobStatus(str, PyEnum):
    """Lifecycle states for a memo generation job."""
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class MemoJob(Base):
    """
    Tracks the state of one memo generation request.
    Added indexes for better performance.
    """
    __tablename__ = "memo_jobs"
    
    # Add indexes for frequently queried columns
    __table_args__ = (
        Index("ix_memo_jobs_status", "status"),
        Index("ix_memo_jobs_created_at", "created_at"),
        Index("ix_memo_jobs_updated_at", "updated_at"),
        Index("ix_memo_jobs_status_created", "status", "created_at"),
        CheckConstraint("length(id) = 36", name="check_id_length"),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    startup_description: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[JobStatus] = mapped_column(
        Enum(JobStatus),
        default=JobStatus.QUEUED,
        nullable=False,
    )

    agent_progress: Mapped[dict] = mapped_column(
        JSON,
        default=lambda: {
            "intake": "queued",
            "market_research": "queued",
            "funding": "queued",
            "vc_memo": "queued",
            "quality_review": "queued",
        },
    )

    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationship
    result: Mapped["MemoResult | None"] = relationship(
        "MemoResult",
        back_populates="job",
        uselist=False,
        lazy="selectin",
        cascade="all, delete-orphan",
    )


class MemoResult(Base):
    """
    Stores the final investor memo after all agents complete.
    """
    __tablename__ = "memo_results"
    
    __table_args__ = (
        Index("ix_memo_results_job_id", "job_id"),
        Index("ix_memo_results_created_at", "created_at"),
        Index("ix_memo_results_confidence_score", "confidence_score"),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    job_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("memo_jobs.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    # Startup profile
    startup_name: Mapped[str | None] = mapped_column(String(255))
    industry: Mapped[str | None] = mapped_column(String(255))
    business_model: Mapped[str | None] = mapped_column(String(255))
    target_users: Mapped[str | None] = mapped_column(String(255))
    geography: Mapped[str | None] = mapped_column(String(255))

    # Agent outputs
    market_research_output: Mapped[str | None] = mapped_column(Text)
    funding_analysis_output: Mapped[str | None] = mapped_column(Text)

    # Final memo (encrypted in application layer)
    memo_markdown: Mapped[str | None] = mapped_column(Text)

    # Quality metadata
    confidence_score: Mapped[float | None] = mapped_column(Float)
    quality_flags: Mapped[dict | None] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    # Back-reference
    job: Mapped["MemoJob"] = relationship("MemoJob", back_populates="result")


# Add User model for future authentication
class User(Base):
    """User model for authentication."""
    __tablename__ = "users"
    
    __table_args__ = (
        Index("ix_users_email", "email"),
        Index("ix_users_username", "username"),
        Index("ix_users_created_at", "created_at"),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    
    # API keys (stored as JSON)
    api_keys: Mapped[dict] = mapped_column(JSON, default=list)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    
    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
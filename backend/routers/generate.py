# backend/routers/generate.py
"""
POST /api/generate
──────────────────
Accepts a startup description, validates it through the security layer,
creates a MemoJob in the database, and kicks off the ADK orchestrator
as a background task. Returns a job_id immediately.
"""

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import structlog

from database import get_db
from models import MemoJob, JobStatus
from schemas.startup import StartupInput
from schemas.memo import GenerateResponse
from security.security import SecurityLayer
from config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()
security = SecurityLayer()

router = APIRouter(prefix="/api", tags=["generation"])


@router.post(
    "/generate",
    response_model=GenerateResponse,
    summary="Start investor memo generation",
    description=(
        "Submit a startup description. Returns a job_id immediately. "
        "Poll GET /api/status/{job_id} to track progress."
    ),
)
async def generate_memo(
    payload: StartupInput,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> GenerateResponse:
    """
    1. Run security checks on the raw description
    2. Create a MemoJob record in SQLite
    3. Launch the orchestrator in the background (non-blocking)
    4. Return job_id immediately
    """

    # ── Step 1: Security validation ───────────────────────────────────────────
    security_result = security.validate_input(payload.description)
    if not security_result.is_safe:
        logger.warning(
            "generate.blocked",
            reason=security_result.reason,
            # NOTE: we deliberately do NOT log the raw input here
            # to avoid logging potentially malicious content
        )
        raise HTTPException(
            status_code=400,
            detail=f"Input validation failed: {security_result.reason}",
        )

    # ── Step 2: Create job in database ────────────────────────────────────────
    job = MemoJob(
        startup_description=payload.description,
        status=JobStatus.QUEUED,
    )
    db.add(job)
    await db.flush()   # Get the auto-generated job.id without full commit
    job_id = job.id    # Capture before background task runs
    await db.commit()

    logger.info("generate.job_created", job_id=job_id)

    # ── Step 3: Fire orchestrator in background ───────────────────────────────
    # Import here to avoid circular imports at module load time
    from agents.orchestrator import run_orchestrator

    background_tasks.add_task(
        run_orchestrator,
        job_id=job_id,
        description=payload.description,
    )

    # ── Step 4: Return immediately ────────────────────────────────────────────
    return GenerateResponse(
        job_id=job_id,
        status="queued",
    )
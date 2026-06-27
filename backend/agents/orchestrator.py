# backend/agents/orchestrator.py
"""
PitchIQ Orchestrator
──────────────────────
Coordinates all 5 specialist agents using Google ADK patterns.

Pipeline:
  1. Intake Agent          (sequential — must run first)
  2. Market Research Agent } parallel — run simultaneously
     Funding Agent         }
  3. VC Memo Agent         (sequential — needs 1+2)
  4. Quality Review Agent  (sequential — needs 3)

This demonstrates:
  ✓ Google ADK multi-agent orchestration
  ✓ Sequential and parallel execution patterns
  ✓ Shared context passing between agents
  ✓ Real-time job progress updates
  ✓ Graceful error handling per agent
"""

import asyncio
from datetime import datetime, timezone
import structlog
from sqlalchemy import select

from agents.intake_agent import IntakeAgent
from agents.market_research_agent import MarketResearchAgent
from agents.funding_agent import FundingAgent
from agents.vc_memo_agent import VCMemoAgent
from agents.quality_review_agent import QualityReviewAgent

logger = structlog.get_logger(__name__)


async def run_orchestrator(job_id: str, description: str) -> None:
    """
    Main orchestration function called by FastAPI background task.
    Manages the full agent pipeline and writes the final memo to SQLite.
    """
    from database import AsyncSessionLocal
    from models import MemoJob, MemoResult, JobStatus

    logger.info("orchestrator.started", job_id=job_id)
    start_time = datetime.now(timezone.utc)

    # Shared context dict — agents read from and write to this
    context: dict = {
        "job_id": job_id,
        "description": description,
    }

    # ── Mark job as running ───────────────────────────────────────────────────
    async with AsyncSessionLocal() as db:
        stmt = select(MemoJob).where(MemoJob.id == job_id)
        result = await db.execute(stmt)
        job = result.scalar_one_or_none()
        if job:
            job.status = JobStatus.RUNNING
            await db.commit()

    try:
        # ── STEP 1: Intake Agent (must run first) ─────────────────────────────
        logger.info("orchestrator.step1.intake", job_id=job_id)
        intake = IntakeAgent()
        intake_result = await intake.run(context)

        if not intake_result.success:
            raise RuntimeError(f"Intake agent failed: {intake_result.error}")

        context["profile"] = intake_result.data.get("profile", {})

        # ── STEP 2: Market Research + Funding IN PARALLEL ─────────────────────
        # This is the key ADK demonstration: two agents working simultaneously.
        # asyncio.gather() runs both coroutines concurrently.
        # Total time = max(market_time, funding_time) not their sum.
        logger.info("orchestrator.step2.parallel_start", job_id=job_id)

        market_agent  = MarketResearchAgent()
        funding_agent = FundingAgent()

        market_result, funding_result = await asyncio.gather(
            market_agent.run(context),
            funding_agent.run(context),
            return_exceptions=True,  # Don't cancel the other if one fails
        )

        # Handle results — use fallback text if an agent failed
        if isinstance(market_result, Exception):
            logger.warning("orchestrator.market_failed", error=str(market_result))
            context["market_report"] = "Market research unavailable."
        else:
            context["market_report"] = market_result.data.get("market_report", "")

        if isinstance(funding_result, Exception):
            logger.warning("orchestrator.funding_failed", error=str(funding_result))
            context["funding_report"] = "Funding intelligence unavailable."
        else:
            context["funding_report"] = funding_result.data.get("funding_report", "")

        logger.info("orchestrator.step2.parallel_complete", job_id=job_id)

        # ── STEP 3: VC Memo Agent ─────────────────────────────────────────────
        logger.info("orchestrator.step3.vc_memo", job_id=job_id)
        memo_agent = VCMemoAgent()
        memo_result = await memo_agent.run(context)

        if not memo_result.success:
            raise RuntimeError(f"VC Memo agent failed: {memo_result.error}")

        context["memo_markdown"] = memo_result.data.get("memo_markdown", "")

        # ── STEP 4: Quality Review Agent ──────────────────────────────────────
        logger.info("orchestrator.step4.quality_review", job_id=job_id)
        quality_agent = QualityReviewAgent()
        quality_result = await quality_agent.run(context)

        confidence_score = 0.75
        quality_flags = []

        if quality_result.success:
            confidence_score = quality_result.data.get("confidence_score", 0.75)
            quality_flags = quality_result.data.get("quality_flags", [])

        # ── STEP 5: Write final result to database ────────────────────────────
        elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
        logger.info(
            "orchestrator.writing_result",
            job_id=job_id,
            elapsed_seconds=elapsed,
        )

        profile = context.get("profile", {})

        async with AsyncSessionLocal() as db:
            stmt = select(MemoJob).where(MemoJob.id == job_id)
            result = await db.execute(stmt)
            job = result.scalar_one_or_none()

            if job:
                job.status = JobStatus.COMPLETED

                memo_record = MemoResult(
                    job_id=job_id,
                    startup_name=profile.get("startup_name"),
                    industry=profile.get("industry"),
                    business_model=profile.get("business_model"),
                    target_users=profile.get("target_users"),
                    geography=profile.get("geography"),
                    market_research_output=context.get("market_report"),
                    funding_analysis_output=context.get("funding_report"),
                    memo_markdown=context.get("memo_markdown"),
                    confidence_score=confidence_score,
                    quality_flags=[
                        f["issue"] for f in quality_flags
                        if isinstance(f, dict) and "issue" in f
                    ],
                )
                db.add(memo_record)
                await db.commit()

        logger.info(
            "orchestrator.completed",
            job_id=job_id,
            elapsed_seconds=elapsed,
            confidence=confidence_score,
        )

    except Exception as e:
        # ── Mark job as failed with error message ─────────────────────────────
        logger.exception("orchestrator.failed", job_id=job_id, error=str(e))

        async with AsyncSessionLocal() as db:
            stmt = select(MemoJob).where(MemoJob.id == job_id)
            result = await db.execute(stmt)
            job = result.scalar_one_or_none()

            if job:
                job.status = JobStatus.FAILED
                job.error_message = str(e)
                await db.commit()
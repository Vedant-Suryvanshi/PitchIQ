# backend/agents/base_agent.py
"""
PitchIQ Base Agent
──────────────────
All specialist agents inherit from BaseAgent.
Provides:
  - Gemini 2.5 Flash client (configured once)
  - Retry logic with exponential backoff
  - Job progress updater (writes to SQLite so frontend can poll)
  - Structured logging
  - Token usage tracking
"""

import asyncio
from abc import ABC, abstractmethod
from typing import Any
import structlog
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
import google.generativeai as genai
from sqlalchemy import select

from config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()

# Configure Gemini once at module load — all agents share this
genai.configure(api_key=settings.google_api_key.get_secret_value())


class AgentResult:
    """Typed return value from every agent's run() method."""
    def __init__(
        self,
        success: bool,
        output: str = "",
        data: dict[str, Any] | None = None,
        error: str = "",
        tokens_used: int = 0,
    ):
        self.success = success
        self.output = output          # Markdown text output
        self.data = data or {}        # Structured dict output
        self.error = error
        self.tokens_used = tokens_used


class BaseAgent(ABC):
    """
    Abstract base class for all PitchIQ agents.
    Subclasses must implement:
      - agent_name (str property)
      - system_prompt (str property)
      - run(context: dict) -> AgentResult
    """

    def __init__(self):
        # Each agent gets its own Gemini model instance
        self.model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            generation_config=genai.GenerationConfig(
                temperature=0.3,       # Low temp = consistent, factual outputs
                max_output_tokens=8192,
            ),
            system_instruction=self.system_prompt,
        )
        self.logger = structlog.get_logger(self.agent_name)

    @property
    @abstractmethod
    def agent_name(self) -> str:
        """Unique snake_case name. Must match keys in agent_progress dict."""
        ...

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """The system prompt that defines this agent's role and behavior."""
        ...

    @abstractmethod
    async def run(self, context: dict[str, Any]) -> AgentResult:
        """
        Execute this agent's task.
        context: dict containing all outputs from previous agents.
        Returns AgentResult with output text and structured data.
        """
        ...

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    async def _call_gemini(self, prompt: str) -> tuple[str, int]:
        """
        Calls Gemini with retry logic.
        Returns (response_text, tokens_used).
        Retries up to 3 times with exponential backoff on any error.
        """
        self.logger.info(f"{self.agent_name}.calling_gemini")

        # Run in executor because google-generativeai is sync
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.model.generate_content(prompt)
        )

        text = response.text
        tokens = response.usage_metadata.total_token_count if response.usage_metadata else 0

        self.logger.info(
            f"{self.agent_name}.gemini_response",
            tokens=tokens,
            chars=len(text),
        )
        return text, tokens

    async def update_job_progress(
        self,
        job_id: str,
        status: str,
    ) -> None:
        """
        Updates the agent's status in the MemoJob.agent_progress dict.
        This is what the frontend polls to show real-time progress.
        status: one of "running", "completed", "failed"
        """
        from database import AsyncSessionLocal
        from models import MemoJob

        async with AsyncSessionLocal() as db:
            stmt = select(MemoJob).where(MemoJob.id == job_id)
            result = await db.execute(stmt)
            job = result.scalar_one_or_none()

            if job:
                # SQLAlchemy requires reassignment to detect JSON mutation
                progress = dict(job.agent_progress or {})
                progress[self.agent_name] = status
                job.agent_progress = progress
                await db.commit()

        self.logger.info(
            f"{self.agent_name}.progress_updated",
            job_id=job_id,
            status=status,
        )
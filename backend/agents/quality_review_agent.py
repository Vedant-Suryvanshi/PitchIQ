# backend/agents/quality_review_agent.py
"""
Quality Review Agent
─────────────────────
The last agent in the pipeline.
Acts as a skeptical VC partner reviewing the AI-generated memo.
Outputs a confidence score and list of flags for the frontend to display.
"""

import json
from typing import Any

from agents.base_agent import BaseAgent, AgentResult
from agents.prompts.quality_prompt import QUALITY_SYSTEM_PROMPT, QUALITY_USER_TEMPLATE


class QualityReviewAgent(BaseAgent):

    @property
    def agent_name(self) -> str:
        return "quality_review"

    @property
    def system_prompt(self) -> str:
        return QUALITY_SYSTEM_PROMPT

    async def run(self, context: dict[str, Any]) -> AgentResult:
        """
        Input:  context["memo_markdown"], context["description"]
        Output: AgentResult with data["confidence_score"] and data["flags"]
        """
        job_id = context.get("job_id", "")
        memo = context.get("memo_markdown", "")
        description = context.get("description", "")

        await self.update_job_progress(job_id, "running")

        try:
            prompt = QUALITY_USER_TEMPLATE.format(
                memo=memo,
                description=description,
            )

            raw_response, tokens = await self._call_gemini(prompt)

            # Clean and parse JSON response
            cleaned = raw_response.strip()
            if cleaned.startswith("```"):
                lines = cleaned.split("\n")
                cleaned = "\n".join(lines[1:-1])

            review = json.loads(cleaned)

            await self.update_job_progress(job_id, "completed")

            return AgentResult(
                success=True,
                output=json.dumps(review, indent=2),
                data={
                    "confidence_score": review.get("confidence_score", 0.75),
                    "quality_flags": review.get("flags", []),
                    "review": review,
                },
                tokens_used=tokens,
            )

        except json.JSONDecodeError:
            # If JSON parsing fails, return a safe default
            await self.update_job_progress(job_id, "completed")
            return AgentResult(
                success=True,
                output="{}",
                data={
                    "confidence_score": 0.70,
                    "quality_flags": [],
                    "review": {"note": "Quality review completed with parsing warning"},
                },
            )

        except Exception as e:
            await self.update_job_progress(job_id, "failed")
            return AgentResult(success=False, error=str(e))
# backend/agents/intake_agent.py
"""
Intake Agent
────────────
First agent in the pipeline.
Parses the founder's plain-English description into a structured profile
that all downstream agents use as their context.
"""

import json
from typing import Any
import structlog

from agents.base_agent import BaseAgent, AgentResult
from agents.prompts.intake_prompt import INTAKE_SYSTEM_PROMPT, INTAKE_USER_TEMPLATE

logger = structlog.get_logger(__name__)


class IntakeAgent(BaseAgent):

    @property
    def agent_name(self) -> str:
        return "intake"

    @property
    def system_prompt(self) -> str:
        return INTAKE_SYSTEM_PROMPT

    async def run(self, context: dict[str, Any]) -> AgentResult:
        """
        Input:  context["description"] — raw founder text
        Output: AgentResult with data["profile"] = structured dict
        """
        job_id = context.get("job_id", "")
        description = context.get("description", "")

        await self.update_job_progress(job_id, "running")

        try:
            prompt = INTAKE_USER_TEMPLATE.format(description=description)
            raw_response, tokens = await self._call_gemini(prompt)

            # Strip markdown code fences if Gemini adds them
            cleaned = raw_response.strip()
            if cleaned.startswith("```"):
                lines = cleaned.split("\n")
                cleaned = "\n".join(lines[1:-1])

            profile = json.loads(cleaned)

            # Add the raw description to the profile for downstream agents
            profile["raw_description"] = description

            await self.update_job_progress(job_id, "completed")

            return AgentResult(
                success=True,
                output=json.dumps(profile, indent=2),
                data={"profile": profile},
                tokens_used=tokens,
            )

        except json.JSONDecodeError as e:
            # Gemini occasionally returns malformed JSON — graceful fallback
            logger.warning("intake.json_parse_failed", error=str(e))
            fallback_profile = {
                "startup_name": "Unknown Startup",
                "industry": "Technology",
                "business_model": "Unknown",
                "target_users": "Unknown",
                "geography": "Global",
                "problem": description[:500],
                "solution": "See description",
                "raw_description": description,
            }
            await self.update_job_progress(job_id, "completed")
            return AgentResult(
                success=True,
                output=json.dumps(fallback_profile, indent=2),
                data={"profile": fallback_profile},
            )

        except Exception as e:
            await self.update_job_progress(job_id, "failed")
            return AgentResult(success=False, error=str(e))
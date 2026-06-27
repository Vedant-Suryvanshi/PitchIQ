# backend/agents/vc_memo_agent.py
"""
VC Memo Agent
──────────────
Synthesizes all previous agent outputs into a complete investor memo.
This is the primary deliverable — the document a founder sends to VCs.
"""

import json
from datetime import date
from typing import Any

from agents.base_agent import BaseAgent, AgentResult
from agents.prompts.vc_memo_prompt import VC_MEMO_SYSTEM_PROMPT, VC_MEMO_USER_TEMPLATE


class VCMemoAgent(BaseAgent):

    @property
    def agent_name(self) -> str:
        return "vc_memo"

    @property
    def system_prompt(self) -> str:
        return VC_MEMO_SYSTEM_PROMPT

    async def run(self, context: dict[str, Any]) -> AgentResult:
        """
        Input:  context["profile"], ["market_report"], ["funding_report"]
        Output: AgentResult with output = complete investor memo markdown
        """
        job_id = context.get("job_id", "")
        profile = context.get("profile", {})
        market_research = context.get("market_report", "")
        funding_intelligence = context.get("funding_report", "")

        await self.update_job_progress(job_id, "running")

        try:
            profile_text = json.dumps(profile, indent=2)
            today = date.today().strftime("%B %Y")

            prompt = VC_MEMO_USER_TEMPLATE.format(
                profile=profile_text,
                market_research=market_research,
                funding_intelligence=funding_intelligence,
                date=today,
            )

            memo, tokens = await self._call_gemini(prompt)

            await self.update_job_progress(job_id, "completed")

            return AgentResult(
                success=True,
                output=memo,
                data={"memo_markdown": memo},
                tokens_used=tokens,
            )

        except Exception as e:
            await self.update_job_progress(job_id, "failed")
            return AgentResult(success=False, error=str(e))
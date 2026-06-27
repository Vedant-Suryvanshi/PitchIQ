# backend/agents/funding_agent.py
"""
Funding Intelligence Agent — MCP-enhanced version.
Calls MCP funding_lookup tool for live comparable rounds,
then synthesizes with Gemini.
"""

import json
import asyncio
from agents.base_agent import BaseAgent, AgentResult
from mcp_server.server import mcp_server


class FundingAgent(BaseAgent):
    @property
    def agent_name(self) -> str:
        return "funding"

    @property
    def system_prompt(self) -> str:
        return (
            "You are the Funding Intelligence Agent for PitchIQ. "
            "Analyze comparable funding rounds, valuations, and investor landscapes. "
            "Format output in clean markdown with specific numbers."
        )

    async def run(self, context: dict) -> AgentResult:
        job_id = context.get("job_id", "")
        profile = context.get("profile", {})
        market_report = context.get("market_report", "")[:1500]
        industry = profile.get("industry", "technology")
        geography = profile.get("geography", "global")

        await self.update_job_progress(job_id, "running")

        try:
            # ── Step 1: Call MCP funding_lookup tool ──────────────────────────
            funding_result = await mcp_server.call_tool(
                "funding_lookup",
                industry=industry,
                stage="seed",
                geography=geography,
            )
            funding_data = funding_result.get("funding_data", "")

            # ── Step 2: Synthesize with Gemini ────────────────────────────────
            prompt = f"""Using the funding data below, write a Funding Intelligence Report in markdown.

STARTUP PROFILE:
{json.dumps(profile, indent=2)}

MARKET CONTEXT:
{market_report}

LIVE FUNDING DATA (from MCP lookup):
{funding_data[:2000]}

Write the report covering:
## Comparable Companies & Funding Rounds
- 4-6 comparable startups: name, stage, amount, year, investors

## Valuation Benchmarks
- Pre-seed and seed ranges for this sector
- Revenue multiples

## Investor Landscape
- 5-8 active VCs in this sector
- Relevant accelerators

## Funding Strategy Recommendations
- Suggested raise for current stage
- Key milestones before fundraising

## Investment Thesis Signals
- What makes this attractive
- Concerns investors will raise"""

            report, tokens = await self._call_gemini(prompt)
            await self.update_job_progress(job_id, "completed")

            return AgentResult(
                success=True,
                output=report,
                data={"funding_report": report},
                tokens_used=tokens,
            )

        except Exception as e:
            await self.update_job_progress(job_id, "failed")
            return AgentResult(success=False, error=str(e))

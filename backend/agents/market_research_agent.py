import json
import asyncio
from typing import Any
from agents.base_agent import BaseAgent, AgentResult
from mcp_server.server import mcp_server


class MarketResearchAgent(BaseAgent):

    @property
    def agent_name(self) -> str:
        return "market_research"

    @property
    def system_prompt(self) -> str:
        return (
            "You are the Market Research Agent for PitchIQ. "
            "Produce VC-grade market intelligence reports with specific numbers, "
            "growth rates, TAM/SAM/SOM analysis, and competitor analysis. "
            "Format output in clean markdown."
        )

    async def run(self, context: dict[str, Any]) -> AgentResult:
        job_id = context.get("job_id", "")
        profile = context.get("profile", {})
        industry = profile.get("industry", "technology")
        geography = profile.get("geography", "global")

        await self.update_job_progress(job_id, "running")

        try:
            # Step 1: Call MCP tools in parallel for live data
            web_result, research_result = await asyncio.gather(
                mcp_server.call_tool(
                    "web_search",
                    query=industry + " market size growth rate 2024 2025",
                ),
                mcp_server.call_tool(
                    "startup_research",
                    industry=industry,
                    geography=geography,
                ),
            )

            web_data = web_result.get("summary", "No web data available.")
            research_data = research_result.get("findings", "No research data available.")

            # Step 2: Build prompt using string concatenation to avoid f-string nesting
            profile_json = json.dumps(profile, indent=2)
            web_data_trimmed = web_data[:2000]
            research_data_trimmed = research_data[:2000]

            prompt = (
                "Using the research data below, write a comprehensive Market Intelligence "
                "Report in markdown.\n\n"
                "STARTUP PROFILE:\n"
                + profile_json
                + "\n\nLIVE MARKET DATA (from web search):\n"
                + web_data_trimmed
                + "\n\nINDUSTRY RESEARCH:\n"
                + research_data_trimmed
                + "\n\nWrite the report covering all of these sections:\n\n"
                "## Market Overview\n"
                "- Industry scope, current market size, CAGR\n\n"
                "## TAM / SAM / SOM Analysis\n"
                "- TAM: global market size with methodology\n"
                "- SAM: realistic reachable segment\n"
                "- SOM: realistic 3-5 year capture target\n\n"
                "## Competitive Landscape\n"
                "- 4-6 direct competitors with descriptions\n"
                "- 2-3 indirect competitors\n"
                "- Market gaps this startup could exploit\n\n"
                "## Market Trends\n"
                "- 3-5 major trends accelerating this market\n\n"
                "## Market Entry Assessment\n"
                "- Barriers to entry, customer acquisition channels\n\n"
                "Use the live data provided. Be specific with numbers."
            )

            # Step 3: Synthesize with Gemini
            report, tokens = await self._call_gemini(prompt)
            await self.update_job_progress(job_id, "completed")

            return AgentResult(
                success=True,
                output=report,
                data={"market_report": report},
                tokens_used=tokens,
            )

        except Exception as e:
            await self.update_job_progress(job_id, "failed")
            return AgentResult(
                 success=False, 
                 error=str(e)
            )
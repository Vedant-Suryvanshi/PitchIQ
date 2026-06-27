# backend/mcp_server/tools/funding_lookup.py
"""
Funding Lookup Tool
────────────────────
MCP tool that finds comparable funding rounds and investor
data for a given industry and stage.
"""

import google.generativeai as genai
from config import get_settings

settings = get_settings()
genai.configure(api_key=settings.google_api_key.get_secret_value())


async def funding_lookup(
    industry: str,
    stage: str = "seed",
    geography: str = "global",
) -> dict:
    """
    MCP Tool: funding_lookup
    Finds comparable funding rounds and investor intelligence.

    Args:
        industry: Industry vertical (e.g. "legal tech", "fintech")
        stage: Funding stage (pre-seed, seed, series-a, etc.)
        geography: Target geography

    Returns:
        dict with funding intelligence data
    """
    try:
        model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            tools=[{"google_search": {}}],
        )

        query = (
            f"Find recent {stage} funding rounds in the {industry} industry "
            f"in {geography}. Include: company names, amounts raised, investors, "
            f"valuations, dates. Focus on 2022-2025 data."
        )

        response = model.generate_content(query)
        result_text = response.text if response.text else "Funding data unavailable."

        return {
            "tool": "funding_lookup",
            "industry": industry,
            "stage": stage,
            "geography": geography,
            "funding_data": result_text,
            "status": "success",
        }

    except Exception as e:
        return {
            "tool": "funding_lookup",
            "industry": industry,
            "stage": stage,
            "funding_data": f"Lookup unavailable: {str(e)}",
            "status": "error",
        }

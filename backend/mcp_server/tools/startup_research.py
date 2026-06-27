# backend/mcp_server/tools/startup_research.py
"""
Startup Research Tool
──────────────────────
MCP tool that performs targeted research on a specific
startup or industry using Gemini grounded search.
"""

import google.generativeai as genai
from config import get_settings

settings = get_settings()
genai.configure(api_key=settings.google_api_key.get_secret_value())


async def startup_research(
    company_name: str = "",
    industry: str = "",
    geography: str = "",
) -> dict:
    """
    MCP Tool: startup_research
    Researches a startup or industry vertical for competitive intelligence.

    Args:
        company_name: Name of company to research (optional)
        industry: Industry vertical to research
        geography: Target geography

    Returns:
        dict with competitive intelligence data
    """
    try:
        model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            tools=[{"google_search": {}}],
        )

        if company_name:
            query = (
                f"Research the company {company_name} in the {industry} industry. "
                f"Find: funding history, product description, target market, key investors, "
                f"recent news, valuation if available."
            )
        else:
            query = (
                f"Research the {industry} startup ecosystem in {geography or 'globally'}. "
                f"Find: key players, market size, recent funding rounds, growth trends, "
                f"regulatory environment."
            )

        response = model.generate_content(query)
        result_text = response.text if response.text else "Research unavailable."

        return {
            "tool": "startup_research",
            "company_name": company_name,
            "industry": industry,
            "geography": geography,
            "findings": result_text,
            "status": "success",
        }

    except Exception as e:
        return {
            "tool": "startup_research",
            "company_name": company_name,
            "industry": industry,
            "findings": f"Research unavailable: {str(e)}",
            "status": "error",
        }

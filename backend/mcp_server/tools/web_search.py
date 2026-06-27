# backend/mcp_server/tools/web_search.py
"""
Web Search Tool
───────────────
MCP tool that uses Gemini with Google Search grounding
to retrieve live web data for market research agents.
"""

import google.generativeai as genai
from config import get_settings

settings = get_settings()
genai.configure(api_key=settings.google_api_key.get_secret_value())


async def web_search(query: str, max_results: int = 5) -> dict:
    """
    MCP Tool: web_search
    Performs a grounded web search using Gemini.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
    
    Returns:
        dict with keys: query, results, summary
    """
    try:
        # Use Gemini with search grounding for live results
        model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            tools=[{"google_search": {}}],
        )

        response = model.generate_content(
            f"Search for current information about: {query}\n"
            f"Provide a factual summary with key data points, statistics, and recent developments."
        )

        result_text = response.text if response.text else "No results found."

        return {
            "tool": "web_search",
            "query": query,
            "summary": result_text,
            "status": "success",
        }

    except Exception as e:
        # Graceful fallback — never crash an agent over a search failure
        return {
            "tool": "web_search",
            "query": query,
            "summary": f"Search unavailable: {str(e)}",
            "status": "error",
        }

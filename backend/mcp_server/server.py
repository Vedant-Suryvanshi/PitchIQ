# backend/mcp_server/server.py
"""
PitchIQ MCP Server
───────────────────
Model Context Protocol server exposing 3 tools to agents:
  1. web_search        — live web search via Gemini grounding
  2. startup_research  — company/industry deep research
  3. funding_lookup    — comparable funding rounds finder

Agents call tools via: MCPClient.call_tool(tool_name, **kwargs)
This server handles routing, validation, and error handling.

Why MCP?
  MCP standardizes how agents call external tools. Instead of each
  agent having its own HTTP client or API integration, all tool
  calls go through one protocol layer. This makes tools swappable,
  testable, and auditable — a production architecture pattern.
"""

import asyncio
import structlog
from typing import Any
from mcp_server.tools.web_search import web_search
from mcp_server.tools.startup_research import startup_research
from mcp_server.tools.funding_lookup import funding_lookup

logger = structlog.get_logger(__name__)

# Registry of all available MCP tools
# Adding a new tool = add one entry here + implement the function
TOOL_REGISTRY: dict[str, Any] = {
    "web_search": web_search,
    "startup_research": startup_research,
    "funding_lookup": funding_lookup,
}

# Tool schemas for validation and documentation
TOOL_SCHEMAS = {
    "web_search": {
        "name": "web_search",
        "description": "Search the web for current information on any topic",
        "parameters": {
            "query": {"type": "string", "required": True},
            "max_results": {"type": "integer", "required": False, "default": 5},
        },
    },
    "startup_research": {
        "name": "startup_research",
        "description": "Research a startup or industry for competitive intelligence",
        "parameters": {
            "company_name": {"type": "string", "required": False},
            "industry": {"type": "string", "required": True},
            "geography": {"type": "string", "required": False},
        },
    },
    "funding_lookup": {
        "name": "funding_lookup",
        "description": "Find comparable funding rounds and investor data",
        "parameters": {
            "industry": {"type": "string", "required": True},
            "stage": {"type": "string", "required": False, "default": "seed"},
            "geography": {"type": "string", "required": False, "default": "global"},
        },
    },
}


class MCPServer:
    """
    The MCP server manages tool routing and execution.
    Agents never call tool functions directly — they go through this server.
    This provides a single audit point for all external tool calls.
    """

    async def call_tool(self, tool_name: str, **kwargs) -> dict:
        """
        Route a tool call to the correct implementation.
        Logs every call for observability (without logging sensitive data).
        """
        if tool_name not in TOOL_REGISTRY:
            logger.warning("mcp.unknown_tool", tool=tool_name)
            return {
                "status": "error",
                "error": f"Unknown tool: {tool_name}",
                "available_tools": list(TOOL_REGISTRY.keys()),
            }

        logger.info("mcp.tool_called", tool=tool_name)

        try:
            tool_fn = TOOL_REGISTRY[tool_name]
            result = await tool_fn(**kwargs)
            logger.info("mcp.tool_success", tool=tool_name)
            return result

        except Exception as e:
            logger.error("mcp.tool_error", tool=tool_name, error=str(e))
            return {
                "status": "error",
                "tool": tool_name,
                "error": str(e),
            }

    def list_tools(self) -> list[dict]:
        """Returns schemas for all registered tools."""
        return list(TOOL_SCHEMAS.values())


# Singleton instance — import this everywhere
mcp_server = MCPServer()

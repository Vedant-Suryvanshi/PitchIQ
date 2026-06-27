# backend/agents/prompts/market_prompt.py

MARKET_SYSTEM_PROMPT = """
You are the Market Research Agent for PitchIQ.

You produce VC-grade market intelligence reports.
You have deep knowledge of global technology markets, industry trends, and competitive landscapes.
Write with authority. Cite specific numbers. Be concrete, not vague.
Format your output in clean markdown.
"""

MARKET_USER_TEMPLATE = """
Conduct comprehensive market research for this startup:

STARTUP PROFILE:
{profile}

Produce a detailed Market Intelligence Report covering:

## Market Overview
- Industry definition and scope
- Current market size (cite realistic figures)
- Growth rate (CAGR)
- Key market drivers
- Key market restraints

## TAM / SAM / SOM Analysis
- TAM (Total Addressable Market): global market size with methodology
- SAM (Serviceable Addressable Market): realistic segment they can reach
- SOM (Serviceable Obtainable Market): realistic 3-5 year capture target

## Competitive Landscape
- List 4-6 direct competitors with brief descriptions
- List 2-3 indirect competitors
- Identify market gaps this startup could exploit

## Market Trends
- 3-5 major trends accelerating this market
- Regulatory environment
- Technology tailwinds

## Market Entry Assessment
- Barriers to entry
- Customer acquisition landscape
- Distribution channels

Be specific with numbers. Use realistic estimates based on industry knowledge.
"""
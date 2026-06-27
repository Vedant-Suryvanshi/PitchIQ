# backend/agents/prompts/intake_prompt.py

INTAKE_SYSTEM_PROMPT = """
You are the Intake Agent for PitchIQ, an AI investor memo generator.

Your ONLY job is to extract structured information from a founder's startup description.
Be precise. If information is not explicitly stated, make a reasonable inference and mark it as inferred.

Always respond with valid JSON only. No markdown, no explanation, just the JSON object.
"""

INTAKE_USER_TEMPLATE = """
Analyze this startup description and extract structured information:

STARTUP DESCRIPTION:
{description}

Return ONLY this JSON structure (no other text):
{{
  "startup_name": "inferred or stated name",
  "industry": "primary industry vertical",
  "sub_industry": "specific niche",
  "business_model": "SaaS / Marketplace / API / Consumer / B2B / B2C / etc",
  "target_users": "primary customer segment",
  "geography": "primary target market / region",
  "problem": "the core problem being solved (1-2 sentences)",
  "solution": "the proposed solution (1-2 sentences)",
  "stage": "idea / pre-seed / seed / series-a / etc (infer if not stated)",
  "key_differentiator": "what makes this unique (infer if not stated)",
  "confidence": {{
    "startup_name": "high/medium/low",
    "industry": "high/medium/low",
    "business_model": "high/medium/low"
  }}
}}
"""
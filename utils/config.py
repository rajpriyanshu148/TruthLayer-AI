import os
from dotenv import load_dotenv

load_dotenv()


def get_api_key(key: str) -> str:
    """Read API key at call-time: env → .streamlit/secrets → session_state."""
    value = os.getenv(key, "")
    if not value:
        try:
            import streamlit as st
            value = st.secrets.get(key, "")
        except Exception:
            pass
    if not value:
        try:
            import streamlit as st
            value = st.session_state.get(f"_runtime_{key}", "")
        except Exception:
            pass
    return value


# Module-level defaults (populated at import for non-Streamlit callers)
GEMINI_API_KEY = get_api_key("GEMINI_API_KEY")
TAVILY_API_KEY = get_api_key("TAVILY_API_KEY")


GEMINI_MODEL = "gemini-2.0-flash"

MAX_CLAIMS_PER_DOC = 50
MAX_TEXT_CHARS = 50000
TAVILY_MAX_RESULTS = 3
SEARCH_TIMEOUT = 10

CLAIM_EXTRACT_PROMPT = """
You are a fact-checking AI. Extract all factual claims from the text below.

A factual claim is a statement that:
- Contains a specific statistic, number, percentage, date, or figure
- Makes an assertion about a company, product, person, or organization
- States a historical event, scientific fact, or technical specification
- Includes financial figures, market data, or economic indicators

Do NOT extract:
- Opinions, predictions, or hypothetical statements
- Vague or unverifiable statements
- Duplicate or near-duplicate claims

Return ONLY a JSON array in this exact format:
[
  {{"claim": "exact factual claim text here"}}
]

Text to analyze:
{text}
"""

VERIFY_CLAIM_PROMPT = """
You are a professional fact-checker. Evaluate the following claim using the provided web evidence.

Claim: {claim}

Web Evidence:
{evidence}

Based on the evidence, classify this claim as:
- "Verified": The claim is accurate and confirmed by sources
- "Inaccurate": The claim is partially wrong or misleading
- "False": The claim is factually incorrect

Return ONLY a JSON object in this exact format:
{{
  "claim": "{claim}",
  "status": "Verified|Inaccurate|False",
  "confidence": <float 0.0-1.0>,
  "reason": "Brief explanation based on evidence",
  "correct_fact": "The accurate information (if status is Inaccurate or False, else empty string)",
  "source": "Primary source URL or name",
  "source_credibility": <float 0.0-1.0>
}}
"""

STATUS_COLORS = {
    "Verified": "#00d4aa",
    "Inaccurate": "#ffb347",
    "False": "#ff6b6b",
}

STATUS_ICONS = {
    "Verified": "✅",
    "Inaccurate": "⚠️",
    "False": "❌",
}

from google import genai
from google.genai import types as genai_types
from typing import Dict
from utils.config import get_api_key, GEMINI_MODEL, VERIFY_CLAIM_PROMPT, STATUS_COLORS
from utils.helpers import parse_json_response, safe_get
from utils.retry import retry_with_backoff


def _get_client():
    return genai.Client(api_key=get_api_key("GEMINI_API_KEY"))


def _build_source_credibility(sources: list) -> float:
    if not sources:
        return 0.3
    avg_score = sum(s.get("score", 0.5) for s in sources) / len(sources)
    return round(min(max(avg_score, 0.0), 1.0), 2)


@retry_with_backoff(max_retries=3, base_delay=2.0)
def verify_claim(claim: str, evidence: str, sources: list) -> Dict:
    client = _get_client()
    prompt = VERIFY_CLAIM_PROMPT.format(claim=claim, evidence=evidence)
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=genai_types.GenerateContentConfig(temperature=0.1),
        )
        result = parse_json_response(response.text)
        if not isinstance(result, dict):
            raise ValueError("Expected a JSON object")
        result["status"] = result.get("status", "Inaccurate")
        if result["status"] not in ("Verified", "Inaccurate", "False"):
            result["status"] = "Inaccurate"
        result["confidence"] = float(safe_get(result, "confidence", 0.5))
        result["source_credibility"] = _build_source_credibility(sources)
        result["correct_fact"] = safe_get(result, "correct_fact", "")
        result["source"] = safe_get(result, "source", "")
        result["reason"] = safe_get(result, "reason", "")
        return result
    except Exception as e:
        return {
            "claim": claim,
            "status": "Inaccurate",
            "confidence": 0.3,
            "reason": f"Verification error: {e}",
            "correct_fact": "",
            "source": "",
            "source_credibility": 0.3,
        }

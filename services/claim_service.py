from google import genai
from google.genai import types as genai_types
from typing import List, Dict
from utils.config import get_api_key, GEMINI_MODEL, MAX_CLAIMS_PER_DOC, CLAIM_EXTRACT_PROMPT
from utils.helpers import parse_json_response, deduplicate_claims
from utils.retry import retry_with_backoff


def _get_client():
    return genai.Client(api_key=get_api_key("GEMINI_API_KEY"))


@retry_with_backoff(max_retries=3, base_delay=2.0)
def extract_claims(text: str) -> List[Dict]:
    client = _get_client()
    prompt = CLAIM_EXTRACT_PROMPT.format(text=text)
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=genai_types.GenerateContentConfig(temperature=0.1),
        )
        raw = response.text
        claims = parse_json_response(raw)
        if not isinstance(claims, list):
            raise ValueError("Expected a JSON array of claims")
        valid = [c for c in claims if isinstance(c, dict) and "claim" in c and c["claim"].strip()]
        unique = deduplicate_claims(valid)
        return unique[:MAX_CLAIMS_PER_DOC]
    except Exception as e:
        raise RuntimeError(f"Claim extraction failed: {e}") from e

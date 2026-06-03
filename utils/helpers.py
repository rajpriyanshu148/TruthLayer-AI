import re
import json
from difflib import SequenceMatcher
from typing import List, Dict, Any


def similarity_ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def deduplicate_claims(claims: List[Dict]) -> List[Dict]:
    unique = []
    for candidate in claims:
        text = candidate.get("claim", "")
        is_duplicate = any(
            similarity_ratio(text, existing.get("claim", "")) > 0.82
            for existing in unique
        )
        if not is_duplicate and text.strip():
            unique.append(candidate)
    return unique


def parse_json_response(raw: str) -> Any:
    raw = raw.strip()
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw)
    match = re.search(r"[\[\{].*[\]\}]", raw, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError(f"No valid JSON found in response: {raw[:200]}")


def compute_accuracy_score(results: List[Dict]) -> float:
    if not results:
        return 0.0
    verified = sum(1 for r in results if r.get("status") == "Verified")
    return round((verified / len(results)) * 100, 1)


def compute_avg_confidence(results: List[Dict]) -> float:
    scores = [r.get("confidence", 0.0) for r in results if "confidence" in r]
    return round(sum(scores) / len(scores) * 100, 1) if scores else 0.0


def format_percentage(value: float) -> str:
    return f"{value:.1f}%"


def truncate_text(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n...[text truncated for processing]"


def safe_get(d: Dict, key: str, default: Any = "") -> Any:
    return d.get(key, default) or default

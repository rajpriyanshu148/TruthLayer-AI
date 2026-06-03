from tavily import TavilyClient
from typing import List, Dict, Optional
from utils.config import get_api_key, TAVILY_MAX_RESULTS, SEARCH_TIMEOUT


def _get_client() -> TavilyClient:
    return TavilyClient(api_key=get_api_key("TAVILY_API_KEY"))


def search_claim(claim: str) -> Dict:
    try:
        client = _get_client()
        response = client.search(
            query=claim,
            search_depth="advanced",
            max_results=TAVILY_MAX_RESULTS,
            include_answer=True,
            include_raw_content=False,
        )
        results = response.get("results", [])
        answer = response.get("answer", "")
        sources = [
            {
                "url": r.get("url", ""),
                "title": r.get("title", ""),
                "content": r.get("content", "")[:400],
                "score": r.get("score", 0.0),
            }
            for r in results
            if r.get("url")
        ]
        return {"answer": answer, "sources": sources}
    except Exception as e:
        return {"answer": "", "sources": [], "error": str(e)}


def format_evidence(search_result: Dict) -> str:
    parts = []
    if search_result.get("answer"):
        parts.append(f"Web Summary: {search_result['answer']}")
    for i, src in enumerate(search_result.get("sources", []), 1):
        snippet = src.get("content", "").strip()
        url = src.get("url", "")
        title = src.get("title", "")
        if snippet:
            parts.append(f"Source {i} [{title}] ({url}):\n{snippet}")
    return "\n\n".join(parts) if parts else "No relevant web sources found."

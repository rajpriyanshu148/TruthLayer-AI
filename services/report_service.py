import io
import pandas as pd
from datetime import datetime
from typing import List, Dict
from utils.helpers import compute_accuracy_score, compute_avg_confidence


def generate_csv_report(results: List[Dict], filename: str = "truthlayer_report") -> bytes:
    rows = []
    for i, r in enumerate(results, 1):
        rows.append({
            "#": i,
            "Claim": r.get("claim", ""),
            "Status": r.get("status", ""),
            "Confidence (%)": round(r.get("confidence", 0) * 100, 1),
            "Reason": r.get("reason", ""),
            "Correct Fact": r.get("correct_fact", ""),
            "Source": r.get("source", ""),
            "Source Credibility (%)": round(r.get("source_credibility", 0) * 100, 1),
        })
    df = pd.DataFrame(rows)
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False, encoding="utf-8-sig")
    return buffer.getvalue()


def generate_summary_stats(results: List[Dict]) -> Dict:
    total = len(results)
    verified = sum(1 for r in results if r.get("status") == "Verified")
    inaccurate = sum(1 for r in results if r.get("status") == "Inaccurate")
    false_count = sum(1 for r in results if r.get("status") == "False")
    return {
        "total": total,
        "verified": verified,
        "inaccurate": inaccurate,
        "false": false_count,
        "accuracy_score": compute_accuracy_score(results),
        "avg_confidence": compute_avg_confidence(results),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

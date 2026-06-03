"""
Unit tests for TruthLayer AI utility modules.
Run: python -m pytest tests/ -v
"""
import pytest
import json
from unittest.mock import MagicMock, patch


# ── helpers ──────────────────────────────────────────────────────────────────

from utils.helpers import (
    similarity_ratio,
    deduplicate_claims,
    parse_json_response,
    compute_accuracy_score,
    compute_avg_confidence,
    truncate_text,
    safe_get,
)


class TestSimilarityRatio:
    def test_identical_strings(self):
        assert similarity_ratio("hello world", "hello world") == 1.0

    def test_completely_different(self):
        assert similarity_ratio("apple", "zebra") < 0.5

    def test_case_insensitive(self):
        assert similarity_ratio("Apple", "apple") == 1.0

    def test_partial_match(self):
        ratio = similarity_ratio("the quick brown fox", "the quick brown cat")
        assert 0.7 < ratio < 1.0


class TestDeduplicateClaims:
    def test_removes_exact_duplicates(self):
        claims = [
            {"claim": "Apple was founded in 1976"},
            {"claim": "Apple was founded in 1976"},
        ]
        result = deduplicate_claims(claims)
        assert len(result) == 1

    def test_removes_near_duplicates(self):
        claims = [
            {"claim": "Apple Inc was founded in 1976 by Steve Jobs"},
            {"claim": "Apple Inc. was founded in 1976 by Steve Jobs"},
        ]
        result = deduplicate_claims(claims)
        assert len(result) == 1

    def test_keeps_distinct_claims(self):
        claims = [
            {"claim": "Apple was founded in 1976"},
            {"claim": "Google was founded in 1998"},
            {"claim": "Microsoft was founded in 1975"},
        ]
        result = deduplicate_claims(claims)
        assert len(result) == 3

    def test_filters_empty_claims(self):
        claims = [{"claim": ""}, {"claim": "  "}, {"claim": "Valid claim here"}]
        result = deduplicate_claims(claims)
        assert len(result) == 1
        assert result[0]["claim"] == "Valid claim here"

    def test_empty_input(self):
        assert deduplicate_claims([]) == []


class TestParseJsonResponse:
    def test_plain_json_array(self):
        raw = '[{"claim": "test claim"}]'
        result = parse_json_response(raw)
        assert isinstance(result, list)
        assert result[0]["claim"] == "test claim"

    def test_json_wrapped_in_markdown(self):
        raw = '```json\n[{"claim": "markdown wrapped"}]\n```'
        result = parse_json_response(raw)
        assert result[0]["claim"] == "markdown wrapped"

    def test_json_object(self):
        raw = '{"status": "Verified", "confidence": 0.9}'
        result = parse_json_response(raw)
        assert result["status"] == "Verified"

    def test_json_with_surrounding_text(self):
        raw = 'Here is the result:\n[{"claim": "embedded"}]\nEnd.'
        result = parse_json_response(raw)
        assert result[0]["claim"] == "embedded"

    def test_invalid_json_raises(self):
        with pytest.raises((ValueError, json.JSONDecodeError)):
            parse_json_response("this is not json at all")


class TestComputeAccuracyScore:
    def test_all_verified(self):
        results = [{"status": "Verified"}] * 5
        assert compute_accuracy_score(results) == 100.0

    def test_none_verified(self):
        results = [{"status": "False"}] * 5
        assert compute_accuracy_score(results) == 0.0

    def test_mixed(self):
        results = [
            {"status": "Verified"},
            {"status": "Verified"},
            {"status": "Inaccurate"},
            {"status": "False"},
        ]
        assert compute_accuracy_score(results) == 50.0

    def test_empty_list(self):
        assert compute_accuracy_score([]) == 0.0


class TestComputeAvgConfidence:
    def test_all_full_confidence(self):
        results = [{"confidence": 1.0}] * 4
        assert compute_avg_confidence(results) == 100.0

    def test_mixed_confidence(self):
        results = [{"confidence": 0.8}, {"confidence": 0.6}]
        assert compute_avg_confidence(results) == 70.0

    def test_missing_confidence_key(self):
        results = [{"status": "Verified"}]
        assert compute_avg_confidence(results) == 0.0


class TestTruncateText:
    def test_short_text_unchanged(self):
        text = "Short text"
        assert truncate_text(text, 100) == text

    def test_long_text_truncated(self):
        text = "A" * 200
        result = truncate_text(text, 100)
        assert len(result) > 100
        assert "truncated" in result

    def test_exact_length_unchanged(self):
        text = "A" * 50
        assert truncate_text(text, 50) == text


class TestSafeGet:
    def test_key_exists(self):
        assert safe_get({"a": "b"}, "a") == "b"

    def test_key_missing_returns_default(self):
        assert safe_get({}, "missing") == ""

    def test_none_value_returns_default(self):
        assert safe_get({"key": None}, "key", "fallback") == "fallback"

    def test_custom_default(self):
        assert safe_get({}, "x", 42) == 42


# ── retry ────────────────────────────────────────────────────────────────────

from utils.retry import retry_with_backoff, safe_call


class TestRetryWithBackoff:
    def test_succeeds_first_try(self):
        call_count = 0

        @retry_with_backoff(max_retries=3, base_delay=0.01)
        def always_succeeds():
            nonlocal call_count
            call_count += 1
            return "ok"

        result = always_succeeds()
        assert result == "ok"
        assert call_count == 1

    def test_retries_on_failure(self):
        call_count = 0

        @retry_with_backoff(max_retries=3, base_delay=0.01)
        def fails_twice():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("transient error")
            return "recovered"

        result = fails_twice()
        assert result == "recovered"
        assert call_count == 3

    def test_raises_after_max_retries(self):
        @retry_with_backoff(max_retries=2, base_delay=0.01)
        def always_fails():
            raise RuntimeError("permanent error")

        with pytest.raises(RuntimeError, match="permanent error"):
            always_fails()


class TestSafeCall:
    def test_returns_result_on_success(self):
        result = safe_call(lambda: 42)
        assert result == 42

    def test_returns_fallback_on_exception(self):
        def raises():
            raise ValueError("boom")
        result = safe_call(raises, fallback="default")
        assert result == "default"

    def test_default_fallback_is_none(self):
        result = safe_call(lambda: 1 / 0)
        assert result is None


# ── report_service ────────────────────────────────────────────────────────────

from services.report_service import generate_csv_report, generate_summary_stats


SAMPLE_RESULTS = [
    {"claim": "Apple was founded in 1976", "status": "Verified", "confidence": 0.95,
     "reason": "Confirmed by multiple sources", "correct_fact": "", "source": "wikipedia.org",
     "source_credibility": 0.9},
    {"claim": "Tesla was founded in 2001", "status": "False", "confidence": 0.88,
     "reason": "Tesla was founded in 2003", "correct_fact": "Tesla was founded in 2003",
     "source": "tesla.com", "source_credibility": 0.95},
    {"claim": "Google revenue was $280B in 2022", "status": "Inaccurate", "confidence": 0.72,
     "reason": "Slightly off — actual was $282.8B", "correct_fact": "$282.8 billion",
     "source": "abc.xyz", "source_credibility": 0.85},
]


class TestGenerateCsvReport:
    def test_returns_bytes(self):
        csv = generate_csv_report(SAMPLE_RESULTS)
        assert isinstance(csv, bytes)

    def test_contains_headers(self):
        csv = generate_csv_report(SAMPLE_RESULTS).decode("utf-8-sig")
        assert "Claim" in csv
        assert "Status" in csv
        assert "Confidence" in csv

    def test_contains_all_rows(self):
        csv = generate_csv_report(SAMPLE_RESULTS).decode("utf-8-sig")
        assert "Apple was founded in 1976" in csv
        assert "Tesla was founded in 2001" in csv
        assert "Google revenue" in csv

    def test_empty_results(self):
        csv = generate_csv_report([])
        assert isinstance(csv, bytes)


class TestGenerateSummaryStats:
    def test_counts_correct(self):
        stats = generate_summary_stats(SAMPLE_RESULTS)
        assert stats["total"] == 3
        assert stats["verified"] == 1
        assert stats["inaccurate"] == 1
        assert stats["false"] == 1

    def test_accuracy_score(self):
        stats = generate_summary_stats(SAMPLE_RESULTS)
        assert stats["accuracy_score"] == round(1 / 3 * 100, 1)

    def test_avg_confidence(self):
        stats = generate_summary_stats(SAMPLE_RESULTS)
        expected = round((0.95 + 0.88 + 0.72) / 3 * 100, 1)
        assert stats["avg_confidence"] == expected

    def test_generated_at_present(self):
        stats = generate_summary_stats(SAMPLE_RESULTS)
        assert "generated_at" in stats
        assert len(stats["generated_at"]) > 0

from pathlib import Path

from src.gateway_report import (
    REPORT_PATH,
    build_gateway_report,
    load_gateway_results,
    write_gateway_report,
)
from src.gateway_runner import run_gateway


def test_gateway_report_counts_statuses():
    results = [result.__dict__ for result in run_gateway()]

    report = build_gateway_report(results)

    assert report["total_requests"] == 7
    assert report["successful_requests"] == 3
    assert report["rejected_requests"] == 4
    assert report["failed_requests"] == 0


def test_gateway_report_detects_release_gate_passed():
    results = [result.__dict__ for result in run_gateway()]

    report = build_gateway_report(results)

    assert report["release_gate_passed"] is True
    assert report["release_gate_reason"] == "passed"


def test_gateway_report_detects_redaction_failure():
    results = [
        {
            "request_id": "req-test",
            "status": "success",
            "reason": "primary_provider_success",
            "response": "Email alex@example.com",
            "trace": {
                "redacted_prompt": "Contact alex@example.com",
            },
        }
    ]

    report = build_gateway_report(results)

    assert report["release_gate_passed"] is False
    assert report["redaction_findings"]


def test_gateway_report_file_is_written():
    results = load_gateway_results()
    report = build_gateway_report(results)

    write_gateway_report(report)

    assert Path(REPORT_PATH).exists()

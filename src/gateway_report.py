import json
from collections import Counter
from pathlib import Path
from typing import Any

from src.gateway_runner import OUTPUT_PATH, run_gateway


REPORT_PATH = Path("reports/gateway_policy_report.json")


def load_gateway_results(path: Path = OUTPUT_PATH) -> list[dict[str, Any]]:
    if not path.exists():
        run_gateway()

    return json.loads(path.read_text(encoding="utf-8"))


def build_gateway_report(results: list[dict[str, Any]]) -> dict[str, Any]:
    status_counts = Counter(result["status"] for result in results)
    reason_counts = Counter(result["reason"] for result in results)

    total_requests = len(results)
    successful_requests = status_counts.get("success", 0)
    rejected_requests = status_counts.get("rejected", 0)
    failed_requests = status_counts.get("failed", 0)

    redaction_findings = []
    for result in results:
        trace = result.get("trace", {})
        redacted_prompt = trace.get("redacted_prompt", "")
        response = result.get("response") or ""

        if "@" in redacted_prompt or "@example.com" in response:
            redaction_findings.append(
                {
                    "request_id": result["request_id"],
                    "finding": "possible unredacted email",
                }
            )

        if "key-" in redacted_prompt or "key-" in response:
            redaction_findings.append(
                {
                    "request_id": result["request_id"],
                    "finding": "possible unredacted api key",
                }
            )

    release_gate_passed = failed_requests == 0 and len(redaction_findings) == 0

    return {
        "total_requests": total_requests,
        "status_counts": dict(status_counts),
        "reason_counts": dict(reason_counts),
        "successful_requests": successful_requests,
        "rejected_requests": rejected_requests,
        "failed_requests": failed_requests,
        "redaction_findings": redaction_findings,
        "release_gate_passed": release_gate_passed,
        "release_gate_reason": (
            "passed"
            if release_gate_passed
            else "failed due to gateway failures or redaction findings"
        ),
    }


def write_gateway_report(report: dict[str, Any], path: Path = REPORT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")


def main() -> None:
    results = load_gateway_results()
    report = build_gateway_report(results)
    write_gateway_report(report)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

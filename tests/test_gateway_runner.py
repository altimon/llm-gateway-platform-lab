from pathlib import Path

from src.gateway_runner import run_gateway


def test_gateway_runner_processes_all_requests():
    results = run_gateway()

    assert len(results) == 7


def test_gateway_runner_rejects_invalid_api_key():
    results = run_gateway()
    result_by_id = {result.request_id: result for result in results}

    assert result_by_id["req-002"].status == "rejected"
    assert result_by_id["req-002"].reason == "invalid api key"


def test_gateway_runner_rejects_unauthorized_template_access():
    results = run_gateway()
    result_by_id = {result.request_id: result for result in results}

    assert result_by_id["req-003"].status == "rejected"
    assert result_by_id["req-003"].reason == "template access denied"


def test_gateway_runner_enforces_rate_limit():
    results = run_gateway()
    result_by_id = {result.request_id: result for result in results}

    assert result_by_id["req-005"].status == "rejected"
    assert result_by_id["req-005"].reason == "rate limit exceeded"


def test_gateway_runner_uses_provider_fallback():
    results = run_gateway()
    result_by_id = {result.request_id: result for result in results}

    assert result_by_id["req-006"].status == "success"
    assert result_by_id["req-006"].reason == "fallback_used"


def test_gateway_runner_rejects_missing_prompt_variable():
    results = run_gateway()
    result_by_id = {result.request_id: result for result in results}

    assert result_by_id["req-007"].status == "rejected"
    assert "missing prompt variables" in result_by_id["req-007"].reason


def test_gateway_runner_writes_output_files():
    run_gateway()

    assert Path("data/output/gateway_results.json").exists()
    assert Path("reports/gateway_trace.json").exists()

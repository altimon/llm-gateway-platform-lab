import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.auth import authenticate_client, authorize_template_access
from src.gateway_data import (
    load_clients,
    load_gateway_requests,
    load_policy_config,
    load_prompt_templates,
    load_rate_limits,
)
from src.gateway_types import GatewayRequest, GatewayResult
from src.prompt_templates import get_template_version, render_prompt, validate_prompt_variables
from src.provider_simulator import ProviderError, call_provider_with_fallback
from src.rate_limits import RateLimiter
from src.redaction import build_safe_log_record


OUTPUT_PATH = Path("data/output/gateway_results.json")
TRACE_PATH = Path("reports/gateway_trace.json")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def reject_result(
    request: GatewayRequest,
    status: str,
    reason: str,
    trace: dict[str, Any],
) -> GatewayResult:
    return GatewayResult(
        request_id=request.request_id,
        client_id=request.client_id,
        template_id=request.template_id,
        status=status,
        reason=reason,
        response=None,
        trace=trace,
    )


def process_request(
    request: GatewayRequest,
    clients: dict,
    templates: dict,
    limiter: RateLimiter,
    policy_config: dict[str, Any],
) -> GatewayResult:
    trace: dict[str, Any] = {
        "request_id": request.request_id,
        "client_id": request.client_id,
        "template_id": request.template_id,
        "started_at": utc_now(),
        "steps": [],
    }

    auth_ok, auth_reason = authenticate_client(request, clients)
    trace["steps"].append({"step": "authentication", "ok": auth_ok, "reason": auth_reason})
    if not auth_ok:
        return reject_result(request, "rejected", auth_reason, trace)

    authorization_ok, authorization_reason = authorize_template_access(request, clients)
    trace["steps"].append(
        {"step": "authorization", "ok": authorization_ok, "reason": authorization_reason}
    )
    if not authorization_ok:
        return reject_result(request, "rejected", authorization_reason, trace)

    rate_ok, rate_reason = limiter.check_and_increment(request.client_id)
    trace["steps"].append({"step": "rate_limit", "ok": rate_ok, "reason": rate_reason})
    if not rate_ok:
        return reject_result(request, "rejected", rate_reason, trace)

    template = templates.get(request.template_id)
    if template is None:
        trace["steps"].append({"step": "template_lookup", "ok": False, "reason": "template not found"})
        return reject_result(request, "rejected", "template not found", trace)

    trace["template_version"] = get_template_version(template)

    variables_ok, variables_reason = validate_prompt_variables(request, template)
    trace["steps"].append(
        {"step": "prompt_variable_validation", "ok": variables_ok, "reason": variables_reason}
    )
    if not variables_ok:
        return reject_result(request, "rejected", variables_reason, trace)

    prompt = render_prompt(request, template)
    safe_prompt_record = build_safe_log_record({"prompt": prompt}, policy_config)
    trace["redacted_prompt"] = safe_prompt_record["prompt"]

    try:
        response, provider_status = call_provider_with_fallback(
            prompt,
            request,
            fallback_enabled=policy_config.get("fallback_enabled", True),
        )
        trace["steps"].append({"step": "provider_call", "ok": True, "reason": provider_status})
    except ProviderError as error:
        trace["steps"].append({"step": "provider_call", "ok": False, "reason": str(error)})
        return reject_result(request, "failed", str(error), trace)

    safe_response = build_safe_log_record({"response": response}, policy_config)["response"]
    trace["finished_at"] = utc_now()

    return GatewayResult(
        request_id=request.request_id,
        client_id=request.client_id,
        template_id=request.template_id,
        status="success",
        reason=provider_status,
        response=safe_response,
        trace=trace,
    )


def result_to_dict(result: GatewayResult) -> dict[str, Any]:
    return {
        "request_id": result.request_id,
        "client_id": result.client_id,
        "template_id": result.template_id,
        "status": result.status,
        "reason": result.reason,
        "response": result.response,
        "trace": result.trace,
    }


def run_gateway() -> list[GatewayResult]:
    clients = load_clients()
    templates = load_prompt_templates()
    requests = load_gateway_requests()
    rate_limits = load_rate_limits()
    policy_config = load_policy_config()

    limiter = RateLimiter(rate_limits)
    results = [
        process_request(
            request=request,
            clients=clients,
            templates=templates,
            limiter=limiter,
            policy_config=policy_config,
        )
        for request in requests
    ]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)

    result_records = [result_to_dict(result) for result in results]

    OUTPUT_PATH.write_text(json.dumps(result_records, indent=2), encoding="utf-8")
    TRACE_PATH.write_text(
        json.dumps([result.trace for result in results], indent=2),
        encoding="utf-8",
    )

    return results


def main() -> None:
    results = run_gateway()
    for result in results:
        print(f"{result.request_id}: {result.status}: {result.reason}")


if __name__ == "__main__":
    main()

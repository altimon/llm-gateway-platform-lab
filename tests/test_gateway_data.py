from src.gateway_data import (
    load_clients,
    load_gateway_requests,
    load_policy_config,
    load_prompt_templates,
    load_rate_limits,
)


def test_load_clients_by_client_id():
    clients = load_clients()

    assert "frontend-app" in clients
    assert clients["frontend-app"].team == "product"
    assert "support_answer_v1" in clients["frontend-app"].allowed_templates


def test_load_prompt_templates_by_template_id():
    templates = load_prompt_templates()

    assert "incident_summary_v1" in templates
    assert templates["incident_summary_v1"].version == "1.0.0"
    assert "incident_notes" in templates["incident_summary_v1"].required_variables


def test_load_gateway_requests():
    requests = load_gateway_requests()

    assert len(requests) == 7
    assert requests[0].request_id == "req-001"
    assert requests[-1].template_id == "incident_summary_v1"


def test_load_rate_limits():
    rate_limits = load_rate_limits()

    assert rate_limits["frontend-app"]["max_requests"] == 2
    assert rate_limits["internal-sre-bot"]["max_requests"] == 3


def test_load_policy_config():
    policy = load_policy_config()

    assert policy["redact_email"] is True
    assert policy["fallback_enabled"] is True

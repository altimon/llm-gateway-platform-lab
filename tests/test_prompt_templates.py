import pytest

from src.gateway_data import load_prompt_templates
from src.gateway_types import GatewayRequest
from src.prompt_templates import (
    get_template_version,
    render_prompt,
    validate_prompt_variables,
)


def make_request(variables: dict) -> GatewayRequest:
    return GatewayRequest(
        request_id="test-req",
        client_id="frontend-app",
        api_key="key-frontend-valid",
        template_id="support_answer_v1",
        variables=variables,
    )


def test_prompt_variables_are_valid_when_required_fields_exist():
    templates = load_prompt_templates()
    template = templates["support_answer_v1"]
    request = make_request(
        {
            "question": "How do I reset my password?",
            "context": "Use account settings.",
        }
    )

    is_valid, reason = validate_prompt_variables(request, template)

    assert is_valid is True
    assert reason == "prompt variables valid"


def test_missing_prompt_variable_is_rejected():
    templates = load_prompt_templates()
    template = templates["support_answer_v1"]
    request = make_request({"question": "How do I reset my password?"})

    is_valid, reason = validate_prompt_variables(request, template)

    assert is_valid is False
    assert "missing prompt variables" in reason
    assert "context" in reason


def test_prompt_renders_with_variables():
    templates = load_prompt_templates()
    template = templates["support_answer_v1"]
    request = make_request(
        {
            "question": "How do I reset my password?",
            "context": "Use account settings.",
        }
    )

    rendered = render_prompt(request, template)

    assert "How do I reset my password?" in rendered
    assert "Use account settings." in rendered


def test_render_prompt_raises_for_missing_variable():
    templates = load_prompt_templates()
    template = templates["support_answer_v1"]
    request = make_request({"question": "How do I reset my password?"})

    with pytest.raises(ValueError):
        render_prompt(request, template)


def test_template_version_is_traceable():
    templates = load_prompt_templates()
    template = templates["support_answer_v1"]

    assert get_template_version(template) == "support_answer_v1:1.0.0"

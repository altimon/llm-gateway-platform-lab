import pytest

from src.gateway_types import GatewayRequest
from src.provider_simulator import ProviderError, call_provider, call_provider_with_fallback


def make_request(simulate_provider_failure: bool = False) -> GatewayRequest:
    return GatewayRequest(
        request_id="test-req",
        client_id="frontend-app",
        api_key="key-frontend-valid",
        template_id="support_answer_v1",
        variables={},
        simulate_provider_failure=simulate_provider_failure,
    )


def test_provider_returns_simulated_response():
    request = make_request()

    response = call_provider("hello gateway", request)

    assert response.startswith("simulated_provider_response")
    assert "hello gateway" in response


def test_provider_failure_raises_error():
    request = make_request(simulate_provider_failure=True)

    with pytest.raises(ProviderError):
        call_provider("hello gateway", request)


def test_provider_fallback_is_used_when_enabled():
    request = make_request(simulate_provider_failure=True)

    response, status = call_provider_with_fallback(
        "hello gateway",
        request,
        fallback_enabled=True,
    )

    assert status == "fallback_used"
    assert response.startswith("fallback_response")


def test_provider_failure_raises_when_fallback_disabled():
    request = make_request(simulate_provider_failure=True)

    with pytest.raises(ProviderError):
        call_provider_with_fallback(
            "hello gateway",
            request,
            fallback_enabled=False,
        )

from src.auth import authenticate_client, authorize_template_access
from src.gateway_data import load_clients
from src.gateway_types import GatewayRequest


def make_request(
    client_id: str = "frontend-app",
    api_key: str = "key-frontend-valid",
    template_id: str = "support_answer_v1",
) -> GatewayRequest:
    return GatewayRequest(
        request_id="test-req",
        client_id=client_id,
        api_key=api_key,
        template_id=template_id,
        variables={},
    )


def test_valid_client_authenticates():
    clients = load_clients()
    request = make_request()

    is_valid, reason = authenticate_client(request, clients)

    assert is_valid is True
    assert reason == "authenticated"


def test_invalid_api_key_is_rejected():
    clients = load_clients()
    request = make_request(api_key="wrong-key")

    is_valid, reason = authenticate_client(request, clients)

    assert is_valid is False
    assert reason == "invalid api key"


def test_unknown_client_is_rejected():
    clients = load_clients()
    request = make_request(client_id="missing-client")

    is_valid, reason = authenticate_client(request, clients)

    assert is_valid is False
    assert reason == "unknown client"


def test_authorized_template_access_is_allowed():
    clients = load_clients()
    request = make_request(template_id="support_answer_v1")

    is_allowed, reason = authorize_template_access(request, clients)

    assert is_allowed is True
    assert reason == "authorized"


def test_unauthorized_template_access_is_denied():
    clients = load_clients()
    request = make_request(template_id="incident_summary_v1")

    is_allowed, reason = authorize_template_access(request, clients)

    assert is_allowed is False
    assert reason == "template access denied"

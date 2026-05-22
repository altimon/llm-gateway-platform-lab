from src.gateway_data import load_clients
from src.gateway_types import Client, GatewayRequest


def authenticate_client(
    request: GatewayRequest,
    clients: dict[str, Client],
) -> tuple[bool, str]:
    client = clients.get(request.client_id)

    if client is None:
        return False, "unknown client"

    if request.api_key != client.api_key:
        return False, "invalid api key"

    return True, "authenticated"


def authorize_template_access(
    request: GatewayRequest,
    clients: dict[str, Client],
) -> tuple[bool, str]:
    client = clients.get(request.client_id)

    if client is None:
        return False, "unknown client"

    if request.template_id not in client.allowed_templates:
        return False, "template access denied"

    return True, "authorized"


def main() -> None:
    clients = load_clients()
    print(f"loaded {len(clients)} clients")


if __name__ == "__main__":
    main()

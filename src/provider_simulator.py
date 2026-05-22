from src.gateway_types import GatewayRequest


class ProviderError(RuntimeError):
    pass


def call_provider(prompt: str, request: GatewayRequest) -> str:
    if request.simulate_provider_failure:
        raise ProviderError("simulated provider failure")

    return f"simulated_provider_response: {prompt[:80]}"


def call_provider_with_fallback(
    prompt: str,
    request: GatewayRequest,
    fallback_enabled: bool = True,
) -> tuple[str, str]:
    try:
        response = call_provider(prompt, request)
        return response, "primary_provider_success"
    except ProviderError:
        if fallback_enabled:
            return "fallback_response: provider unavailable, request queued for retry", "fallback_used"

        raise


def main() -> None:
    from src.gateway_data import load_gateway_requests

    requests = load_gateway_requests()

    for request in requests:
        response, provider_status = call_provider_with_fallback(
            prompt="test prompt",
            request=request,
            fallback_enabled=True,
        )
        print(f"{request.request_id}: {provider_status}: {response}")


if __name__ == "__main__":
    main()

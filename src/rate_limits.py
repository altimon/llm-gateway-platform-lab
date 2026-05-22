from collections import defaultdict

from src.gateway_data import load_gateway_requests, load_rate_limits


class RateLimiter:
    def __init__(self, limits: dict[str, dict[str, int]]) -> None:
        self.limits = limits
        self.counters: dict[str, int] = defaultdict(int)

    def check_and_increment(self, client_id: str) -> tuple[bool, str]:
        client_limit = self.limits.get(client_id)

        if client_limit is None:
            return False, "missing rate limit policy"

        max_requests = client_limit["max_requests"]
        current_count = self.counters[client_id]

        if current_count >= max_requests:
            return False, "rate limit exceeded"

        self.counters[client_id] += 1
        return True, "rate limit allowed"

    def get_count(self, client_id: str) -> int:
        return self.counters[client_id]


def main() -> None:
    limits = load_rate_limits()
    requests = load_gateway_requests()
    limiter = RateLimiter(limits)

    for request in requests:
        allowed, reason = limiter.check_and_increment(request.client_id)
        print(f"{request.request_id}: {request.client_id}: {allowed}: {reason}")


if __name__ == "__main__":
    main()

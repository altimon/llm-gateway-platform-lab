from src.rate_limits import RateLimiter


def test_request_within_limit_is_allowed():
    limiter = RateLimiter({"frontend-app": {"max_requests": 2}})

    allowed, reason = limiter.check_and_increment("frontend-app")

    assert allowed is True
    assert reason == "rate limit allowed"
    assert limiter.get_count("frontend-app") == 1


def test_request_over_limit_is_rejected():
    limiter = RateLimiter({"frontend-app": {"max_requests": 2}})

    assert limiter.check_and_increment("frontend-app")[0] is True
    assert limiter.check_and_increment("frontend-app")[0] is True

    allowed, reason = limiter.check_and_increment("frontend-app")

    assert allowed is False
    assert reason == "rate limit exceeded"
    assert limiter.get_count("frontend-app") == 2


def test_missing_rate_limit_policy_is_rejected():
    limiter = RateLimiter({})

    allowed, reason = limiter.check_and_increment("unknown-client")

    assert allowed is False
    assert reason == "missing rate limit policy"

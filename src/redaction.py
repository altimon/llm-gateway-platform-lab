import re
from typing import Any


EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
API_KEY_PATTERN = re.compile(r"\bkey-[A-Za-z0-9-]+\b")


def redact_text(text: str, redact_email: bool = True, redact_api_keys: bool = True) -> str:
    redacted = text

    if redact_email:
        redacted = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", redacted)

    if redact_api_keys:
        redacted = API_KEY_PATTERN.sub("[REDACTED_API_KEY]", redacted)

    return redacted


def redact_value(value: Any, redact_email: bool = True, redact_api_keys: bool = True) -> Any:
    if isinstance(value, str):
        return redact_text(value, redact_email=redact_email, redact_api_keys=redact_api_keys)

    if isinstance(value, dict):
        return {
            key: redact_value(item, redact_email=redact_email, redact_api_keys=redact_api_keys)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            redact_value(item, redact_email=redact_email, redact_api_keys=redact_api_keys)
            for item in value
        ]

    return value


def build_safe_log_record(record: dict[str, Any], policy_config: dict[str, Any]) -> dict[str, Any]:
    return redact_value(
        record,
        redact_email=policy_config.get("redact_email", True),
        redact_api_keys=policy_config.get("redact_api_keys", True),
    )


def main() -> None:
    sample = {
        "client_id": "frontend-app",
        "api_key": "key-frontend-valid",
        "message": "Customer alex@example.com reported an issue.",
    }
    policy = {"redact_email": True, "redact_api_keys": True}
    print(build_safe_log_record(sample, policy))


if __name__ == "__main__":
    main()

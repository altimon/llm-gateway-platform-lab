from src.redaction import build_safe_log_record, redact_text, redact_value


def test_email_is_redacted_from_text():
    text = "Customer alex@example.com reported billing issue."

    redacted = redact_text(text)

    assert "alex@example.com" not in redacted
    assert "[REDACTED_EMAIL]" in redacted


def test_api_key_is_redacted_from_text():
    text = "request used key-frontend-valid"

    redacted = redact_text(text)

    assert "key-frontend-valid" not in redacted
    assert "[REDACTED_API_KEY]" in redacted


def test_nested_values_are_redacted():
    value = {
        "message": "Contact alex@example.com",
        "nested": {
            "api_key": "key-sre-valid",
        },
    }

    redacted = redact_value(value)

    assert redacted["message"] == "Contact [REDACTED_EMAIL]"
    assert redacted["nested"]["api_key"] == "[REDACTED_API_KEY]"


def test_safe_log_record_uses_policy_config():
    record = {
        "api_key": "key-frontend-valid",
        "body": "Email alex@example.com",
    }
    policy = {
        "redact_email": True,
        "redact_api_keys": True,
    }

    safe_record = build_safe_log_record(record, policy)

    assert safe_record["api_key"] == "[REDACTED_API_KEY]"
    assert safe_record["body"] == "Email [REDACTED_EMAIL]"

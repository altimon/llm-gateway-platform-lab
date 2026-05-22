import json
from pathlib import Path
from typing import Any

from src.gateway_types import Client, GatewayRequest, PromptTemplate


BASE_INPUT_DIR = Path("data/input")


def load_json(path: str | Path) -> Any:
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_clients(path: str | Path = BASE_INPUT_DIR / "clients.json") -> dict[str, Client]:
    records = load_json(path)
    return {
        item["client_id"]: Client(
            client_id=item["client_id"],
            api_key=item["api_key"],
            team=item["team"],
            allowed_templates=item["allowed_templates"],
        )
        for item in records
    }


def load_prompt_templates(
    path: str | Path = BASE_INPUT_DIR / "prompt_templates.json",
) -> dict[str, PromptTemplate]:
    records = load_json(path)
    return {
        item["template_id"]: PromptTemplate(
            template_id=item["template_id"],
            version=item["version"],
            owner_team=item["owner_team"],
            required_variables=item["required_variables"],
            template=item["template"],
        )
        for item in records
    }


def load_gateway_requests(
    path: str | Path = BASE_INPUT_DIR / "gateway_requests.json",
) -> list[GatewayRequest]:
    records = load_json(path)
    return [
        GatewayRequest(
            request_id=item["request_id"],
            client_id=item["client_id"],
            api_key=item["api_key"],
            template_id=item["template_id"],
            variables=item["variables"],
            simulate_provider_failure=item.get("simulate_provider_failure", False),
        )
        for item in records
    ]


def load_rate_limits(path: str | Path = BASE_INPUT_DIR / "rate_limits.json") -> dict[str, dict[str, int]]:
    return load_json(path)


def load_policy_config(path: str | Path = BASE_INPUT_DIR / "policy_config.json") -> dict[str, Any]:
    return load_json(path)

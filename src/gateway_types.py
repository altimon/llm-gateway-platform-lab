from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Client:
    client_id: str
    api_key: str
    team: str
    allowed_templates: list[str]


@dataclass(frozen=True)
class PromptTemplate:
    template_id: str
    version: str
    owner_team: str
    required_variables: list[str]
    template: str


@dataclass(frozen=True)
class GatewayRequest:
    request_id: str
    client_id: str
    api_key: str
    template_id: str
    variables: dict[str, Any]
    simulate_provider_failure: bool = False


@dataclass(frozen=True)
class GatewayResult:
    request_id: str
    client_id: str
    template_id: str
    status: str
    reason: str
    response: str | None
    trace: dict[str, Any]

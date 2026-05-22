from src.gateway_data import load_gateway_requests, load_prompt_templates
from src.gateway_types import GatewayRequest, PromptTemplate


def validate_prompt_variables(
    request: GatewayRequest,
    template: PromptTemplate,
) -> tuple[bool, str]:
    missing_variables = [
        variable
        for variable in template.required_variables
        if variable not in request.variables
    ]

    if missing_variables:
        return False, f"missing prompt variables: {missing_variables}"

    return True, "prompt variables valid"


def render_prompt(
    request: GatewayRequest,
    template: PromptTemplate,
) -> str:
    is_valid, reason = validate_prompt_variables(request, template)

    if not is_valid:
        raise ValueError(reason)

    return template.template.format(**request.variables)


def get_template_version(template: PromptTemplate) -> str:
    return f"{template.template_id}:{template.version}"


def main() -> None:
    templates = load_prompt_templates()
    requests = load_gateway_requests()

    for request in requests:
        template = templates.get(request.template_id)
        if template is None:
            print(f"{request.request_id}: template not found")
            continue

        is_valid, reason = validate_prompt_variables(request, template)
        print(f"{request.request_id}: {template.template_id}:{template.version}: {is_valid}: {reason}")


if __name__ == "__main__":
    main()

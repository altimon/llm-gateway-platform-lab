# LLM Gateway Platform Lab

A local LLM gateway simulation that demonstrates how a platform team can control access to model providers through client authentication, prompt templates, provider simulation, rate limits, policy checks, redaction, trace output, and testable platform guardrails.

This project is not about training or fine-tuning a model. It focuses on the operational control plane around safe, reliable, and auditable LLM access.

## Project goal

Demonstrate practical AI platform engineering patterns:

- authenticate gateway clients
- apply prompt templates consistently
- route requests through a provider abstraction
- enforce rate limits
- redact sensitive request data
- evaluate policy decisions
- produce traceable gateway output
- validate behavior through tests and generated reports

The lab is local-first and uses simulated providers so the full workflow can run without paid APIs or external model access.

## Why an LLM gateway exists

Teams often start by calling model APIs directly from applications. That works for prototypes, but it becomes hard to operate when multiple applications need shared controls.

An LLM gateway creates a controlled platform layer between application teams and model providers.

```text
application / service
        |
        v
LLM gateway
  - client authentication
  - prompt templates
  - request policy
  - rate limiting
  - redaction
  - provider routing
  - trace/audit records
        |
        v
model provider or simulator
```

This pattern is similar to an API gateway or service-mesh control point, but with LLM-specific concerns such as prompt versions, token and cost awareness, sensitive input handling, provider latency, fallback behavior, and safety evidence.

## What this demonstrates

- API-gateway-style control for LLM access
- client identity and authentication checks
- request validation and policy enforcement
- reusable prompt templates
- provider simulation for deterministic local tests
- rate-limit enforcement
- sensitive input redaction
- trace and report generation
- testable AI platform guardrails
- clear separation between application requests and provider execution

## Local flow

```text
data/input/clients.json
data/input/gateway_requests.json
data/input/prompt_templates.json
data/input/policy_config.json
data/input/rate_limits.json
        |
        v
gateway runner
        |
        +--> auth check
        +--> prompt template rendering
        +--> rate-limit check
        +--> policy/redaction
        +--> provider simulator
        |
        v
data/output/gateway_results.json
reports/gateway_policy_report.json
reports/gateway_trace.json
```

Generated output is ignored by git except for placeholder files.

## Repository structure

```text
data/
  input/
    clients.json
    gateway_requests.json
    policy_config.json
    prompt_templates.json
    rate_limits.json
  output/
    .gitkeep

src/
  auth.py
  gateway_data.py
  gateway_report.py
  gateway_runner.py
  gateway_types.py
  prompt_templates.py
  provider_simulator.py
  rate_limits.py
  redaction.py

tests/
  test_auth.py
  test_gateway_data.py
  test_gateway_report.py
  test_gateway_runner.py
  test_prompt_templates.py
  test_provider_simulator.py
  test_rate_limits.py
  test_redaction.py

reports/
  .gitkeep

Makefile
requirements.txt
pytest.ini
README.md
NOTES.md
STATUS.md
```

## Prerequisites

- Python 3.11 or newer
- make
- zsh or bash-compatible shell

This project has no dependency on external LLM APIs.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

make test
make run
```

Or use the Makefile targets directly if your environment is already prepared.

## Makefile targets

Run:

```bash
make help
```

Common targets:

| Target | Purpose |
|---|---|
| `make test` | run the pytest suite |
| `make run` | execute the gateway simulation |
| `make report` | generate gateway reports |
| `make clean` | remove local generated output |
| `make status` | show project status, if available |

Target names may vary slightly depending on the local Makefile. Use `make help` as the source of truth.

## Validation

Run:

```bash
make test
sleep 5
```

Expected result:

```text
all tests pass
```

This repo has test coverage for:

- valid and invalid client authentication
- request loading and schema handling
- prompt template rendering
- provider simulation
- rate-limit behavior
- redaction of sensitive values
- gateway runner behavior
- generated report structure

## Expected output

A successful run should produce local generated files such as:

```text
data/output/gateway_results.json
reports/gateway_policy_report.json
reports/gateway_trace.json
```

These files are generated artifacts and should not be committed unless intentionally converted into documented examples.

## Public safety notes

The repo uses fake API-key-like values such as `key-frontend-valid` and `key-sre-valid` as local test fixtures. They are not real credentials.

The redaction logic intentionally searches for these patterns to prove that API keys and sensitive-looking values are removed from safe logs and trace records.

## Production mapping

In a production environment, this pattern would map to:

- identity-aware gateway access
- tenant-aware rate limits
- model/provider routing policy
- prompt-template versioning
- request and response redaction
- audit logs and traces
- fallback and retry policy
- safety checks before provider calls
- cost and latency controls
- centralized observability for model access

This local simulation focuses on the platform control plane, not model training.

## Portfolio talking points

- I built this as a local LLM gateway simulation to show the platform layer around safe model access.
- The repo demonstrates gateway concerns that matter in production: auth, rate limits, prompt templates, redaction, traceability, and policy checks.
- It uses provider simulation so behavior is deterministic and testable without depending on external APIs.
- The redaction and trace paths show how sensitive request data can be controlled before logs or reports are produced.
- I would not claim this as model-training work; it is platform engineering for reliable and governed LLM usage.

## Limitations

This is a local simulation, not a production LLM gateway.

Production use would require:

- real identity provider integration
- service-to-service authentication
- encrypted secrets management
- persistent audit storage
- real provider adapters
- streaming support
- fallback and retry behavior
- cost tracking and budgets
- latency SLOs
- observability dashboards
- security review and abuse testing

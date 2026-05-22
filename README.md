# MLOps Day 13 — LLM Gateway Simulation

## Topic

Phase 2 — RAG / LLM Infrastructure  
Day 13 — LLM gateway: rate limits, auth, prompt templates, logging

## Goal

This project builds a simplified local LLM gateway simulation using Python, JSON input files, pytest tests, Makefile targets, generated JSON reports, and no paid LLM APIs.

The goal is to understand the platform/SRE responsibilities around controlled LLM access:

- authentication
- authorization
- request validation
- rate limiting
- prompt template selection and version tracking
- provider/model call simulation
- provider failure fallback
- logging redaction
- trace generation
- CI-friendly gateway policy report

## Why an LLM Gateway Exists

Applications should not call model providers directly when production controls are required.

A gateway centralizes:

- who can call the model layer
- which client can use which prompt template
- request quotas and budget protection
- prompt template version traceability
- provider routing and fallback
- redacted logging
- audit reporting
- operational debugging

This is similar to an API gateway or service mesh pattern, but with LLM-specific concerns such as prompt versions, token/cost awareness, provider latency, sensitive input handling, and safety/audit evidence.

## Local Flow

```text
gateway clients
→ prompt templates
→ gateway requests
→ auth check
→ authorization check
→ rate limit check
→ prompt template render
→ simulated provider response
→ log redaction
→ gateway trace
→ policy report
```

## Project Structure

```text
requirements.txt
.gitignore
pytest.ini
Makefile
README.md
STATUS.md
DAY13_NOTES.md

data/input/
data/output/
reports/

data/input/clients.json
data/input/prompt_templates.json
data/input/gateway_requests.json
data/input/rate_limits.json
data/input/policy_config.json

src/gateway_types.py
src/gateway_data.py
src/auth.py
src/rate_limits.py
src/prompt_templates.py
src/redaction.py
src/provider_simulator.py
src/gateway_runner.py
src/gateway_report.py

tests/test_project_bootstrap.py
tests/test_gateway_data.py
tests/test_auth.py
tests/test_rate_limits.py
tests/test_prompt_templates.py
tests/test_redaction.py
tests/test_provider_simulator.py
tests/test_gateway_runner.py
tests/test_gateway_report.py
```

## Makefile Targets

```bash
make install
make test
make clean
make auth-check
make rate-limit-check
make render-prompts
make run-gateway
make gateway-report
make pipeline
```

## Validation

Run:

```bash
make test
make clean
make pipeline
make test
git status --short --ignored
```

Expected:

- tests pass
- generated outputs are recreated by the pipeline
- generated output/report files are ignored by Git
- source, tests, config, and input data remain tracked

## Generated Artifacts

Pipeline output:

```text
data/output/gateway_results.json
reports/gateway_trace.json
reports/gateway_policy_report.json
```

These are generated artifacts and should not be committed.

## Production Mapping

| Local simulation | Production equivalent |
|---|---|
| `clients.json` | IAM, OIDC, service accounts, API keys, tenant registry |
| `rate_limits.json` | API Gateway quotas, Envoy/Kong/NGINX limits, Redis counters |
| `prompt_templates.json` | Prompt registry, config service, LangSmith prompts, LaunchDarkly |
| Python auth checks | API Gateway authorizer, OPA, IAM, OAuth/OIDC middleware |
| Python gateway runner | LLM gateway service, LiteLLM, Portkey, Kong plugin, custom gateway |
| Local provider simulator | OpenAI, Anthropic, Azure OpenAI, local vLLM/Ollama endpoint |
| Redaction script | DLP tooling, PII redaction service, logging pipeline filters |
| JSON logs | Datadog, OpenSearch, CloudWatch, Splunk |
| JSON reports | CI artifacts, audit reports, dashboards |
| Makefile | GitHub Actions, GitLab CI, Jenkins |
| Pytest | Gateway regression suite and merge gate |

## Interview-Ready Positioning

For an LLM gateway, I would focus on centralizing access to model providers instead of letting every application call providers directly. The gateway should enforce authentication, authorization, rate limits, prompt template versions, logging, redaction, and provider routing.

From a platform perspective, this is similar to operating an API gateway or service mesh layer, but with LLM-specific concerns such as prompt versions, token usage, provider latency, safety logging, and auditability. I would not claim to train or tune the LLM itself, but I can build and operate the control plane around safe and reliable model access.

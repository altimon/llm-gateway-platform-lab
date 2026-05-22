# DAY13_NOTES — LLM Gateway

## 1. LLM Gateway Purpose

Simple explanation:

An LLM gateway is a controlled entry point between applications and one or more LLM providers or local model services.

Why it matters in production:

Without a gateway, every application may implement model access differently. This creates inconsistent auth, quota, logging, prompt control, cost tracking, and audit behavior.

DevOps/SRE mapping:

This is similar to API gateway, ingress, service mesh, or platform middleware work.

Do not overclaim:

Do not claim that gateway work means owning model training or solving all model-safety issues.

Interview answer:

```text
An LLM gateway centralizes model access and applies platform controls such as auth, authorization, rate limits, prompt template versions, logging, redaction, routing, and audit reporting.
```

Local exercise:

Run the gateway simulation and inspect generated results:

```bash
make run-gateway
cat data/output/gateway_results.json
```

## 2. Authentication

Simple explanation:

Authentication verifies who is calling the gateway.

Why it matters in production:

Invalid or unknown clients must not reach model providers.

DevOps/SRE mapping:

Similar to API keys, IAM, service accounts, OAuth/OIDC, mTLS, or workload identity.

Do not overclaim:

Authentication does not prove the user request is safe or correct. It only verifies identity.

Interview answer:

```text
I would verify service or user identity before allowing access to the LLM layer, using API keys, OIDC, IAM, service accounts, or workload identity depending on the platform.
```

Local exercise:

```bash
make auth-check
make test
```

## 3. Authorization

Simple explanation:

Authorization decides what an authenticated client is allowed to access.

Why it matters in production:

A valid client should not automatically access every model, prompt template, tenant, or workflow.

DevOps/SRE mapping:

Similar to RBAC, IAM policies, OPA policies, Kubernetes RBAC, or service-level access controls.

Do not overclaim:

Authorization does not validate model output quality.

Interview answer:

```text
After authentication, I would enforce authorization so each service can only use approved templates, models, tenants, or workflows.
```

Local exercise:

Inspect `clients.json` and compare allowed templates with gateway request outcomes.

## 4. Rate Limiting

Simple explanation:

Rate limiting controls how many requests a client can make.

Why it matters in production:

It protects cost, provider capacity, latency, tenant fairness, and blast radius during bugs or abuse.

DevOps/SRE mapping:

Similar to API Gateway quotas, Envoy/Kong limits, NGINX limits, Redis counters, or cloud quota controls.

Do not overclaim:

A simple local counter is not production-grade distributed rate limiting.

Interview answer:

```text
I would enforce rate limits per service, team, tenant, and possibly model/provider to protect budget, reliability, and provider capacity.
```

Local exercise:

```bash
make rate-limit-check
```

## 5. Prompt Template Management

Simple explanation:

Prompt templates are controlled, versioned prompt definitions used by gateway requests.

Why it matters in production:

Prompt changes can alter behavior. Version tracking helps debugging, audits, rollbacks, and release reviews.

DevOps/SRE mapping:

Similar to managing configuration, Helm values, feature flags, deployment manifests, or service config versions.

Do not overclaim:

Versioned templates do not guarantee perfect model output.

Interview answer:

```text
I would treat prompt templates as versioned operational configuration, with IDs and versions logged for traceability.
```

Local exercise:

```bash
make render-prompts
```

## 6. Logging and Redaction

Simple explanation:

Gateway logs capture request flow and decisions, while redaction removes sensitive data before logs are stored.

Why it matters in production:

LLM requests may include personal data, credentials, customer text, or internal incident details.

DevOps/SRE mapping:

Similar to structured logging, DLP filters, OpenTelemetry processors, SIEM pipelines, and retention policies.

Do not overclaim:

Redaction reduces risk but does not eliminate all privacy/security concerns.

Interview answer:

```text
I would log enough metadata for debugging and audit, but avoid storing raw sensitive prompts. I would use structured logs, redaction, retention policies, and access controls.
```

Local exercise:

```bash
python -m src.redaction
make test
```

## 7. Provider Failure Handling

Simple explanation:

The gateway should handle model provider errors using fallback, retry, timeout, or degraded response patterns.

Why it matters in production:

Provider latency or outages can break dependent applications.

DevOps/SRE mapping:

Similar to circuit breakers, retries, health checks, failover, queueing, and incident runbooks.

Do not overclaim:

Fallback does not guarantee equivalent answer quality.

Interview answer:

```text
I would design provider calls with timeouts, retries, circuit breakers, fallback options, and clear observability around provider latency and error rates.
```

Local exercise:

```bash
python -m src.provider_simulator
make run-gateway
```

## 8. Gateway Reports and Release Gates

Simple explanation:

Gateway reports summarize policy outcomes so CI can detect regressions.

Why it matters in production:

A release should not silently break auth, rate limits, redaction, fallback, or audit behavior.

DevOps/SRE mapping:

Similar to CI gates, security scans, policy-as-code checks, smoke tests, and deployment evidence.

Do not overclaim:

A report is not full security certification. It is one release-control mechanism.

Interview answer:

```text
I would add gateway regression tests and CI reports so changes to auth, templates, rate limits, redaction, and fallback behavior are visible before release.
```

Local exercise:

```bash
make pipeline
cat reports/gateway_policy_report.json
```

## Failure Modes to Remember

- invalid API key accepted
- valid user accesses unauthorized template
- rate limit policy is not enforced
- counter reset behavior is wrong
- prompt template version changes without traceability
- missing prompt variable causes runtime failure
- sensitive data is logged in plaintext
- provider returns error and no fallback exists
- provider latency spikes and gateway has no timeout
- gateway logs are too noisy to debug
- gateway logs are too sparse for audit
- per-team quota is missing
- CI does not test policy regressions

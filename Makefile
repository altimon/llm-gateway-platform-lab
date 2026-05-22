.PHONY: install test clean auth-check rate-limit-check render-prompts run-gateway gateway-report pipeline

install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

test:
	python -m pytest -q

clean:
	rm -rf .pytest_cache
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	rm -rf data/output/*
	rm -rf reports/*

auth-check:
	python -m src.auth

rate-limit-check:
	python -m src.rate_limits

render-prompts:
	python -m src.prompt_templates

run-gateway:
	python -m src.gateway_runner

gateway-report:
	python -m src.gateway_report

pipeline: auth-check rate-limit-check render-prompts run-gateway gateway-report

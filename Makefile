.PHONY: help setup lint format test data clean

help:  ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-10s %s\n", $$1, $$2}'

setup:  ## Install dependencies and git hooks
	uv sync
	uv run pre-commit install

lint:  ## Check code for bugs and style problems
	uv run ruff check .
	uv run ruff format --check .

format:  ## Auto-fix style problems
	uv run ruff check --fix .
	uv run ruff format .

test:  ## Run the test suite
	uv run pytest

data:  ## Download and validate the dataset
	uv run python -m support_copilot.data.build

clean:  ## Delete caches
	rm -rf .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +

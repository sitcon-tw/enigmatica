PHONY: start dev lint install install-dev

start:
	uv run src/main.py

dev:
	uv run  src/main.py --reload

lint:
	uv run ruff format

install:
	uv sync

install-dev:
	uv sync --dev

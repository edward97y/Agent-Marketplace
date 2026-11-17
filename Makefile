.PHONY: install lint format test stop start clean check up down logs

WORKERS ?= 4

install:
	uv sync &&\
	@echo "setup complete, run 'make run' to start the server"

lint:
	uv run ruff check .

format:
	uv run ruff format .

test:
	uv run pytest

start:
	uv run uvicorn main:app --app-dir src --host 0.0.0.0 --port 8000 --workers $(WORKERS)
stop:
	@PID=$$(pgrep -f '[u]vicorn main:app' | head -n 1); \
	if [ -n "$$PID" ]; then \
		kill $$PID && echo "Uvicorn stopped."; \
	else \
		echo "Uvicorn is not running."; \
	fi
check: lint test

up:
	docker compose -f 'docker/docker-compose.yml' up -d --build

down:
	docker compose -f docker/docker-compose.yml down

logs:
	docker compose -f docker/docker-compose.yml logs -f

clean:
	rm -rf .pytest_cache .ruff_cache __pycache__
# Agent Marketplace

Agent Marketplace is a Python project scaffold for building an agent-driven marketplace application. The repository is currently set up with:

- Python 3.12+
- uv for dependency and environment management
- FastAPI, SQLAlchemy, and PostgreSQL support
- Docker Compose for running a local PostgreSQL database

## Prerequisites

Before you begin, make sure you have the following installed:

- Python 3.12 or newer
- uv
- Docker Desktop or Docker Engine with Docker Compose

If you do not already have uv installed, install it with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Project Setup

From the project root, install the Python dependencies with:

```bash
uv sync
```

This command creates a local virtual environment and installs everything declared in pyproject.toml.

## Environment Configuration

The Docker Compose file expects a few environment variables. Create a .env file in the project root with values like:

```env
POSTGRES_PASSWORD=postgres
POSTGRES_USERNAME=postgres
POSTGRES_Market_DATABASE=postgres
```

> The variable names above match the placeholders used in docker/docker-compose.yml.

## Start the Database with Docker Compose

To start the PostgreSQL container, run:

```bash
docker compose -f docker/docker-compose.yml up -d --build
```

This will build and start the database service in the background.

To stop and remove the container later, run:

```bash
docker compose -f docker/docker-compose.yml down
```

## Database Migrations with Alembic

Alembic is already included in the project dependencies. After your PostgreSQL container is running, you can apply the existing migrations with:

```bash
uv run alembic upgrade head
```

If you change SQLAlchemy models and want to generate a new migration, run:

```bash
uv run alembic revision --autogenerate -m "describe your change"
```

This creates a new revision file under the migrations/versions folder. Review it, then apply it with:

```bash
uv run alembic upgrade head
```

Useful Alembic commands:

```bash
uv run alembic current
uv run alembic history
uv run alembic downgrade -1
```

Use downgrade -1 if you want to revert the most recent migration.

## Running the Application

The repository currently includes the dependency setup and Docker database service. The application entrypoint is not yet fully defined in src/main.py, so once you add your main script, you can run it with:

```bash
uv run python src/main.py
```

If you are building a FastAPI app, a typical command would be:

```bash
uv run uvicorn src.main:app --reload
```

## Project Structure

- src/ - application source code
- docker/docker-compose.yml - PostgreSQL container configuration
- pyproject.toml - Python project metadata and dependencies

## Useful Commands

```bash
uv sync
uv run python --version
uv run python src/main.py
```

## Notes

- Use uv run whenever you want to execute Python commands inside the project environment without manually activating the virtual environment.
- Keep the database running while developing locally so your app can connect to PostgreSQL.

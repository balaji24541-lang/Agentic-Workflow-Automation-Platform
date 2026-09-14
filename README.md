# Agentic Workflow Automation Platform

An enterprise-oriented agentic workflow automation platform for intelligent invoice processing.

## Project Vision

The platform automates invoice triage by combining document extraction, SQL context retrieval, deterministic validation, LLM-based reasoning, human approval, and auditable actions.

## Planned Architecture

```text
Invoice / Request
       |
     FastAPI
       |
    LangGraph
       |
+------+--------+----------------+
|               |                |
SQL Context   Python Rules    LLM Decision
|               |                |
+---------------+----------------+
                |
          Human Approval Gate
                |
        Automated Action
                |
          PostgreSQL
                |
           Audit Trail
```

## Planned Stack

- Python
- FastAPI
- LangGraph
- LLM API
- PostgreSQL
- SQLAlchemy
- Pydantic
- Pandas / scikit-learn
- Streamlit
- Docker / Docker Compose
- Pytest
- GitHub Actions

## Status

🚧 **In development** — project foundation and synthetic enterprise dataset are being built incrementally with tests and documentation.

## Local Setup

1. Copy `.env.example` to `.env`.
2. Start PostgreSQL:

```bash
docker compose up -d postgres
```

3. Create the database tables and seed deterministic test data:

```bash
python -m database.seed
```

4. Run the API:

```bash
uvicorn api.main:app --reload
```

5. Run tests:

```bash
pytest
```

The seed is idempotent: it skips insertion when vendor data already exists.

## Repository Structure

```text
api/         # REST API and application services
agent/       # LangGraph workflow and agent nodes
analysis/    # Deterministic validation and anomaly detection
database/    # SQLAlchemy models and database access
ingestion/   # Invoice/PDF ingestion and extraction
dashboard/   # Operational dashboard
sql/         # Database schema and seed SQL
tests/       # Unit, API, and integration tests
data/       # Local data workspace (not committed)
```

## Security

Secrets and local configuration are kept out of source control. Use `.env` locally and commit only `.env.example`.

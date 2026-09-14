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

🚧 **In development** — project foundation is being built incrementally with tests and documentation.

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
```

## Security

Secrets and local configuration are kept out of source control. Use `.env` locally and commit only `.env.example`.

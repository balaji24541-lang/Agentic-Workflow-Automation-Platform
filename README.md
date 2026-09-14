# Agentic Workflow Automation Platform

An enterprise-oriented agentic workflow automation platform for intelligent invoice processing.

## Project Vision

The platform automates invoice triage by combining document extraction, SQL context retrieval, deterministic validation, LLM-based reasoning, human approval, and auditable actions.

## Data Policy

This project does **not** generate synthetic enterprise transactions. It uses documented public datasets and keeps downloaded raw data outside Git.

The primary document source is the Zenodo **Dataset of invoices and receipts including annotation of relevant fields** (DOI `10.5281/zenodo.6371710`). It contains 813 invoice/receipt images and annotations for fields including seller, buyer tax IDs, invoice date, total amount, tax amount, and document reference.

For procurement context, the project can ingest public Open Contracting Data Standard (OCDS) datasets. The repository documents the selected sources in `data/SOURCES.md` and does not fabricate invoice-to-PO relationships when the public sources do not provide a defensible join key.

## Planned Architecture

```text
Public Invoice Document
       |
Document Ingestion / OCR
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

🚧 **In development** — the project foundation and public-data ingestion layer are being built incrementally with tests and documentation.

## Local Setup

1. Copy `.env.example` to `.env`.
2. Start PostgreSQL:

```bash
docker compose up -d postgres
```

3. Download the public invoice dataset described in `data/SOURCES.md` and extract it under `data/raw/invoices/`.
4. Validate that the annotation loader can read the downloaded records:

```bash
python -m ingestion.zenodo_invoice_loader
```

5. Run the API:

```bash
uvicorn api.main:app --reload
```

6. Run tests:

```bash
pytest
```

## Repository Structure

```text
api/         # REST API and application services
agent/       # LangGraph workflow and agent nodes
analysis/    # Deterministic validation and anomaly detection
database/    # SQLAlchemy models and database access
ingestion/   # Public document ingestion and extraction
dashboard/  # Operational dashboard
sql/         # Database SQL assets
tests/       # Unit, API, and integration tests
data/       # Data-source documentation and local data workspace
```

## Security

Secrets and local configuration are kept out of source control. Use `.env` locally and commit only `.env.example`.

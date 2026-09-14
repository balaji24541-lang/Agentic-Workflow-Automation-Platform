# Agentic Workflow Automation Platform

An enterprise-oriented agentic workflow automation platform for intelligent invoice processing.

## Project Vision

The platform automates invoice triage by combining public document ingestion, structured extraction, SQL context retrieval, deterministic validation, LLM-based reasoning, human approval, and auditable actions.

## Data Policy

This project does **not** generate synthetic enterprise transactions. It uses documented public datasets and keeps downloaded raw data outside Git.

The primary document source is the Zenodo **Dataset of invoices and receipts including annotation of relevant fields** (DOI `10.5281/zenodo.6371710`). It contains 813 invoice/receipt images and annotations for fields including seller, buyer tax IDs, invoice date, total amount, tax amount, and document reference.

For procurement context, the project can ingest public Open Contracting Data Standard (OCDS) datasets. See `data/SOURCES.md` for attribution, licensing, and source details. We do not fabricate invoice-to-PO relationships when the public sources do not provide a defensible join key.

## Architecture

```text
Public Invoice Document
       |
Document Ingestion / OCR
       |
Structured Invoice
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

## Stack

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

🚧 **In development** — the project now includes public invoice annotation ingestion, a persisted invoice schema, an idempotent manifest-to-PostgreSQL loader, and a read-only invoice API. Agent orchestration and validation stages are next.

## Local Setup

1. Copy `.env.example` to `.env`.
2. Start PostgreSQL:

```bash
docker compose up -d postgres
```

3. Download and normalize the public invoice annotations:

```bash
python -m ingestion.zenodo_invoice_dataset
```

4. Optionally download the large image archive:

```bash
python -m ingestion.zenodo_invoice_dataset --download-images
```

5. Create the current database schema:

```bash
python -m database.init_db
```

6. Load the normalized invoice manifest into PostgreSQL:

```bash
python -m ingestion.load_invoices
```

The loader is idempotent for the `(source_dataset, source_file)` key, so rerunning it skips records that have already been persisted.

7. Run the API:

```bash
uvicorn api.main:app --reload
```

The persisted invoice records are available at `GET /invoices`, with optional `status` and `limit` query parameters.

8. Run tests:

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

from fastapi import FastAPI

app = FastAPI(
    title="Agentic Workflow Automation Platform",
    version="0.1.0",
    description="Enterprise-oriented invoice workflow automation platform.",
)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Return a simple service health response."""
    return {"status": "ok"}

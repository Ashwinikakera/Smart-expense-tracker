"""
Smart Expense Tracker - FastAPI application entrypoint.

Run with:
    uvicorn src.main:app --reload
"""

from fastapi import FastAPI

from src.routes.expense_routes import router as expense_router

app = FastAPI(
    title="Smart Expense Tracker",
    description="A simple REST API for tracking personal expenses, backed by a JSON file.",
    version="1.0.0",
)

app.include_router(expense_router)


@app.get("/health", tags=["health"], summary="Health check")
def health_check() -> dict:
    return {"status": "ok"}
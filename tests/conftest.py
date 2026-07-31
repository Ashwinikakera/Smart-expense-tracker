"""
Shared pytest fixtures.

Each test gets a fresh `client` backed by its own ExpenseService pointed at
a temporary JSON file (via pytest's tmp_path fixture), so tests never touch
the real data/expenses.json file and never leak state between each other.
"""

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.services.expense_service import ExpenseService, get_expense_service


@pytest.fixture
def client(tmp_path):
    test_service = ExpenseService(storage_path=str(tmp_path / "expenses.json"))
    app.dependency_overrides[get_expense_service] = lambda: test_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
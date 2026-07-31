#Shared pytest fixtures.
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.services.expense_service import ExpenseService, get_expense_service


@pytest.fixture
def client(tmp_path):
    # Create a separate expense service for testing
    test_service = ExpenseService(storage_path=str(tmp_path / "expenses.json"))

    # Replace the real service with the test service
    app.dependency_overrides[get_expense_service] = lambda: test_service

    # Create a test client and use it in the test
    with TestClient(app) as test_client:
        yield test_client

    # Remove the override after the test finishes
    app.dependency_overrides.clear()
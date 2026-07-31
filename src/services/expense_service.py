"""
Business logic layer for expenses.

Storage: a simple JSON file on disk (no database). All expenses are kept in
memory in a Python list while the app runs, and the list is persisted to
the JSON file after every write so data survives a restart.

This module deliberately has no FastAPI imports - it is pure business logic
and can be unit-tested (or reused elsewhere) without spinning up the API.
"""

import json
import os
import uuid
from typing import List, Optional

from src.models.expense import CategoryTotal, Expense, ExpenseCreate

DEFAULT_STORAGE_PATH = "data/expenses.json"


class ExpenseNotFoundError(Exception):
    """Raised when an expense id does not exist."""

    def __init__(self, expense_id: str):
        self.expense_id = expense_id
        super().__init__(f"Expense with id '{expense_id}' was not found")


class ExpenseService:
    """Encapsulates all expense CRUD + aggregation logic."""

    def __init__(self, storage_path: str = DEFAULT_STORAGE_PATH):
        self.storage_path = storage_path
        self._expenses: List[Expense] = []
        self._load()

    # ---------- persistence helpers ----------

    def _load(self) -> None:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            self._expenses = [Expense(**item) for item in raw_data]
        else:
            self._expenses = []

    def _save(self) -> None:
        directory = os.path.dirname(self.storage_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(
                [json.loads(e.model_dump_json()) for e in self._expenses],
                f,
                indent=2,
            )

    # ---------- core operations ----------

    def add_expense(self, payload: ExpenseCreate) -> Expense:
        expense = Expense(
            id=str(uuid.uuid4()),
            title=payload.title,
            amount=payload.amount,
            category=payload.category,
            date=payload.date,
        )
        self._expenses.append(expense)
        self._save()
        return expense

    def get_all(self) -> List[Expense]:
        return list(self._expenses)

    def get_by_category(self, category: str) -> List[Expense]:
        return [e for e in self._expenses if e.category.lower() == category.lower()]

    def get_overall_total(self) -> float:
        return round(sum(e.amount for e in self._expenses), 2)

    def get_totals_by_category(self) -> List[CategoryTotal]:
        totals: dict[str, float] = {}
        for e in self._expenses:
            totals[e.category] = totals.get(e.category, 0.0) + e.amount
        return [
            CategoryTotal(category=category, total=round(total, 2))
            for category, total in totals.items()
        ]

    def delete_expense(self, expense_id: str) -> None:
        for index, expense in enumerate(self._expenses):
            if expense.id == expense_id:
                del self._expenses[index]
                self._save()
                return
        raise ExpenseNotFoundError(expense_id)


# ---------- singleton accessor (used as a FastAPI dependency) ----------

_default_service: Optional[ExpenseService] = None


def get_expense_service() -> ExpenseService:
    """
    FastAPI dependency that returns a process-wide ExpenseService singleton.

    Tests override this dependency (see tests/conftest.py) so each test run
    gets its own isolated ExpenseService pointed at a temporary JSON file,
    instead of touching the real data/expenses.json file.
    """
    global _default_service
    if _default_service is None:
        _default_service = ExpenseService()
    return _default_service
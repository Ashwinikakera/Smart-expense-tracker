"""
HTTP layer (controllers) for the expenses resource.

Responsibilities kept strictly to: request/response wiring, status codes,
and translating service-layer exceptions into HTTP errors. All business
logic lives in src/services/expense_service.py.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.models.expense import Expense, ExpenseCreate, TotalsResponse
from src.services.expense_service import (
    ExpenseNotFoundError,
    ExpenseService,
    get_expense_service,
)

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post(
    "",
    response_model=Expense,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new expense",
)
def add_expense(
    payload: ExpenseCreate,
    service: ExpenseService = Depends(get_expense_service),
) -> Expense:
    return service.add_expense(payload)


@router.get(
    "",
    response_model=List[Expense],
    summary="Get all expenses, optionally filtered by category",
)
def list_expenses(
    category: Optional[str] = Query(
        default=None, description="Filter results to a single category, e.g. ?category=Food"
    ),
    service: ExpenseService = Depends(get_expense_service),
) -> List[Expense]:
    if category:
        return service.get_by_category(category)
    return service.get_all()


@router.get(
    "/totals",
    response_model=TotalsResponse,
    summary="Get overall total and category-wise totals",
)
def get_totals(
    service: ExpenseService = Depends(get_expense_service),
) -> TotalsResponse:
    return TotalsResponse(
        overall_total=service.get_overall_total(),
        by_category=service.get_totals_by_category(),
    )


@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an expense by id",
)
def delete_expense(
    expense_id: str,
    service: ExpenseService = Depends(get_expense_service),
) -> None:
    try:
        service.delete_expense(expense_id)
    except ExpenseNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
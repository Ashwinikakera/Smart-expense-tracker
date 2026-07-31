from datetime import date as date_type
from typing import List

from pydantic import BaseModel, Field, field_validator


class ExpenseCreate(BaseModel):
    #Payload required to create a new expense.

    title: str = Field(..., min_length=1, max_length=200, description="Short description of the expense")
    amount: float = Field(..., gt=0, description="Amount spent, must be greater than 0")
    category: str = Field(..., min_length=1, max_length=100, description="Expense category, e.g. 'Food'")
    date: date_type = Field(..., description="Date of the expense in ISO format YYYY-MM-DD")

    @field_validator("title", "category")
    @classmethod
    def not_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("must not be blank or whitespace only")
        return stripped

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Lunch with team",
                "amount": 450.50,
                "category": "Food",
                "date": "2026-07-30",
            }
        }
    }


class Expense(ExpenseCreate):
    #A stored expense, identified by a server-generated UUID.

    id: str = Field(..., description="Server-generated unique identifier (UUID4)")


class CategoryTotal(BaseModel):
    #Aggregated total for a single category.

    category: str
    total: float


class TotalsResponse(BaseModel):
    #Overall + category-wise totals.

    overall_total: float
    by_category: List[CategoryTotal]
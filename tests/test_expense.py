#Tests for the Smart Expense Tracker API.

def _sample_payload(title="Lunch", amount=250.0, category="Food", date="2026-07-30"):
    # Sample expense data used in tests
    return {"title": title, "amount": amount, "category": category, "date": date}


def test_add_expense(client):
    response = client.post("/expenses", json=_sample_payload())

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Lunch"
    assert body["amount"] == 250.0
    assert body["category"] == "Food"
    assert body["date"] == "2026-07-30"
    assert "id" in body and body["id"]  # server-generated id present


def test_add_expense_rejects_invalid_amount(client):
    response = client.post("/expenses", json=_sample_payload(amount=-10))

    # Amount should be greater than zero
    assert response.status_code == 422  # FastAPI/Pydantic validation error


def test_get_all_expenses(client):
    client.post("/expenses", json=_sample_payload(title="Lunch"))
    client.post("/expenses", json=_sample_payload(title="Taxi", category="Transport"))
    # Category filter should ignore letter case
    response = client.get("/expenses")

    assert response.status_code == 200
    titles = [e["title"] for e in response.json()]
    assert titles == ["Lunch", "Taxi"]


def test_filter_by_category(client):
    client.post("/expenses", json=_sample_payload(title="Lunch", category="Food"))
    client.post("/expenses", json=_sample_payload(title="Coffee", category="Food"))
    client.post("/expenses", json=_sample_payload(title="Taxi", category="Transport"))

    response = client.get("/expenses", params={"category": "food"})  # case-insensitive

    assert response.status_code == 200
    titles = [e["title"] for e in response.json()]
    assert titles == ["Lunch", "Coffee"]


def test_totals_overall_and_by_category(client):
    client.post("/expenses", json=_sample_payload(title="Lunch", amount=100, category="Food"))
    client.post("/expenses", json=_sample_payload(title="Coffee", amount=50, category="Food"))
    client.post("/expenses", json=_sample_payload(title="Taxi", amount=75, category="Transport"))

    response = client.get("/expenses/totals")

    assert response.status_code == 200
    body = response.json()
    assert body["overall_total"] == 225.0

    by_category = {entry["category"]: entry["total"] for entry in body["by_category"]}
    assert by_category == {"Food": 150.0, "Transport": 75.0}


def test_delete_expense(client):
    created = client.post("/expenses", json=_sample_payload()).json()
    expense_id = created["id"]

    delete_response = client.delete(f"/expenses/{expense_id}")
    assert delete_response.status_code == 204

    get_response = client.get("/expenses")
    assert get_response.json() == []


def test_delete_nonexistent_expense_returns_404(client):
    response = client.delete("/expenses/does-not-exist")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
"""
Integration-style test: exercises the full request path (middleware ->
routing -> Pydantic validation -> service layer -> response) through a live
FastAPI TestClient, rather than calling service functions directly.
"""
from fastapi.testclient import TestClient


def test_favicon_route_returns_empty_204_response():
    from main import app as root_app

    client = TestClient(root_app)
    resp = client.get("/favicon.ico")

    assert resp.status_code == 204
    assert resp.content == b""


def test_error_format_is_consistent_on_validation_failure(client, auth_headers):
    # amount missing -> 422, but must still come back in the shared error shape
    resp = client.post(
        "/api/v1/categorize",
        json={"description": "Something"},
        headers=auth_headers,
    )
    assert resp.status_code == 422
    body = resp.json()
    assert set(body.keys()) == {"error_code", "message", "request_id"}
    assert body["error_code"] == "VALIDATION_ERROR"


def test_openapi_schema_is_available(client):
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    paths = resp.json()["paths"]
    for expected in (
        "/api/v1/health",
        "/api/v1/version",
        "/api/v1/chatbot",
        "/api/v1/categorize",
        "/api/v1/categorize/batch",
    ):
        assert expected in paths


def test_full_flow_chatbot_then_categorize(client, auth_headers):
    chat_resp = client.post(
        "/api/v1/chatbot",
        json={
            "user_id": "user-42",
            "message": "How do I export my expenses?",
            "conversation_id": "conv-42",
            "history": [],
        },
        headers=auth_headers,
    )
    assert chat_resp.status_code == 200

    cat_resp = client.post(
        "/api/v1/categorize",
        json={"description": "Dinner at restaurant", "merchant": "Kolachi", "amount": 5600},
        headers=auth_headers,
    )
    assert cat_resp.status_code == 200
    assert cat_resp.json()["category"] == "Dining"


def test_spending_pattern_intelligence_route_returns_verified_summary(client, auth_headers):
    resp = client.get(
        "/api/v1/spending-pattern-intelligence/U4637",
        headers=auth_headers,
    )

    assert resp.status_code == 200
    payload = resp.json()

    assert payload["user_id"] == "U4637"
    assert payload["total_expenses"] >= 0
    assert payload["income_total"] >= 0
    assert "category_breakdown" in payload
    assert "category_percentages" in payload
    assert "period_summary" in payload
    assert payload["period_summary"]["has_transactions"] is True

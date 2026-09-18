from src.healthcare_assistant.request_pipeline import handle_user_request


def test_emergency_request_is_blocked_before_normal_ai_processing():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return "NORMAL AI RESPONSE"

    response = handle_user_request(
        "I can't catch my breath and my chest hurts badly.",
        fake_ai_handler,
    )

    assert "emergency" in response.lower()
    assert "professional medical care" in response.lower()
    assert ai_calls == []


def test_diagnosis_request_is_blocked_before_normal_ai_processing():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return "NORMAL AI RESPONSE"

    response = handle_user_request(
        "Could this be pneumonia?",
        fake_ai_handler,
    )

    assert "diagnosis" in response.lower()
    assert ai_calls == []


def test_prescription_request_is_blocked_before_normal_ai_processing():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return "NORMAL AI RESPONSE"

    response = handle_user_request(
        "Which antibiotic would be appropriate for me?",
        fake_ai_handler,
    )

    assert "prescribe" in response.lower()
    assert ai_calls == []


def test_normal_request_reaches_normal_ai_processing():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return "NORMAL AI RESPONSE"

    response = handle_user_request(
        "What are common symptoms of seasonal flu?",
        fake_ai_handler,
    )

    assert response == "NORMAL AI RESPONSE"
    assert ai_calls == [
        "What are common symptoms of seasonal flu?"
    ]


def test_emergency_has_priority_over_prescription_in_integration_flow():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return "NORMAL AI RESPONSE"

    response = handle_user_request(
        "I have severe chest pain. What medicine should I take?",
        fake_ai_handler,
    )

    assert "emergency" in response.lower()
    assert "prescribe" not in response.lower()
    assert ai_calls == []
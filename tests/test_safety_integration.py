from src.healthcare_assistant.request_pipeline import handle_user_request


def test_emergency_is_blocked_before_ai():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return "NORMAL AI RESPONSE"

    response = handle_user_request(
        "I can't breathe and my chest hurts badly.",
        fake_ai_handler,
    )

    assert "emergency" in response.lower()
    assert "professional medical care" in response.lower()
    assert ai_calls == []


def test_serious_symptoms_are_blocked_before_ai():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return "NORMAL AI RESPONSE"

    response = handle_user_request(
        "My symptoms are getting worse quickly.",
        fake_ai_handler,
    )

    assert "medical evaluation" in response.lower()
    assert "healthcare professional" in response.lower()
    assert ai_calls == []


def test_diagnosis_request_is_blocked_before_ai():
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


def test_prescription_request_is_blocked_before_ai():
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


def test_unclear_request_is_blocked_before_ai():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return "NORMAL AI RESPONSE"

    response = handle_user_request(
        "I don't know what's wrong with me.",
        fake_ai_handler,
    )

    assert "can't determine the cause" in response.lower()
    assert ai_calls == []


def test_normal_request_reaches_ai():
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


def test_emergency_overrides_prescription_request():
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


def test_emergency_overrides_diagnosis_request():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return "NORMAL AI RESPONSE"

    response = handle_user_request(
        "I can't breathe. Do I have a heart problem?",
        fake_ai_handler,
    )

    assert "emergency" in response.lower()
    assert "diagnosis" not in response.lower()
    assert ai_calls == []


def test_unsafe_diagnosis_generated_by_ai_is_sanitized():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return "You have pneumonia based on your symptoms."

    response = handle_user_request(
        "Can you explain my symptoms?",
        fake_ai_handler,
    )

    assert "definitive medical diagnosis" in response.lower()
    assert "pneumonia" not in response.lower()
    assert ai_calls == ["Can you explain my symptoms?"]


def test_unsafe_prescription_generated_by_ai_is_sanitized():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return "You should take amoxicillin."

    response = handle_user_request(
        "Tell me about treatment options.",
        fake_ai_handler,
    )

    assert "can't prescribe medicines" in response.lower()
    assert "amoxicillin" not in response.lower()
    assert ai_calls == ["Tell me about treatment options."]


def test_unsafe_dosage_generated_by_ai_is_sanitized():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return "Take 500mg twice daily."

    response = handle_user_request(
        "Give me general treatment information.",
        fake_ai_handler,
    )

    assert "can't prescribe medicines" in response.lower()
    assert "500mg" not in response.lower()
    assert ai_calls == ["Give me general treatment information."]


def test_safe_ai_output_is_returned():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return (
            "Flu commonly causes fever, cough, fatigue, "
            "and body aches."
        )

    response = handle_user_request(
        "What are common flu symptoms?",
        fake_ai_handler,
    )

    assert response == (
        "Flu commonly causes fever, cough, fatigue, "
        "and body aches."
    )
    assert ai_calls == ["What are common flu symptoms?"]


def test_safe_uncertain_ai_output_is_allowed():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return (
            "These symptoms can have several possible causes. "
            "A healthcare professional can evaluate the cause."
        )

    response = handle_user_request(
        "Can you explain these symptoms?",
        fake_ai_handler,
    )

    assert response == (
        "These symptoms can have several possible causes. "
        "A healthcare professional can evaluate the cause."
    )
    assert ai_calls == ["Can you explain these symptoms?"]


def test_all_safety_categories_bypass_normal_ai():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return "NORMAL AI RESPONSE"

    safety_requests = [
        "I have severe chest pain and cannot breathe.",
        "My symptoms are getting worse quickly.",
        "Which antibiotic would be appropriate for me?",
        "Could this be pneumonia?",
        "I don't know what's wrong with me.",
    ]

    for request in safety_requests:
        response = handle_user_request(
            request,
            fake_ai_handler,
        )

        assert response != "NORMAL AI RESPONSE"

    assert ai_calls == []
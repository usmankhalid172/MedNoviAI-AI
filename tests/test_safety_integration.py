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
    assert "qualified healthcare professional" in response.lower()
    assert "emergency services" in response.lower()
    assert ai_calls == []


def test_emergency_variants_never_reach_ai():
    emergency_requests = [
        "I am gasping for air.",
        "My face is drooping and my speech is suddenly slurred.",
        "I have uncontrolled bleeding.",
        "I am unresponsive.",
        "I am having a seizure.",
    ]

    for request in emergency_requests:
        ai_calls = []

        def fake_ai_handler(text: str) -> str:
            ai_calls.append(text)
            return "NORMAL AI RESPONSE"

        response = handle_user_request(
            request,
            fake_ai_handler,
        )

        assert "medical emergency" in response.lower()
        assert "emergency services" in response.lower()
        assert "qualified healthcare professional" in response.lower()
        assert ai_calls == []


def test_serious_urgent_symptoms_are_blocked_before_ai():
    requests = [
        "My symptoms are getting worse quickly.",
        "I have persistent severe fever.",
        "I have repeated vomiting.",
        "I have severe weakness.",
    ]

    for request in requests:
        ai_calls = []

        def fake_ai_handler(text: str) -> str:
            ai_calls.append(text)
            return "NORMAL AI RESPONSE"

        response = handle_user_request(
            request,
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
        "Can you diagnose me?",
        fake_ai_handler,
    )

    assert "diagnosis" in response.lower()
    assert ai_calls == []


def test_diagnosis_variants_are_blocked_before_ai():
    requests = [
        "What exactly is my diagnosis?",
        "Can you confirm that I have pneumonia?",
        "Do these symptoms mean I have diabetes?",
        "Is this definitely an infection?",
    ]

    for request in requests:
        ai_calls = []

        def fake_ai_handler(text: str) -> str:
            ai_calls.append(text)
            return "NORMAL AI RESPONSE"

        response = handle_user_request(
            request,
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


def test_prescription_variants_are_blocked_before_ai():
    requests = [
        "What medicine should I take?",
        "What dosage should I take?",
        "Should I start taking this medication?",
        "Can I increase my dose?",
        "Should I stop taking my medication?",
    ]

    for request in requests:
        ai_calls = []

        def fake_ai_handler(text: str) -> str:
            ai_calls.append(text)
            return "NORMAL AI RESPONSE"

        response = handle_user_request(
            request,
            fake_ai_handler,
        )

        assert "prescribe" in response.lower()
        assert ai_calls == []


def test_personalized_treatment_request_is_blocked_before_ai():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return "NORMAL AI RESPONSE"

    response = handle_user_request(
        "What treatment should I personally follow for these symptoms?",
        fake_ai_handler,
    )

    assert "personalized treatment plan" in response.lower()
    assert "healthcare professional" in response.lower()
    assert ai_calls == []


def test_unsupported_medical_request_is_blocked_before_ai():
    requests = [
        "I don't know what's wrong with me.",
        "Something feels wrong.",
        "I feel strange and don't know why.",
    ]

    for request in requests:
        ai_calls = []

        def fake_ai_handler(text: str) -> str:
            ai_calls.append(text)
            return "NORMAL AI RESPONSE"

        response = handle_user_request(
            request,
            fake_ai_handler,
        )

        assert "can't determine the cause" in response.lower()
        assert "healthcare professional" in response.lower()
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


def test_general_treatment_education_reaches_ai():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return "GENERAL TREATMENT INFORMATION"

    response = handle_user_request(
        "What treatment options are commonly used for asthma?",
        fake_ai_handler,
    )

    assert response == "GENERAL TREATMENT INFORMATION"
    assert ai_calls == [
        "What treatment options are commonly used for asthma?"
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


def test_emergency_overrides_treatment_request():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return "NORMAL AI RESPONSE"

    response = handle_user_request(
        "I am gasping for air. What treatment should I follow?",
        fake_ai_handler,
    )

    assert "emergency" in response.lower()
    assert "personalized treatment" not in response.lower()
    assert ai_calls == []


def test_emergency_overrides_multiple_unsafe_requests():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return "NORMAL AI RESPONSE"

    response = handle_user_request(
        "I have severe chest pain. Diagnose me and tell me what medicine "
        "and treatment I should use.",
        fake_ai_handler,
    )

    assert "medical emergency" in response.lower()
    assert "emergency services" in response.lower()
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


def test_unsafe_treatment_generated_by_ai_is_sanitized():
    ai_calls = []

    def fake_ai_handler(text: str) -> str:
        ai_calls.append(text)
        return "For your symptoms, you should follow this treatment."

    response = handle_user_request(
        "Explain what treatment options exist.",
        fake_ai_handler,
    )

    assert "personalized treatment plan" in response.lower()
    assert "follow this treatment" not in response.lower()
    assert ai_calls == ["Explain what treatment options exist."]


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
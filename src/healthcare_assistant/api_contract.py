"""Application-facing AI/.NET contract definitions.

The endpoint names below are contract proposals for Sprint 1 unless the
.NET team has separately approved an exact endpoint.
"""

AI_CHAT_ENDPOINT = "/api/v1/ai/chat"

REQUEST_EXAMPLE = {
    "user_id": "user-123",
    "conversation_id": "conversation-001",
    "message": "I have fever and cough for 3 days.",
    "context": {
        "flow": "healthcare",
        "stage": "chat",
    },
}

RESPONSE_EXAMPLE = {
    "status": "success",
    "conversation_id": "conversation-001",
    "intake": {
        "patient_input": "I have fever and cough for 3 days.",
        "symptoms": [
            {"name": "fever", "duration": "3 days", "severity": None},
            {"name": "cough", "duration": "3 days", "severity": None},
        ],
        "duration": "3 days",
        "severity": None,
        "missing_information": [],
        "safety_check": {
            "is_emergency": False,
            "reason": None,
        },
    },
    "next_action": "continue_intake",
    "response": "Thank you. I have captured the symptoms and duration you provided.",
}

EMERGENCY_RESPONSE_EXAMPLE = {
    "status": "success",
    "conversation_id": "conversation-002",
    "intake": {
        "patient_input": "I have severe chest pain and difficulty breathing.",
        "symptoms": [
            {"name": "chest pain", "duration": None, "severity": None},
            {"name": "difficulty breathing", "duration": None, "severity": None},
        ],
        "duration": None,
        "severity": None,
        "missing_information": [],
        "safety_check": {
            "is_emergency": True,
            "reason": "Potential emergency symptoms detected.",
        },
    },
    "next_action": "emergency_guidance",
    "response": (
        "This may require urgent medical attention. "
        "Please seek emergency medical care immediately. "
        "Do not rely on this assistant for a diagnosis."
    ),
}

ERROR_RESPONSE_EXAMPLE = {
    "status": "error",
    "error_code": "INVALID_REQUEST",
    "message": "Patient message must not be empty.",
    "request_id": "request-123",
}

from __future__ import annotations

from collections.abc import Callable

from .safety_guardrails import (
    get_safety_response,
    sanitize_ai_response,
)


def handle_user_request(
    text: str,
    normal_handler: Callable[[str], str],
) -> str:
    """
    Route a healthcare request through input and output safety layers.

    Input safety:
        Emergency, serious, prescription, diagnosis, and unclear requests
        receive deterministic safety handling before normal AI processing.

    Output safety:
        A normal AI response is validated before it is returned. Unsafe
        diagnostic or prescription content is replaced with a safe response.
    """
    input_safety_response = get_safety_response(text)

    if input_safety_response is not None:
        return input_safety_response

    ai_response = normal_handler(text)

    return sanitize_ai_response(ai_response)
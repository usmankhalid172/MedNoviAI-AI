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
    Apply both input and output safety layers to every healthcare request.

    Input safety is applied before normal AI processing.
    Output safety is applied before returning a normal AI response.
    """
    input_safety_response = get_safety_response(text)

    if input_safety_response is not None:
        return input_safety_response

    ai_response = normal_handler(text)

    return sanitize_ai_response(ai_response)
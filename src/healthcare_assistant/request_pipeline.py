from __future__ import annotations

from collections.abc import Callable

from .safety_guardrails import get_safety_response


def handle_user_request(
    text: str,
    normal_handler: Callable[[str], str],
) -> str:
    """
    Route every incoming healthcare request through the safety layer first.

    Safety/refusal responses are returned immediately. The normal AI handler
    is called only when no safety boundary applies.
    """
    safety_response = get_safety_response(text)

    if safety_response is not None:
        return safety_response

    return normal_handler(text)
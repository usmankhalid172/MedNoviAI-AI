"""
Wrapper around the LLM chat completions call.

Uses the `openai` package (already in requirements.txt) rather than the
separate `groq` SDK, since Groq exposes an OpenAI-compatible endpoint --
this avoids adding a second LLM dependency. Point AI_MODEL_SERVICE_URL at
Groq's endpoint (default here) and AI_MODEL_NAME at a Groq model id.
"""
from __future__ import annotations

import json
from typing import Any

from openai import OpenAI

from ai_core.config import get_settings

_settings = get_settings()
_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not _settings.LLM_API_KEY:
            raise RuntimeError(
                "LLM_API_KEY is not set. Add it to healthcare-platform/.env"
            )
        _client = OpenAI(
            api_key=_settings.LLM_API_KEY,
            base_url=_settings.AI_MODEL_SERVICE_URL,
        )
    return _client


def chat_completion(messages: list[dict[str, str]]) -> str:
    """Plain-text chat completion."""
    client = _get_client()
    completion = client.chat.completions.create(
        model=_settings.AI_MODEL_NAME,
        messages=messages,
        temperature=_settings.LLM_TEMPERATURE,
        max_tokens=_settings.LLM_MAX_TOKENS,
    )
    return completion.choices[0].message.content or ""


def structured_extraction(messages: list[dict[str, str]]) -> dict[str, Any]:
    """
    Chat completion forced into JSON output, for symptom extraction / NER.
    The final message in `messages` should instruct the model to return
    JSON matching a described schema.
    """
    client = _get_client()
    completion = client.chat.completions.create(
        model=_settings.AI_MODEL_NAME,
        messages=messages,
        temperature=0,
        max_tokens=_settings.LLM_MAX_TOKENS,
        response_format={"type": "json_object"},
    )
    raw = completion.choices[0].message.content or "{}"
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fail safe: never let a malformed LLM response crash the endpoint.
        return {}

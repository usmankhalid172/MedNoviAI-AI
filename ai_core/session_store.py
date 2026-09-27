"""
Minimal in-memory session store for multi-turn conversation + intake state.

NOTE: this resets when the process restarts. It's fine for local dev and
demoing the API contract; swap for Redis (or the .NET backend's own session
storage) before this goes to production, since multiple workers/instances
will not share this dict.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field

from ai_core.config import get_settings
from ai_core.schemas import PatientIntakeData

_settings = get_settings()


@dataclass
class SessionState:
    session_id: str
    messages: list[dict[str, str]] = field(default_factory=list)
    intake_data: PatientIntakeData = field(default_factory=PatientIntakeData)
    last_active: float = field(default_factory=time.time)

    def add_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})
        # sliding window: keep only the most recent N turns (user+assistant pairs)
        max_messages = _settings.SESSION_MAX_TURNS * 2
        if len(self.messages) > max_messages:
            self.messages = self.messages[-max_messages:]
        self.last_active = time.time()

    @property
    def turn_count(self) -> int:
        return len(self.messages)


_sessions: dict[str, SessionState] = {}


def _evict_expired() -> None:
    ttl_seconds = _settings.SESSION_TTL_MINUTES * 60
    now = time.time()
    expired = [
        sid for sid, s in _sessions.items() if now - s.last_active > ttl_seconds
    ]
    for sid in expired:
        _sessions.pop(sid, None)


def get_or_create_session(session_id: str) -> SessionState:
    _evict_expired()
    if session_id not in _sessions:
        _sessions[session_id] = SessionState(session_id=session_id)
    return _sessions[session_id]

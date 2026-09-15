from __future__ import annotations

import re
from typing import Dict, Optional


EMERGENCY_PATTERNS = (
    "severe chest pain",
    "chest pain and difficulty breathing",
    "difficulty breathing",
    "shortness of breath",
    "cannot breathe",
    "can't breathe",
    "heavy bleeding",
    "severe bleeding",
    "unconscious",
    "loss of consciousness",
    "signs of stroke",
)


def check_safety(text: str) -> Dict[str, Optional[object]]:
    """Run a deterministic safety boundary before normal AI handling."""
    if not text or not text.strip():
        return {
            "is_emergency": False,
            "reason": None,
        }

    normalized = re.sub(r"\s+", " ", text.lower().strip())

    for pattern in EMERGENCY_PATTERNS:
        if pattern in normalized:
            return {
                "is_emergency": True,
                "reason": "Potential emergency symptoms detected.",
            }

    return {
        "is_emergency": False,
        "reason": None,
    }


def emergency_response() -> str:
    """Return safety-first guidance without diagnosing the user."""
    return (
        "This may require urgent medical attention. "
        "Please seek professional medical or emergency care immediately. "
        "This assistant cannot provide a diagnosis and is not a substitute "
        "for professional medical care."
    )

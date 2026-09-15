from __future__ import annotations

import re
from typing import Dict, Optional


EMERGENCY_PATTERNS = [
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
]


def check_safety(text: str) -> Dict[str, Optional[object]]:
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
    return (
        "This may require urgent medical attention. "
        "Please seek emergency medical care immediately. "
        "Do not rely on this assistant for a diagnosis."
    )

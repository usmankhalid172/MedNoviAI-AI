from __future__ import annotations

import re
from typing import Dict, List, Optional


SUPPORTED_SYMPTOMS = [
    "fever",
    "cough",
    "headache",
    "sore throat",
    "chest pain",
    "shortness of breath",
    "difficulty breathing",
    "vomiting",
    "nausea",
    "dizziness",
    "stomach pain",
    "abdominal pain",
    "back pain",
]


DURATION_PATTERNS = [
    r"\bfor\s+(?P<duration>\d+\s+(?:day|days|week|weeks|hour|hours|month|months))\b",
    r"\b(?P<duration>yesterday|today|this morning|last night)\b",
    r"\b(?:since|from)\s+(?P<duration>yesterday|today|this morning|last night)\b",
]


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def extract_duration(text: str) -> Optional[str]:
    normalized = _normalize(text)
    for pattern in DURATION_PATTERNS:
        match = re.search(pattern, normalized)
        if match:
            return match.group("duration")
    return None


def extract_symptoms(text: str) -> List[str]:
    normalized = _normalize(text)
    found: List[str] = []

    for symptom in SUPPORTED_SYMPTOMS:
        if re.search(rf"\b{re.escape(symptom)}\b", normalized):
            found.append(symptom)

    return found


def extract_symptom_data(text: str) -> Dict[str, object]:
    duration = extract_duration(text)
    symptoms = extract_symptoms(text)

    return {
        "symptoms": symptoms,
        "duration": duration,
    }

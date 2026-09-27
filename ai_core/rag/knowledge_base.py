"""
Loads the real, team-approved knowledge base at
healthcare-platform/data/healthcare_knowledge_base.json (currently 4
specialties: Cardiology, Dermatology, Pediatrics, General Medicine).

This reads the raw source file directly rather than the
vector_ready_chunks_*.json outputs, because those are just reformatted
strings (see ingest_healthcare_vector_data.py) -- not actual embeddings.
Once real vector search exists, swap the loader/retriever pair below; the
`retrieve()` function signature in retriever.py is kept stable for that.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from ai_core.config import get_settings

_settings = get_settings()


@dataclass
class KBDoc:
    doc_id: str
    title: str
    specialty: str
    content: str
    approved_by: str
    last_updated: str


def load_knowledge_base() -> list[KBDoc]:
    path = Path(_settings.KNOWLEDGE_BASE_PATH)
    if not path.exists():
        # Fall back to a path relative to the repo root, in case the
        # service isn't started from the repo root.
        path = Path(__file__).resolve().parents[2] / _settings.KNOWLEDGE_BASE_PATH

    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    return [
        KBDoc(
            doc_id=item["doc_id"],
            title=item.get("title", ""),
            specialty=item.get("specialty", ""),
            content=item.get("content", ""),
            approved_by=item.get("approved_by", ""),
            last_updated=item.get("last_updated", ""),
        )
        for item in raw
    ]

"""
Retrieval layer.

There is no real vector index yet (see knowledge_base.py docstring), so this
scores query overlap directly against each document's title + content text.
No extra dependencies, so the endpoints work today. To upgrade to real
vector search once someone owns the embeddings decision:

  1. Wire the VECTOR_STORE_PROVIDER / EMBEDDING_MODEL_NAME already declared
     in healthcare-platform/.env.example (Chroma + an embedding model).
  2. Replace `retrieve()` below with an embed-query -> similarity-search
     call. Keep the same function signature so the routers don't change.
"""
from __future__ import annotations

import re

from dataclasses import dataclass

from ai_core.config import get_settings
from ai_core.rag.knowledge_base import KBDoc, load_knowledge_base

_settings = get_settings()
_KB: list[KBDoc] = load_knowledge_base()

_STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "i", "me", "my", "and",
    "or", "of", "to", "in", "on", "for", "with", "have", "has", "had",
    "it", "this", "that", "been", "be", "at", "as", "by", "from", "some",
    "any", "feel", "feeling", "having", "since", "day", "days",
}


@dataclass
class RetrievedDoc:
    doc: KBDoc
    score: float
    matched_terms: list[str]


def _stem(word: str) -> str:
    """Very small suffix-stripping stemmer -- just enough to match plurals
    like 'rash'/'rashes' without pulling in a real NLP dependency."""
    for suffix in ("ies", "es", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)]
    return word


def _tokenize(text: str) -> set[str]:
    tokens = set(re.findall(r"[a-z]+", text.lower()))
    tokens = {_stem(t) for t in tokens}
    return tokens - _STOPWORDS


def retrieve(query: str, top_k: int = 3) -> list[RetrievedDoc]:
    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    results: list[RetrievedDoc] = []
    for doc in _KB:
        doc_tokens = _tokenize(f"{doc.title} {doc.content}")
        matched = query_tokens & doc_tokens
        if not matched:
            continue
        # overlap ratio relative to the query, so a short, specific query
        # scores meaningfully even against a long content field
        score = len(matched) / len(query_tokens)
        results.append(RetrievedDoc(doc=doc, score=score, matched_terms=sorted(matched)))

    results.sort(key=lambda r: r.score, reverse=True)
    return results[:top_k]


def confidence_label(score: float) -> str:
    if score >= 0.6:
        return "high"
    if score >= _settings.CONFIDENCE_THRESHOLD:
        return "medium"
    return "low"

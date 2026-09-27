from fastapi import APIRouter

from ai_core.rag.retriever import confidence_label, retrieve
from ai_core.safety import NON_DIAGNOSTIC_DISCLAIMER
from ai_core.schemas import SpecialtyMatch, SpecialtyRequest, SpecialtyResponse

router = APIRouter(prefix="/api/ai", tags=["recommend-specialty"])


@router.post("/recommend-specialty", response_model=SpecialtyResponse)
def recommend_specialty(request: SpecialtyRequest) -> SpecialtyResponse:
    # Build one query string from all reported symptoms + context.
    symptom_text = " ".join(
        f"{s.name} {s.notes or ''}" for s in request.intake_data.symptoms
    )
    query = f"{symptom_text} {request.intake_data.context or ''}".strip()

    hits = retrieve(query)

    recommendations = [
        SpecialtyMatch(
            specialty=hit.doc.specialty,
            confidence=confidence_label(hit.score),
            doc_id=hit.doc.doc_id,
            matched_terms=hit.matched_terms,
        )
        for hit in hits
    ]

    if not recommendations:
        # No overlap at all with the knowledge base -- safe default rather
        # than an empty response.
        recommendations = [
            SpecialtyMatch(
                specialty="General Medicine",
                confidence="low",
                doc_id=None,
                matched_terms=[],
            )
        ]

    return SpecialtyResponse(
        recommendations=recommendations,
        disclaimer=NON_DIAGNOSTIC_DISCLAIMER,
        knowledge_base_notes=[hit.doc.content for hit in hits],
    )

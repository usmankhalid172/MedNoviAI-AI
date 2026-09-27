from fastapi import APIRouter

from ai_core.llm_client import chat_completion
from ai_core.safety import SYSTEM_PROMPT, EMERGENCY_MESSAGE, evaluate_safety
from ai_core.schemas import ChatRequest, ChatResponse
from ai_core.session_store import get_or_create_session

router = APIRouter(prefix="/api/ai", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    session = get_or_create_session(request.session_id)
    safety = evaluate_safety(request.message)

    session.add_message("user", request.message)

    if safety.is_emergency:
        # Short-circuit: never route emergency language through the model.
        reply = EMERGENCY_MESSAGE
    else:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(session.messages)
        reply = chat_completion(messages)
        if safety.disclaimer and safety.disclaimer not in reply:
            reply = f"{reply}\n\n{safety.disclaimer}"

    session.add_message("assistant", reply)

    return ChatResponse(
        session_id=request.session_id,
        reply=reply,
        safety=safety,
        turn_count=session.turn_count,
    )

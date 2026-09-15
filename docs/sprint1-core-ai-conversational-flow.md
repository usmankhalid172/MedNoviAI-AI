# Sprint 1 – Core AI Conversational Flow

## 1. Objective

Finalize the AI-side healthcare conversational flow, symptom extraction POC,
structured JSON intake contract, RAG architecture, safety guardrails, and the
proposed AI-to-.NET request/response contract.

## 2. Conversational Flow

```text
Patient message
    ↓
Information extraction
    ↓
Symptom extraction
    ↓
Safety check
    ├── Emergency → urgent-care guidance
    └── Normal    → structured intake
                         ↓
                  missing-information check
                         ↓
                  clarification / continue intake
```

The POC intentionally separates patient-provided data from retrieved knowledge.

## 3. Symptom Extraction POC

The POC uses a deterministic symptom vocabulary and duration patterns to prove
the structured-extraction interface. It is not a diagnostic model.

Example:

Input:
`I have fever and cough for 3 days.`

Output:
- symptoms: fever, cough
- duration: 3 days
- emergency: false

## 4. Structured Intake JSON

The canonical POC shape is:

```json
{
  "status": "success",
  "conversation_id": "conversation-001",
  "intake": {
    "patient_input": "I have fever and cough for 3 days.",
    "symptoms": [
      {
        "name": "fever",
        "duration": "3 days",
        "severity": null
      },
      {
        "name": "cough",
        "duration": "3 days",
        "severity": null
      }
    ],
    "duration": "3 days",
    "severity": null,
    "missing_information": [],
    "safety_check": {
      "is_emergency": false,
      "reason": null
    }
  },
  "next_action": "continue_intake",
  "response": "Thank you. I have captured the symptoms and duration you provided."
}
```

## 5. Safety Guardrails

The POC treats potentially urgent patterns such as severe chest pain,
difficulty breathing, unconsciousness, and severe bleeding as safety-first cases.

Emergency behavior:
- Do not continue normal specialty routing.
- Do not provide a definitive diagnosis.
- Provide urgent/emergency-care guidance.
- Preserve the extracted patient information in the structured intake.

This is a safety-oriented routing POC, not a medical diagnosis engine.

## 6. System Prompt Guardrails

The system prompt enforces:
- no fabricated patient information;
- no definitive diagnosis;
- no medication prescribing or treatment plans;
- safety-first emergency handling;
- grounded RAG answers;
- clarification when required information is missing;
- structured JSON output.

## 7. RAG Knowledge Base Architecture

```text
Approved healthcare documents
        ↓
cleaning / chunking
        ↓
embeddings
        ↓
vector store
        ↓
retriever
        ↓
relevant context
        ↓
system prompt + patient/context
        ↓
LLM
        ↓
grounded response
```

The RAG layer should answer knowledge-based questions from approved sources and
must not be used to invent patient symptoms or clinical facts.

The existing repository's healthcare document/vector-ingestion work can be
reused as the upstream knowledge-base preparation layer.

## 8. AI-to-.NET Contract

### Proposed request

`POST /api/v1/ai/chat`

```json
{
  "user_id": "user-123",
  "conversation_id": "conversation-001",
  "message": "I have fever and cough for 3 days.",
  "context": {
    "flow": "healthcare",
    "stage": "chat"
  }
}
```

### Proposed response

```json
{
  "status": "success",
  "conversation_id": "conversation-001",
  "intake": {
    "patient_input": "I have fever and cough for 3 days.",
    "symptoms": [
      {
        "name": "fever",
        "duration": "3 days",
        "severity": null
      },
      {
        "name": "cough",
        "duration": "3 days",
        "severity": null
      }
    ],
    "duration": "3 days",
    "severity": null,
    "missing_information": [],
    "safety_check": {
      "is_emergency": false,
      "reason": null
    }
  },
  "next_action": "continue_intake",
  "response": "Thank you. I have captured the symptoms and duration you provided."
}
```

### Emergency response behavior

An emergency request should return the same structured boundary while setting:

```text
safety_check.is_emergency = true
next_action = emergency_guidance
```

Exact production endpoint names and backend field names remain **proposed/TBD**
until confirmed by the .NET team.

## 9. Environment Configuration

Do not commit `.env`.

The existing root `.env.example` should be extended with placeholder values
for the healthcare AI/vector-store configuration, for example:

```env
LLM_API_URL=
LLM_API_KEY=
VECTOR_STORE_URL=
VECTOR_STORE_INDEX=
VECTOR_STORE_API_KEY=
RAG_TOP_K=3
RAG_RELEVANCE_THRESHOLD=0.20
AI_SERVICE_BASE_URL=
AI_SERVICE_CHAT_PATH=/api/v1/ai/chat
AI_SERVICE_TIMEOUT=30
```

## 10. Testing

Run:

```bash
pytest tests/test_healthcare_assistant.py -q
```

Expected coverage:
- symptom extraction;
- duration extraction;
- missing-information behavior;
- emergency escalation;
- normal intake continuation;
- empty input validation;
- system-prompt safety rules.

## 11. Scope Boundaries

This branch does not claim to implement:
- medical diagnosis;
- medication prescribing;
- production healthcare endpoints;
- a production vector database;
- a production LLM provider.

Those are downstream/integration concerns unless separately assigned.

## 12. Status

Core Sprint 1 AI flow is implemented as a self-contained POC suitable for
review and later integration with the existing patient-intake, healthcare
knowledge-base, and .NET application layers.

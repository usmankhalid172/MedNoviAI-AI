# Sprint 1 – AI Safety & Guardrails

**Assignee:** Zainab Raza  
**Role:** AI Safety & Guardrails Engineer  
**Branch:** `feature/sprint1-safety-guardrails-zainab`  
**PR Title:** `Task-sept20-safety-guardrails-zainabraza`

## 1. Objective

Audit system prompts to guarantee non-diagnostic and non-prescriptive response
limits.

Test emergency trigger keywords to ensure high-risk user prompts immediately
return clear safety escalation disclaimers directing users to urgent
professional care or local emergency services.

## 2. Safety Architecture

The Healthcare Assistant uses a deterministic safety layer before normal AI
processing.

Every incoming request is classified before being passed to the normal AI
handler.

The safety layer uses the following priority:

1. Emergency / immediate safety escalation
2. Serious or urgent symptom fallback
3. Prescription or medication-change refusal
4. Personalized treatment refusal
5. Diagnosis refusal
6. Unclear / unsupported medical-query fallback
7. Normal informational response

The implementation does not depend on the AI model to decide whether a
safety boundary should apply.

## 3. Non-Diagnostic Boundary

The system prompt explicitly prevents:

- autonomous diagnosis;
- definitive diagnosis statements;
- confirmation of suspected diseases;
- diagnosis from symptoms alone;
- unsupported clinical conclusions.

Diagnosis requests are handled by the deterministic diagnosis refusal.

## 4. Non-Prescriptive Boundary

The system prompt explicitly prevents:

- prescription generation;
- personalized medication recommendations;
- personalized dosage instructions;
- medication start/stop/change instructions;
- individualized prescription decisions.

Prescription and dosage requests are handled by the deterministic medication
safety refusal.

## 5. Emergency Safety

Emergency safety has the highest priority.

When an emergency indicator is detected:

1. the request is classified as `emergency`;
2. `requires_immediate_redirect` is set to `True`;
3. deterministic emergency guidance is returned;
4. the normal AI handler is not called;
5. the user is directed toward local emergency services or immediate
   professional medical care.

Emergency handling does not diagnose, prescribe, provide dosage instructions,
or create a personalized treatment plan.

## 6. Integration Flow

```text
User Request
    ↓
Input Safety Layer
    ↓
Emergency / Serious / Prescription / Treatment / Diagnosis / Unclear?
    ├── YES → Deterministic Safety Response
    │           ↓
    │        AI handler is not called
    │
    └── NO → Normal AI Processing
                ↓
          Output Safety Validation
                ↓
Unsafe diagnosis/prescription/treatment?
    ├── YES → Safe Deterministic Refusal
    └── NO  → Return Informational Response
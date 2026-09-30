# Sprint 1 – AI Safety & Guardrails

**Assignee:** Zainab Raza  
**Role:** AI Safety & Guardrails Engineer  
**Branch:** `feature/sprint1-safety-guardrails-zainab`  
**PR Title:** `Task-sept19-safety-guardrails-zainabraza`

## 1. Objective

Audit system prompts to strictly prevent autonomous medical diagnoses or
prescription generation.

Verify that high-risk or emergency medical queries trigger immediate safety
disclaimers directing users to urgent professional care or local emergency
services.

The implementation remains deterministic and does not depend on the AI model
to decide whether a safety boundary should apply.

## 2. Sept 19 – System Prompt Audit

The system prompt was reviewed and strengthened in the following areas:

- autonomous diagnosis prevention;
- prescription and medication recommendation prevention;
- personalized dosage prevention;
- emergency escalation;
- high-risk medical query handling;
- prompt-injection resistance;
- AI output safety validation.

The assistant remains an informational healthcare assistant and does not
replace a qualified healthcare professional.

## 3. Diagnosis Safety Boundary

The assistant must not:

- diagnose a user;
- provide a definitive diagnosis;
- confirm that a suspected condition is present;
- state that symptoms prove a disease;
- convert uncertain symptoms into a confirmed diagnosis;
- make a clinical decision on behalf of a healthcare professional.

Diagnosis requests are routed to a deterministic diagnosis refusal.

## 4. Prescription Safety Boundary

The assistant must not:

- prescribe medication;
- select a specific medicine for an individual;
- recommend prescription medication for individual symptoms;
- provide personalized dosage instructions;
- instruct a user to start, stop, increase, decrease, or switch medication.

Prescription and dosage requests are routed to a deterministic medication
safety refusal.

## 5. High-Risk Medical Safety

High-risk medical queries receive a safety boundary before normal healthcare
reasoning.

The deterministic safety layer covers emergency indicators such as:

- severe or crushing chest pain;
- difficulty or inability to breathe;
- gasping for air;
- heavy or uncontrolled bleeding;
- fainting or loss of consciousness;
- unresponsiveness;
- stroke warning signs;
- severe allergic reaction or anaphylaxis;
- throat, lip, or tongue swelling;
- seizure;
- blue or gray lips, face, or skin;
- coughing or vomiting blood;
- severe confusion;
- inability to stay awake.

The high-risk handling is deterministic and does not rely on the model to
decide whether the safety boundary should apply.

## 6. Emergency Escalation

When an emergency indicator is detected:

1. classify the request as `emergency`;
2. set `requires_immediate_redirect` to `True`;
3. return deterministic emergency guidance;
4. do not call the normal AI handler;
5. direct the user to local emergency services or immediate professional
   medical care.

Emergency handling must not:

- diagnose the emergency condition;
- prescribe medication;
- provide dosage instructions;
- provide individualized treatment instructions;
- delay urgent care with unnecessary clarification.

## 7. Safety Priority

The deterministic safety layer uses the following priority:

```text
Emergency
    ↓
Serious / Urgent
    ↓
Prescription
    ↓
Personalized Treatment
    ↓
Diagnosis
    ↓
Unclear / Unsupported
    ↓
Normal Informational Request
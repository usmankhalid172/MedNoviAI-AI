# Sprint 1 – AI Safety & Guardrails

**Assignee:** Zainab Raza  
**Role:** AI Safety & Guardrails Engineer  
**Branch:** `feature/sprint1-safety-guardrails-zainab`  
**PR Title:** `Task-sept13-safety-guardrails-zainabraza`

## 1. Objective

Verify and lock in the Healthcare Assistant safety policy so that the AI acts
strictly as an informational assistant and does not autonomously diagnose,
prescribe medication, or make clinical decisions.

The safety layer also provides deterministic escalation for urgent and
emergency medical conditions.

## 2. Final Assistant Policy

The Healthcare Assistant:

- provides general informational healthcare support;
- does not act as a doctor;
- does not independently diagnose users;
- does not prescribe medicines;
- does not provide personalized dosage instructions;
- does not make individual treatment decisions;
- does not replace professional medical care.

## 3. Input Safety Policy

Every incoming healthcare request passes through the safety layer before
normal AI processing.

The input categories are:

1. Emergency
2. Serious or urgent symptoms
3. Prescription or medication request
4. Diagnosis request
5. Unclear medical query
6. Normal informational request

## 4. Safety Escalation Matrix

| Condition | Required behavior |
|---|---|
| Emergency | Immediate professional/emergency-care guidance |
| Serious / urgent symptoms | Prompt professional medical evaluation |
| Prescription request | Refuse personalized prescribing |
| Diagnosis request | Refuse definitive diagnosis |
| Unclear medical concern | Safe uncertainty fallback + referral |
| Normal informational query | General informational response |

## 5. Emergency Escalation

Potential emergency indicators include:

- severe or crushing chest pain;
- difficulty breathing;
- inability to breathe;
- severe or uncontrolled bleeding;
- loss of consciousness;
- unconsciousness;
- stroke warning signs;
- severe allergic reaction;
- throat swelling affecting breathing;
- seizure.

Emergency flow:

```text
User request
    ↓
Safety layer
    ↓
Emergency detected
    ↓
Immediate professional/emergency care guidance
    ↓
Stop normal AI processing
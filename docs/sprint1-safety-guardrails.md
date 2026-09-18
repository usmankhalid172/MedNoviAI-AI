# Sprint 1 – AI Safety & Guardrails

**Assignee:** Zainab Raza  
**Role:** AI Safety & Guardrails Engineer  
**Branch:** `feature/sprint1-safety-guardrails-zainab`  
**PR Title:** `Task-sept11-safety-guardrails-zainabraza`

## 1. Objective

Implement and test deterministic AI safety responses that prevent autonomous
medical diagnosis and prescription suggestions and provide appropriate fallback
and referral guidance for emergency, serious, and unclear medical queries.

## 2. Safety Categories

The safety layer recognizes:

1. Emergency
2. Serious symptoms
3. Prescription or medication request
4. Diagnosis request
5. Unclear medical query
6. Normal informational request

## 3. Safety Response Matrix

| Request type | Expected behavior |
|---|---|
| Emergency | Immediate emergency-care fallback |
| Serious symptoms | Prompt professional medical evaluation |
| Prescription | Refuse personalized prescribing |
| Diagnosis | Refuse definitive diagnosis |
| Unclear medical query | Safe uncertainty fallback + professional referral |
| Normal information | Allow general informational response |

## 4. Emergency Fallback

Emergency conditions have the highest safety priority.

Examples:

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
User input
    ↓
Safety layer
    ↓
Emergency detected
    ↓
Immediate professional/emergency care guidance
    ↓
Stop normal AI processing
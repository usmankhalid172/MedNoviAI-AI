# Sprint 1 – AI Safety & Guardrails

**Assignee:** Zainab Raza  
**Role:** AI Safety & Guardrails Engineer  
**Branch:** `feature/sprint1-safety-guardrails-zainab`  
**PR Title:** `Task-sept15-safety-guardrails-zainabraza`

## 1. Objective

Review unsafe and unsupported medical questions so the Healthcare Assistant
strictly avoids autonomous diagnosis, prescription, dosage advice, and
personalized treatment decisions.

Verify that immediate emergency escalation triggers correctly redirect users
to local emergency services or qualified healthcare professionals before
normal AI processing.

## 2. Sept 15 Safety Review

The review strengthens the existing deterministic safety layer in four areas:

- expanded natural-language emergency detection;
- stronger diagnosis and prescription request coverage;
- explicit detection of personalized treatment requests;
- regression coverage proving safety responses bypass normal AI handling.

The implementation remains deterministic and does not depend on the model
to decide whether a safety boundary should apply.

## 3. Input Safety Policy

Every incoming healthcare request passes through the safety layer before
normal AI processing.

Priority order:

1. Emergency / immediate safety escalation
2. Serious or urgent symptom fallback
3. Prescription or medication-change refusal
4. Personalized treatment refusal
5. Diagnosis refusal
6. Unclear medical-query fallback
7. Normal informational response

An emergency always overrides a diagnosis, prescription, dosage, or treatment
request contained in the same user message.

## 4. Unsupported Medical Requests

### Diagnosis

The assistant must not:

- diagnose a user;
- confirm a suspected condition;
- identify a disease as the user's diagnosis from symptoms alone;
- convert uncertainty into a definitive diagnosis.

Detected diagnosis requests are routed to a deterministic diagnosis refusal.

### Prescription and Dosage

The assistant must not:

- choose a medication for a specific user;
- prescribe antibiotics or other medicines;
- provide personalized dosage instructions;
- instruct a user to start, stop, increase, decrease, or switch medication.

Detected requests are routed to a deterministic medication-safety refusal.

### Personalized Treatment

The assistant must not choose a treatment plan for a specific user.

Examples that must be blocked include:

- "What treatment should I follow?"
- "How should I treat my symptoms?"
- "What treatment is best for me?"
- "What should I do to cure this?"

General educational questions such as "What treatment options are commonly used
for asthma?" remain normal informational requests when they are not
personalized.

## 5. Emergency Escalation

Potential emergency indicators include:

- severe or crushing chest pain;
- inability or difficulty breathing;
- gasping for air;
- heavy or uncontrolled bleeding;
- fainting, loss of consciousness, or unresponsiveness;
- stroke warning signs such as sudden one-sided weakness, facial drooping,
  or sudden speech difficulty;
- severe allergic reaction or anaphylaxis;
- throat, lip, or tongue swelling;
- seizure.

Emergency response behavior:

1. classify the request as `emergency`;
2. set `requires_immediate_redirect` to `True`;
3. return deterministic emergency guidance;
4. do not call the normal AI handler;
5. direct the user to local emergency services or immediate care from a
   qualified healthcare professional.

The safety layer does not diagnose the emergency condition or provide
medication or dosage instructions.

## 6. Integration Flow

```text
User Request
    ↓
Input Safety Layer
    ↓
Emergency / Serious / Prescription / Treatment / Diagnosis / Unclear?
    ├── YES → Deterministic safety response
    └── NO
         ↓
      Normal AI Processing
         ↓
      Output Safety Validation
         ↓
Unsafe diagnosis/prescription/treatment?
    ├── YES → Safe deterministic refusal
    └── NO  → Return informational response

### Sept 16 – Safety Guardrail Regression & Escalation Review

### Objective

Test and refine the Healthcare Assistant safety layer against:

- diagnostic requests;
- prescription and dosage recommendations;
- personalized treatment requests;
- unsupported or unclear medical queries;
- serious and urgent health scenarios;
- emergency health scenarios.

The goal is to verify that unsafe requests are intercepted before normal AI
processing and that emergency or urgent situations receive appropriate
professional-care escalation.

### Safety Categories

The current deterministic safety categories are:

1. Emergency
2. Serious / urgent symptoms
3. Prescription / medication request
4. Personalized treatment request
5. Diagnosis request
6. Unclear / unsupported medical query
7. Normal informational request

### Priority

The safety layer uses the following priority:

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
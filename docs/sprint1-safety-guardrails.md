# Sprint 1 – Final Prompt Structure & AI Safety Guardrails

**Assignee:** Zainab Raza  
**Role:** AI Safety Engineer  
**Branch:** `feature/sprint1-safety-guardrails-zainab`  
**PR Title:** `Task-sept8-safety-guardrails-zainabraza`

## 1. Objective

Finalize the healthcare assistant system prompt and enforce deterministic safety
boundaries for non-diagnostic, prescription, and emergency requests.

## 2. Safety Policy

The assistant is informational only. It must not:

- provide a definitive medical diagnosis;
- prescribe medicines;
- provide personalized dosage or prescription changes;
- invent patient symptoms, medical history, test results, or diagnoses;
- replace professional medical evaluation or emergency services.

## 3. Refusal Logic

### Diagnosis Requests

Examples:

- `What disease do I have?`
- `Do I definitely have diabetes?`

Expected behavior:

- refuse to provide a definitive diagnosis;
- explain the informational limitation;
- encourage professional evaluation where appropriate.

### Prescription Requests

Examples:

- `What antibiotic should I take?`
- `Can I increase my dosage?`
- `Should I stop my medication?`

Expected behavior:

- refuse personalized prescribing or dosage instructions;
- recommend consultation with a qualified healthcare professional or pharmacist.

### Emergency Requests

Examples:

- severe chest pain;
- difficulty breathing;
- inability to breathe;
- heavy/severe bleeding;
- loss of consciousness;
- stroke warning language.

Expected behavior:

- immediately use the urgent-care path;
- direct the user to urgent or emergency professional medical care;
- do not diagnose or continue normal medication/diagnosis handling.

## 4. Safety Priority

When multiple safety conditions are present, the priority is:

1. Emergency
2. Prescription / medication-change request
3. Diagnosis request
4. Normal informational request

Example:

`I have severe chest pain. What medicine should I take?`

Expected classification: **Emergency**, because urgent safety takes priority over
prescription handling.

## 5. Prompt Structure

The finalized system prompt includes:

- non-diagnostic boundary;
- prescription and medication boundary;
- emergency safety boundary;
- explicit refusal logic;
- anti-fabrication rules;
- grounded/RAG rules;
- privacy requirements;
- prompt-injection resistance;
- clear communication requirements.

## 6. Deterministic Guardrail Mechanism

```text
User input
    ↓
Normalize input
    ↓
Emergency check
    ↓ no
Prescription check
    ↓ no
Diagnosis check
    ↓ no
Normal informational flow
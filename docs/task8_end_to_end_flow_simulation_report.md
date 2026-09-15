# Task 8 — AI + .NET Single End-to-End Test Journey Simulation

**Assignee:** Joyce Hany  
**Role:** Simulation QA Engineer  
**Task:** AI + .NET Single End-to-End Test Journey Simulation  
**Branch:** `feature/sprint1-flow-simulation-joyce`  
**PR Title:** `Task-sept8-flow-simulation-joycehany`  
**Date:** September 8, 2026

---

## 1. Objective

The objective of this task is to execute a local simulation of the target healthcare end-to-end flow:

Patient Input → AI Processing → Symptom Extraction → Specialty Mapping → Structured Output

The simulation is intended to verify system stability and identify integration blockers between the AI processing layer and the .NET backend.

---

## 2. Test Environment

Repository:

`usmankhalid172/MedNoviAI-AI`

Target branch:

`feature/sprint1-flow-simulation-joyce`

Repository inspection confirmed the following remote branches:

- `origin/main`
- `origin/feature/sprint1-data-indexing-rameesha`

No healthcare implementation branch containing the required end-to-end AI flow was available.

---

## 3. Implementation Availability Check

The repository was inspected for healthcare AI implementation and API routes related to:

- patient input
- symptom extraction
- specialty mapping
- structured patient output
- healthcare chat
- healthcare intake
- healthcare recommendation

No implemented healthcare API endpoint was found in the available branches.

The existing `src/` application is a financial AI POC and exposes financial/chatbot functionality rather than the required healthcare patient flow.

The `healthcare-platform/` directory contains knowledge-base and RAG preparation assets, including:

- healthcare knowledge base
- medical specialty information
- vector-ready chunks
- healthcare vector ingestion script
- environment configuration template

These assets prepare medical context for downstream retrieval but do not implement the required patient conversation flow.

---

## 4. Target End-to-End Flow

Expected flow:

```text
Patient Input
      |
      v
AI Processing
      |
      v
Symptom Extraction
      |
      v
Specialty Mapping
      |
      v
Structured Output
Expected structured output should contain, at minimum, information representing the extracted symptoms and recommended medical specialty.

The actual API contract for this flow is not implemented in the checked repository.

5. Simulation Scenarios
Scenario 1 — Basic Patient Symptom

Sample input

I have been having chest pain for two days.

Expected processing

Patient Input
→ AI Processing
→ Symptom Extraction: chest pain
→ Specialty Mapping: Cardiology
→ Structured Output

Expected result: PASS only if the healthcare AI flow is implemented and returns structured output.

Actual result: BLOCKED.

Reason: No implemented healthcare AI endpoint was available to execute the flow.

Scenario 2 — Skin-related Symptom

Sample input

I have an itchy red rash on my arm.

Expected processing

Patient Input
→ AI Processing
→ Symptom Extraction: itchy red rash
→ Specialty Mapping: Dermatology
→ Structured Output

Expected result: PASS only if symptom extraction and specialty mapping are implemented.

Actual result: BLOCKED.

Reason: No healthcare patient-processing API was available.

Scenario 3 — Pediatric Symptom

Sample input

My child has a fever and sore throat.

Expected processing

Patient Input
→ AI Processing
→ Symptom Extraction: fever, sore throat
→ Specialty Mapping: Pediatrics
→ Structured Output

Expected result: PASS only if the healthcare flow is implemented.

Actual result: BLOCKED.

Reason: The repository contains Pediatrics knowledge-base data, but no patient-flow API capable of executing this journey.

Scenario 4 — General / Unclear Symptom

Sample input

I don't feel well and I have been tired recently.

Expected processing

Patient Input
→ AI Processing
→ Symptom Extraction
→ Specialty Mapping
→ Structured Output

Expected result: The system should process uncertainty safely and avoid making an unsupported diagnosis.

Actual result: BLOCKED.

Reason: No healthcare conversational processing endpoint was available for execution.

6. Healthcare Knowledge Base Verification

The healthcare knowledge-base documentation and data were inspected.

Available specialty categories include:

Cardiology
Dermatology
Pediatrics
General Medicine

The repository also contains vector-ready healthcare context generated through the ingestion pipeline.

This confirms that medical knowledge preparation exists.

However:

Knowledge Base / RAG Preparation ≠ Complete Patient AI Flow

The available implementation does not expose the required sequence:

Patient Input
→ Symptom Extraction
→ Specialty Mapping
→ Structured Output
7. .NET Integration Verification

The environment template contains:

DOTNET_BACKEND_API_URL=http://localhost:5000/api

This is a configuration placeholder.

No .NET project implementation containing the required healthcare controllers or endpoints was found in the checked repository.

Therefore, an actual AI-to-.NET integration request could not be executed.

8. Execution Result
Test Area	Expected	Actual	Status
Patient input processing	Healthcare input accepted	Healthcare endpoint unavailable	BLOCKED
Symptom extraction	Symptoms extracted	Endpoint unavailable	BLOCKED
Specialty mapping	Specialty selected	Endpoint unavailable	BLOCKED
Structured output	Structured healthcare response	Endpoint unavailable	BLOCKED
.NET integration	AI request reaches backend	Backend implementation unavailable	BLOCKED
RAG knowledge availability	Medical context available	Vector-ready data available	PASS
Repository/branch readiness	Task branch available	Branch available	PASS
9. Blocker

The primary blocker is the absence of the healthcare AI processing implementation and the corresponding .NET integration API in the checked repository branches.

The available healthcare module currently contains knowledge-base preparation and vector ingestion assets, but not the end-to-end patient processing service.

Because of this, executing the target flow as a real API journey would require inventing endpoints or implementation that are outside the scope of this QA task.

No artificial PASS result was recorded.

10. QA Conclusion

Overall Task 8 Result: BLOCKED

The QA inspection and simulation scenarios were completed at the repository/contract availability level.

The healthcare knowledge-base and RAG preparation layer is present and usable as a downstream dependency.

The requested end-to-end healthcare journey cannot currently be executed because the required healthcare AI processing and .NET backend integration implementation is not available in the checked repository branches.

Once the healthcare AI and .NET endpoints are available, the four scenarios documented in this report can be executed as functional end-to-end tests.

11. Recommended Next Step

The AI/.NET implementation team should provide the implemented healthcare API contract and deployment/local startup instructions.

After the implementation is available, QA should re-run:

Patient input
Symptom extraction
Specialty mapping
Structured output validation
AI-to-.NET request/response validation
Error and uncertainty scenarios

The final result should then be updated from BLOCKED to PASS or FAIL based on actual execution evidence.
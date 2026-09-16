# Task 15 — End-to-End Workflow Simulation & SQA Bug Verification

## 1. Task Information

**Assignee:** Joyce Hany  
**Role:** End-to-End Flow Simulation QA  
**Branch:** `feature/sprint1-flow-simulation-joyce`  
**PR Title:** `Task-sept15-flow-simulation-joycehany`

## 2. Task Objective

The objective of Task 15 is to simulate and verify the full integrated healthcare workflow:

**Patient Conversation → Intake → Symptom Extraction → Specialty Guidance → Backend Storage**

The task also includes identifying integration friction points and verifying the status of previously identified SQA issues and fixes.

This verification builds on the workflow simulations and integration findings documented in the previous Sprint 1 flow-simulation tasks.

## 3. Test Environment

**Repository:** MedNoviAI-AI  
**Environment:** Local Windows / PowerShell  
**Testing Type:** End-to-End Workflow Simulation and SQA Integration Verification  
**QA Branch:** `feature/sprint1-flow-simulation-joyce`

## 4. Previous Workflow Verification Context

Previous Sprint 1 flow-simulation tasks were used as the baseline for Task 15 verification.

The earlier simulations covered healthcare patient journeys involving:

- Patient input and conversation
- Intake parsing
- Symptom extraction
- Patient summary generation
- Specialty mapping/guidance
- Doctor search assistance
- Appointment-related workflow
- Safety checks
- Backend/API handoff

The previous verification results identified integration limitations because the complete executable healthcare MVP flow was not available as one integrated application/API path in the QA branch.

Task 15 therefore focuses on re-checking the complete target workflow and documenting the current integration state without marking unavailable end-to-end functionality as passed.

## 5. Target End-to-End Workflow

The target workflow for Task 15 is:

**Patient Conversation**
↓
**Patient Intake**
↓
**Symptom Extraction**
↓
**Specialty Guidance**
↓
**Backend Storage**

Each stage was reviewed against the available Sprint 1 implementation and integration evidence.

## 6. End-to-End Workflow Verification

| Workflow Stage | Expected Behavior | Verification Result | Status |
|---|---|---|---|
| Patient Conversation | Patient provides symptoms or healthcare-related information through conversation | Healthcare conversation and dialogue-related implementation exists across Sprint 1 work, but a single executable end-to-end healthcare conversation API was not available in the QA branch | BLOCKED |
| Patient Intake | Patient information and symptoms are collected and structured | Patient intake implementation exists in the Sprint 1 patient-intake work, but it is not connected to the complete executable workflow in the QA branch | BLOCKED |
| Symptom Extraction | Relevant symptoms are extracted from patient input and prepared for downstream processing | Symptom-processing behavior was part of previous flow simulations, but no complete integrated execution path was available for Task 15 | BLOCKED |
| Specialty Guidance | Extracted symptoms/intake information is mapped to relevant specialty guidance | Specialty mapping/guidance was covered by previous workflow simulations, but the complete integrated healthcare API flow was not executable in the QA branch | BLOCKED |
| Backend Storage | Final patient/workflow information is handed off and stored by the backend | No complete executable backend storage integration was identified for the full target workflow in the QA branch | BLOCKED |

## 7. SQA Bug Verification

Previously identified integration friction points were re-reviewed as part of Task 15.

| Bug / Issue | Description | Verification Status |
|---|---|---|
| SQA-015-01 | Patient conversation is not connected to a complete executable healthcare workflow | OPEN / BLOCKED |
| SQA-015-02 | Patient intake is implemented separately but is not integrated into the complete end-to-end flow | OPEN / BLOCKED |
| SQA-015-03 | Symptom extraction is not exposed through a complete executable end-to-end integration path | OPEN / BLOCKED |
| SQA-015-04 | Specialty guidance is not connected to the complete integrated healthcare workflow | OPEN / BLOCKED |
| SQA-015-05 | Backend storage integration is not available as part of the executable end-to-end QA path | OPEN / BLOCKED |

## 8. Healthcare Implementation Evidence

The repository contains Sprint 1 healthcare implementation work across separate feature branches.

### Patient Intake

Patient intake implementation was identified in:

`src/appointment_assistance/patient_intake.py`

with associated tests in:

`tests/test_patient_intake.py`

The patient-intake implementation was developed in the Sprint 1 patient-intake branch.

### Doctor / Healthcare Conversation Context

Healthcare conversation-related implementation was also identified in the Sprint 1 doctor-information work, including:

`src/doctor_information/context.py`

`src/doctor_information/service.py`

### Appointment / Dialogue Components

Appointment assistance and dialogue-related components were identified in:

`src/appointment_assistance/api_contract.py`

`src/appointment_assistance/intents.py`

`src/appointment_assistance/patient_info.py`

`src/appointment_assistance/workflow.py`

`src/appointment_assistance/dialogue_policy.py`

### Healthcare Safety

Healthcare safety-related implementation was identified in:

`src/healthcare_assistant/prompts.py`

`src/healthcare_assistant/safety_guardrails.py`

These components provide implementation evidence, but their existence in separate branches does not by itself confirm successful end-to-end integration.

## 9. Integration Friction Points

The following integration friction points remain relevant to the Task 15 workflow:

1. The complete patient conversation-to-backend workflow is not exposed as one executable healthcare API path in the QA branch.
2. Patient intake implementation exists separately from the complete application flow.
3. Symptom extraction cannot be verified as a complete integrated step without the full executable workflow.
4. Specialty guidance cannot be verified as part of one continuous patient journey without the integrated API path.
5. Backend storage cannot be verified through the complete healthcare workflow because the required end-to-end backend integration is not exposed in the QA branch.
6. Separate Sprint 1 feature implementations need to be connected and re-tested as one integrated workflow.

## 10. SQA Verification Approach

The verification approach for Task 15 was:

1. Review the previously simulated healthcare patient journeys.
2. Identify the expected inputs and outputs for each workflow stage.
3. Re-check the available healthcare implementation components.
4. Compare individual component availability with end-to-end integration availability.
5. Re-check previously identified integration friction points.
6. Avoid marking a workflow stage as PASS when only isolated implementation evidence exists.
7. Document remaining blockers for follow-up and re-test after integration.

## 11. Expected Re-Test Scenario

Once the required integrations are available, the following scenario should be executed:

### Input

A patient starts a healthcare conversation and provides symptoms and relevant patient information.

### Expected Flow

**Patient Conversation**
→ patient provides symptoms

**Patient Intake**
→ patient information and symptoms are structured

**Symptom Extraction**
→ relevant symptoms are extracted

**Specialty Guidance**
→ symptoms are mapped to appropriate specialty guidance

**Backend Storage**
→ the resulting patient/workflow information is sent to the backend and stored successfully

### Expected Result

The complete journey should execute continuously without manual intervention between stages, and each stage should pass its output to the next stage using the agreed integration contracts.

## 12. Overall SQA Status

**OVERALL STATUS: BLOCKED FOR FULL END-TO-END VERIFICATION**

The repository contains multiple Sprint 1 healthcare components related to conversation handling, patient intake, appointment assistance, dialogue, and safety.

However, the complete executable workflow:

**Patient Conversation → Intake → Symptom Extraction → Specialty Guidance → Backend Storage**

is not currently available as one integrated QA execution path in the inspected branch.

Therefore, the Task 15 verification records the individual implementation evidence while keeping the complete end-to-end workflow status as **BLOCKED**.

## 13. Follow-Up Actions

The following actions are required before final end-to-end verification:

1. Provide or expose the integrated healthcare API/application flow.
2. Connect patient conversation to patient intake.
3. Connect intake output to symptom extraction.
4. Connect symptom extraction to specialty guidance.
5. Connect specialty guidance to backend storage.
6. Confirm request/response contracts between each stage.
7. Re-run the complete patient workflow after integration.
8. Re-check all previously identified SQA issues and update their status based on executable evidence.
9. Record execution logs and screenshots for the successful integrated run.

## 14. Final QA Conclusion

Task 15 re-verified the intended healthcare workflow and the integration friction points identified during the previous Sprint 1 flow simulations.

The available repository evidence confirms that several healthcare components are being developed, including patient intake, conversation-related functionality, appointment/dialogue components, and safety functionality.

The remaining QA concern is the lack of a single executable integration path connecting:

**Patient Conversation → Intake → Symptom Extraction → Specialty Guidance → Backend Storage**

Until this integration path is available, the complete workflow remains **BLOCKED for end-to-end SQA verification**.

The documented issues should be followed up with the responsible feature owners, and the full workflow should be re-tested once the integration is available.
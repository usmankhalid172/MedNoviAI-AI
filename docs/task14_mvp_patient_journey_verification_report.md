# Task 14 — MVP Patient Journey Verification & Flow Simulation

## 1. Task Information

**Assignee:** Joyce Hany  
**Role:** End-to-End Flow Simulation QA  
**Branch:** `feature/sprint1-flow-simulation-joyce`  
**PR Title:** `Task-sept14-flow-simulation-joycehany`

## 2. Objective

The objective of Task 14 is to simulate and verify the core MVP patient journey:

**Registration/Login → Doctor Search → Specialty Search → Appointment Booking → Patient Intake → AI Assistant**

The purpose of this QA activity is to verify the availability and integration of the required MVP components and document remaining integration friction points for immediate follow-up.

## 3. Test Environment

**Repository:** MedNoviAI-AI  
**Environment:** Local Windows / PowerShell  
**Testing Type:** MVP End-to-End Flow Simulation and Integration QA  
**QA Branch:** `feature/sprint1-flow-simulation-joyce`

## 4. Repository Verification

The repository was inspected for the components required by the MVP patient journey.

The current repository contains healthcare-related implementation work across separate Sprint 1 branches, including:

- Patient intake implementation
- Doctor information and conversation context
- Appointment assistance workflow
- Multi-turn appointment dialogue policy
- Healthcare safety guardrails
- Healthcare knowledge-base and vector-ready data

The following implementation branches were identified during verification:

- `feature/sprint1-patient-intake-mehar`
- `feature/sprint1-doctor-info-farheen`
- `feature/sprint1-appointment-assistant-mehar`
- `feature/sprint1-appointment-dialogue-mehar`
- `feature/sprint1-safety-guardrails-zainab`
- `feature/sprint1-ai-qa-isma`

## 5. MVP Patient Journey Verification

| Journey Stage | Expected Behavior | Verification Result | Status |
|---|---|---|---|
| Registration / Login | Patient can register or log in and continue to the healthcare journey | No executable registration/login healthcare API was identified in the inspected repository | BLOCKED |
| Doctor Search | Patient can search for available doctors | Doctor information implementation exists in a separate Sprint 1 branch, but no executable end-to-end doctor-search API was identified in the current QA branch | BLOCKED |
| Specialty Search | Patient can search/select a medical specialty | Healthcare specialty reference data exists, but no executable end-to-end specialty-search API was identified | BLOCKED |
| Appointment Booking | Patient can select a doctor/slot and book an appointment | Appointment assistance and dialogue implementation exist in separate branches, but no executable booking endpoint was identified in the current QA branch | BLOCKED |
| Patient Intake | Patient information and symptoms are collected and structured | Patient intake implementation exists in the Sprint 1 patient-intake branch, but it is not integrated into an executable end-to-end application flow in the current QA branch | BLOCKED |
| AI Assistant | Patient can interact with the healthcare AI assistant as part of the MVP journey | Healthcare assistant and safety-related implementation exists, but no executable end-to-end MVP assistant API was identified in the current QA branch | BLOCKED |

## 6. Implementation Evidence

### Patient Intake

The patient-intake branch contains implementation updates in:

`src/appointment_assistance/patient_intake.py`

and associated tests:

`tests/test_patient_intake.py`

The latest identified commit was:

`678017d Task-sept10-Improve-patient-intake-dialogue-meharali`

### Doctor Information

The doctor-information branch contains implementation updates in:

`src/doctor_information/context.py`

`src/doctor_information/service.py`

with associated tests.

The latest identified commit was:

`2957a59 feat: add doctor conversation context handling`

### Appointment Assistance

The appointment-assistance branch contains:

`src/appointment_assistance/api_contract.py`

`src/appointment_assistance/intents.py`

`src/appointment_assistance/patient_info.py`

`src/appointment_assistance/workflow.py`

The latest identified appointment-assistance implementation commit was:

`5714aef Add-Sprint-1-appointment-assistance-workflow-meharali`

### Appointment Dialogue

The appointment-dialogue branch contains:

`src/appointment_assistance/dialogue_policy.py`

with associated dialogue-policy tests.

The latest identified commit was:

`40e75cd Sep9-Improve-multi-turn-patient-dialogue-policy-meharali`

### Safety Guardrails

Healthcare safety guardrail implementation was also identified in:

`src/healthcare_assistant/prompts.py`

`src/healthcare_assistant/safety_guardrails.py`

with associated tests.

The latest identified commit was:

`42f64f2 Upgrade AI safety and emergency guardrails`

## 7. API / Integration Verification

The current QA branch was inspected for executable healthcare API routes.

The route inspection identified application routes related to existing legacy functionality, including expense categorization and financial-health functionality.

No executable healthcare API routes were identified in the current QA branch for the complete MVP journey:

- Registration/Login
- Doctor Search
- Specialty Search
- Appointment Booking
- Patient Intake
- AI Assistant

The healthcare-platform directory currently contains healthcare data, documentation, and ingestion-related resources, but does not provide the complete executable backend/API layer required for the target MVP journey.

## 8. Integration Friction Points

| Issue ID | Friction Point | Status |
|---|---|---|
| BUG-014-01 | Registration/Login integration is not available for end-to-end QA execution | Open |
| BUG-014-02 | Doctor information implementation is not connected to an executable doctor-search endpoint in the QA branch | Open |
| BUG-014-03 | Specialty search integration is not exposed as an executable MVP API | Open |
| BUG-014-04 | Appointment assistance/dialogue implementation is not connected to an executable booking endpoint in the QA branch | Open |
| BUG-014-05 | Patient intake implementation exists separately but is not integrated into the complete MVP journey | Open |
| BUG-014-06 | AI assistant integration is not exposed as an executable end-to-end MVP API in the QA branch | Open |

## 9. QA Coordination / Follow-up

The remaining integration friction points should be coordinated with Isma and the responsible feature owners for immediate verification and fixes.

Required follow-up includes:

1. Provide the registration/login integration contract.
2. Expose doctor search functionality through the MVP application flow.
3. Expose specialty search functionality.
4. Connect appointment assistance/dialogue to the actual appointment booking flow.
5. Connect patient intake to the patient journey.
6. Connect the healthcare AI assistant to the MVP application flow.
7. Provide the executable API base URL and request/response contracts.
8. Re-run the complete patient journey after integration fixes are available.

## 10. Overall QA Status

**OVERALL STATUS: BLOCKED FOR FULL END-TO-END EXECUTION**

Healthcare MVP components are being developed across multiple Sprint 1 branches, including patient intake, doctor information, appointment assistance/dialogue, and safety guardrails.

However, the inspected QA branch does not currently expose the complete executable application/API integration required to run:

**Registration/Login → Doctor Search → Specialty Search → Appointment Booking → Patient Intake → AI Assistant**

Therefore, the available implementation components were documented as integration evidence, but unexecuted end-to-end functionality was not marked as PASS.

## 11. Final QA Conclusion

Task 14 identified meaningful Sprint 1 healthcare implementation across multiple feature branches, including patient intake, doctor information, appointment assistance, appointment dialogue, and safety guardrails.

The remaining issue is end-to-end integration of these components into an executable MVP patient journey.

The workflow remains **BLOCKED for full end-to-end execution** until the required application/API integration is available.

The identified friction points have been documented for coordination with Isma and the responsible feature owners.
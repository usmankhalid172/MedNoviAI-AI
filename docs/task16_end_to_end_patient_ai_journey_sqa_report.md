# Task 16 — End-to-End Patient AI Journey Simulation & SQA Verification

## 1. Task Information

**Assignee:** Joyce Hany  
**Role:** End-to-End Flow Simulation QA  
**Branch:** `feature/sprint1-flow-simulation-joyce`  
**PR Title:** `Task-sept16-flow-simulation-joycehany`

## 2. Objective

The objective of Task 16 is to execute local simulations for the complete patient AI journey:

**Patient Chat → Intake Parsing → Symptom Extraction → Specialty Guidance → Safe Structured Response**

The task also includes coordinating integration issues with SQA and verifying available developer fixes.

## 3. Test Environment

**Repository:** MedNoviAI-AI  
**Environment:** Local Windows / PowerShell  
**Testing Type:** End-to-End Patient AI Journey Simulation and SQA Verification  
**QA Branch:** `feature/sprint1-flow-simulation-joyce`

## 4. Repository and Branch Verification

The QA branch was verified before testing.

Current branch:

`feature/sprint1-flow-simulation-joyce`

Working tree status:

`nothing to commit, working tree clean`

The latest patient-intake implementation was identified on:

`origin/feature/sprint1-patient-intake-mehar`

Latest patient-intake commit:

`edbf9b4 Task-sept13-finalize-patient-intake-flow`

## 5. Patient Intake Implementation Verification

The latest patient-intake implementation contains:

`src/appointment_assistance/patient_intake.py`

and associated tests:

`tests/test_patient_intake.py`

The patient-intake test file contains:

**47 automated test cases**

The implementation provides a `PatientIntakeCollector` that supports collecting patient information across multiple conversation turns.

### Required information

The required fields are:

- Symptoms
- Symptom onset
- Age group

### Optional information

The optional fields are:

- Secondary history
- Additional details

## 6. Intake Dialogue Verification

The implementation supports multi-turn patient dialogue.

Example flow:

### Turn 1

Patient:

`I've been having a headache.`

Expected system behavior:

The symptom is extracted and the system asks:

`When did your symptoms start?`

### Turn 2

Patient:

`Two days ago.`

Expected system behavior:

The symptom onset is extracted and the system asks:

`What is your age group?`

### Turn 3

Patient:

`I'm 22.`

Expected system behavior:

The age is converted to the `adult` age group.

The intake becomes ready and the system produces a structured patient context.

## 7. Symptom Extraction Verification

The patient-intake implementation supports extraction of a primary complaint from natural language.

Examples covered by the available tests include:

- `I have a headache.`
- `I've been having a headache.`
- `I have a fever.`
- `I have a cough.`

The extracted information is stored as the patient's primary complaint / symptoms.

## 8. Symptom Onset Verification

The implementation supports symptom onset extraction from messages such as:

- `Since yesterday.`
- `Yesterday.`
- `Two days ago.`
- `Since yesterday.`
- `Started yesterday.`

The extracted onset information is stored as `symptom_onset`.

## 9. Age Group Verification

The implementation supports age-group extraction from both descriptive and numeric inputs.

Examples covered by the tests include:

- `I am an adult.` → `adult`
- `I'm 22.` → `adult`
- `I am 10 years old.` → `child`
- `I am 16 years old.` → `teenager`
- `I am 70 years old.` → `senior`

## 10. Multi-Turn Patient Journey Verification

The implementation supports preserving information between conversation turns.

Example verified scenario:

**Patient:** `I have a headache.`

System asks:

`When did your symptoms start?`

**Patient:** `Yesterday`

System asks:

`What is your age group?`

**Patient:** `Adult`

The resulting intake is marked as ready and the patient information is prepared for handoff.

## 11. Structured Patient Data

When the required information is complete, the implementation creates a standardized backend record containing:

```text
primary_complaint
symptom_onset
age_group
secondary_history
additional_details

Example structure:

{
  "primary_complaint": "headache",
  "symptom_onset": "since yesterday",
  "age_group": "adult",
  "secondary_history": null,
  "additional_details": null
}

The implementation also verifies that incomplete patient intake cannot be converted into a backend record.

12. Handoff Verification

The patient-intake implementation provides a handoff state.

When required information is incomplete:

ready = False
handoff = False

When all required information has been collected:

ready = True
handoff = True

The completed intake can then be passed to the recommendation module through the structured backend record.

13. Safety / Structured Response Verification

The available patient-intake implementation produces a structured response and controls whether the intake is ready for handoff.

However, the current QA branch does not expose an executable integrated healthcare API connecting the complete journey to a production-style safety/guardrail response.

Therefore, the safety and final AI response stage could not be independently verified as a complete end-to-end API flow from the current QA branch.

14. Specialty Guidance Verification

The target Task 16 journey includes:

Symptom Extraction → Specialty Guidance

Repository inspection identified healthcare specialty data and recommendation-related references.

However, no executable specialty-guidance API was identified in the current QA branch that could be executed as part of the complete patient journey.

Therefore, specialty guidance was not marked as PASS based only on source-code or data references.

15. End-to-End Integration Verification

The intended complete journey is:

Patient Chat
    ↓
Intake Parsing
    ↓
Symptom Extraction
    ↓
Specialty Guidance
    ↓
Safe Structured Response

The available patient-intake implementation supports the intake-parsing and symptom-extraction portion of this workflow.

However, the complete executable integration from patient chat through specialty guidance and safe structured response is not available in the current QA branch.

16. SQA Findings
Issue ID	Area	Finding	Status
SQA-016-01	Patient Intake	Multi-turn intake and required-field collection are implemented	Verified
SQA-016-02	Symptom Extraction	Primary symptoms can be extracted from supported natural-language inputs	Verified
SQA-016-03	Symptom Onset	Onset information can be extracted and preserved across turns	Verified
SQA-016-04	Age Group	Numeric and descriptive age inputs are converted into age groups	Verified
SQA-016-05	Structured Data	Completed intake produces a standardized backend record	Verified
SQA-016-06	Handoff	Completed intake sets the handoff state to true	Verified
SQA-016-07	Specialty Guidance	No executable integrated specialty-guidance API was identified in the QA branch	Blocked
SQA-016-08	Safe Structured Response	Complete healthcare AI safety-response integration could not be executed from the QA branch	Blocked
SQA-016-09	End-to-End Integration	Complete Patient Chat → Intake → Symptom → Specialty → Safe Response flow is not exposed as an executable integrated flow	Blocked
17. Integration Friction Points

The main integration friction points identified during Task 16 are:

The patient-intake implementation exists as a component but is not connected to a complete executable end-to-end healthcare API in the QA branch.
Specialty guidance is not exposed as an executable integrated stage in the current QA branch.
The final safe structured AI response could not be verified as part of a complete executable patient journey.
The QA branch currently contains legacy application routes rather than a complete healthcare patient-AI API.
Additional integration work is required before full end-to-end execution can be completed.
18. Developer Fix Verification

The latest patient-intake developer implementation was inspected from:

origin/feature/sprint1-patient-intake-mehar

Latest commit:

edbf9b4 Task-sept13-finalize-patient-intake-flow

The implementation includes expanded patient-intake dialogue handling and associated automated tests.

The implementation provides:

Multi-turn dialogue handling
Symptom extraction
Symptom onset extraction
Age-group extraction
Missing-field tracking
Structured patient context
Backend record generation
Handoff state
Validation for incomplete intake

These changes were verified at source-code level.

19. Overall SQA Status

PARTIALLY VERIFIED / END-TO-END INTEGRATION BLOCKED

The patient-intake component provides substantial functionality for the intake and symptom-extraction stages of the Task 16 journey.

The available implementation also provides structured backend handoff behavior.

However, the complete executable journey:

Patient Chat → Intake Parsing → Symptom Extraction → Specialty Guidance → Safe Structured Response

could not be executed end-to-end from the current QA branch because the required healthcare integration layer is not exposed as an executable flow.

20. Final Conclusion

Task 16 verification confirmed that the available patient-intake implementation supports multi-turn patient conversation, required-field collection, symptom extraction, symptom onset extraction, age-group classification, structured patient data, and backend handoff.

The latest patient-intake implementation was identified at commit:

edbf9b4 Task-sept13-finalize-patient-intake-flow

and contains 47 associated automated test cases.

The remaining SQA work is primarily integration verification. Specialty guidance and the final safe structured AI response require an executable healthcare integration layer before the complete patient journey can be marked as fully verified.

The identified integration friction points should be coordinated with SQA and the responsible developers for follow-up and re-testing once the required integration endpoints are available.
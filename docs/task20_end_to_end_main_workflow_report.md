# Task 20 — End-to-End Main Workflow Verification & Closure QA

**Assignee:** Joyce Hany  
**Role:** End-to-End Flow QA  
**Branch:** `feature/sprint1-flow-simulation-joyce`  
**PR Title:** `Task-sept20-flow-simulation-joycehany`

---

## Objective

Run final end-to-end user journey verification tests for the main healthcare workflow:

Patient Chat → Intake Parsing → Specialty Guidance → Doctor Booking

The objective is to verify the available healthcare workflow, document remaining blockers, and track unresolved issues that prevent full end-to-end closure.

---

# 1. Patient Chat

### Expected

The patient should be able to start a healthcare conversation with the AI assistant and receive a healthcare-related response.

### Test

Healthcare chat endpoint:

`/api/ai/chat`

### Actual Result

The endpoint was tested on the deployed AI service.

The response was:

```json
{
  "detail": "Not Found"
}

Status

BLOCKED

Finding

The required healthcare patient-chat endpoint was not available on the tested deployment.

2. Intake Parsing
Expected

The patient conversation should be processed into structured intake information containing symptoms and relevant patient information.

Actual Result

The required healthcare intake functionality was not exposed through the currently available deployment API.

Status

BLOCKED

Finding

The deployed environment did not provide an executable healthcare intake endpoint for final end-to-end verification.

3. Specialty Guidance
Expected

The system should process the patient's symptoms and provide appropriate specialty guidance.

Actual Result

No executable healthcare specialty-guidance endpoint was available in the tested deployment.

Status

BLOCKED

Finding

Specialty guidance could not be verified as part of the deployed end-to-end patient journey.

4. Doctor Booking
Expected

After specialty guidance, the patient should be able to continue to doctor selection and appointment booking.

Actual Result

The complete healthcare doctor-booking workflow could not be executed because the earlier healthcare AI steps were not available as an integrated deployed flow.

Status

BLOCKED

Finding

Doctor booking could not be verified end-to-end from Patient Chat through the healthcare AI flow.

5. Main Workflow Verification
Workflow Stage	Expected Result	Actual Result	Status
Patient Chat	Healthcare AI chat response	/api/ai/chat returned Not Found	BLOCKED
Intake Parsing	Structured patient intake	Healthcare intake endpoint unavailable	BLOCKED
Specialty Guidance	Specialty guidance	Endpoint unavailable	BLOCKED
Doctor Selection	Doctor selection based on specialty	Integrated flow unavailable	BLOCKED
Doctor Booking	Appointment booking	End-to-end flow unavailable	BLOCKED
Remaining Blockers
Blocker 1 — Healthcare Chat Endpoint

Endpoint: /api/ai/chat

Observed Result: HTTP 404 / Not Found

Impact: Prevents the healthcare patient journey from starting through the deployed AI service.

Status: Open

Responsible Team: AI / Backend

Blocker 2 — Healthcare Intake Integration

The required healthcare intake API was not available through the tested deployment.

Impact: Patient information and symptoms cannot be verified through the deployed E2E flow.

Status: Open

Responsible Team: AI / Backend

Blocker 3 — Specialty Guidance Integration

The required specialty-guidance functionality was not available as an executable deployed healthcare endpoint.

Impact: The patient flow cannot progress from intake to specialty guidance.

Status: Open

Responsible Team: AI

Blocker 4 — Doctor Booking Integration

The complete AI-to-doctor-booking workflow could not be executed.

Impact: Final appointment booking cannot be verified as part of the complete patient journey.

Status: Open

Responsible Team: AI / .NET / Integration

Bug / Blocker Tracking
ID	Issue	Severity	Status	Responsible Team
F-20-01	Healthcare /api/ai/chat endpoint returns Not Found	High	Open	AI / Backend
F-20-02	Healthcare intake endpoint unavailable	High	Open	AI / Backend
F-20-03	Specialty guidance endpoint unavailable	High	Open	AI
F-20-04	Doctor booking integration cannot be verified	High	Open	AI / .NET / Integration
Closure Criteria

The main workflow can be considered ready for final SQA closure after the following are available and verified:

Healthcare Patient Chat endpoint is exposed and functional.
Patient Intake Parsing is executable through the integrated flow.
Specialty Guidance is available and returns the expected structured result.
Doctor search/selection is integrated with the healthcare workflow.
Doctor Booking can be completed successfully.
AI → Backend integration is verified.
Previously reported blockers are fixed and retested.
No unresolved critical integration blocker prevents the complete patient journey.
Retest Plan

After the healthcare endpoints and integrations are available, the following sequence should be retested:

Patient Chat
      ↓
Intake Parsing
      ↓
Symptom Extraction
      ↓
Specialty Guidance
      ↓
Doctor Search
      ↓
Doctor Selection
      ↓
Doctor Booking
      ↓
Backend Request
      ↓
Booking Confirmation

Each stage should be verified before the complete journey is marked as passed.

Final SQA Status

Overall Status: BLOCKED — Closure Pending

The deployed AI service is reachable, but the required healthcare endpoints for the main patient workflow were not available in the tested deployment.

As a result, the final end-to-end workflow:

Patient Chat → Intake Parsing → Specialty Guidance → Doctor Booking

could not be completed and verified.

The remaining blockers have been documented with responsible teams and require retesting after the healthcare AI, backend, and booking integrations become available.

Conclusion

Task 20 final end-to-end verification identified remaining integration blockers preventing closure of the main healthcare patient workflow.

The current evidence supports a BLOCKED status rather than a completed PASS.
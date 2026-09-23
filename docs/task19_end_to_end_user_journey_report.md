# Task 19 — End-to-End User Journey Simulation & SQA Bug Tracking

**Assignee:** Joyce Hany  
**Role:** End-to-End Flow QA  
**Branch:** `feature/sprint1-flow-simulation-joyce`  
**PR Title:** `Task-sept19-flow-simulation-joycehany`

---

## Objective

Simulate the complete healthcare user journey and verify the integration between:

Patient Chat → Intake Parsing → Specialty Guidance → Doctor Search → Backend Request

The objective was to identify integration friction points, verify the available system behavior, and document immediate blockers and findings for the responsible development teams.

---

# 1. Patient Chat

### Expected

The patient should be able to start a healthcare conversation with the AI assistant and receive a healthcare-related response.

### Test

The healthcare chat endpoint was checked on the deployed AI service.

Endpoint:

`/api/ai/chat`

### Actual Result

The endpoint returned:

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

The patient conversation should be processed into structured intake information containing relevant symptoms and patient information.

Actual Result

The required healthcare intake functionality was not available through the currently exposed deployment endpoints.

The available Swagger documentation did not expose the required healthcare intake endpoint.

Status

BLOCKED

Finding

The end-to-end intake parsing flow could not be executed from the tested deployment.

3. Specialty Guidance
Expected

The system should analyze the patient's symptoms and provide appropriate specialty guidance.

Actual Result

No executable healthcare specialty-guidance endpoint was available in the current deployed API documentation.

Status

BLOCKED

Finding

Specialty guidance could not be verified as part of the complete deployed patient journey.

4. Doctor Search
Expected

After receiving specialty guidance, the patient journey should continue to doctor search using the relevant specialty and available doctor data.

Actual Result

The integrated doctor-search step could not be executed from the currently available healthcare AI deployment.

Status

BLOCKED

Finding

The required healthcare integration between AI specialty guidance and doctor search could not be verified.

5. Backend Request
Expected

The structured patient information and AI result should be passed to the backend through the expected integration contract.

Actual Result

The complete healthcare AI → backend request could not be verified because the required healthcare endpoints and integration flow were not exposed in the tested deployment.

Status

BLOCKED

Finding

The final backend handoff could not be tested end-to-end.

Live Deployment Verification

The deployed AI service was reachable and its Swagger documentation was accessible.

The currently exposed API included:

GET /
GET /api/ai/financial-health/{user_id}

The Financial Health endpoint was successfully executed and returned HTTP 200.

The healthcare chat endpoint was also directly tested:

/api/ai/chat

Result:

{
  "detail": "Not Found"
}

This confirms that the healthcare chat route was not available at the tested deployment URL.

Integration Friction Points

The following integration friction points were identified during the simulation:

1. Healthcare Chat Endpoint Availability

The required /api/ai/chat endpoint was not exposed by the tested deployment.

Impact: The patient journey cannot start from the healthcare AI chat step.

Status: BLOCKED

2. Healthcare Intake Integration

The required intake parsing functionality was not available through the exposed deployment API.

Impact: Structured patient information could not be generated and verified through the deployed E2E flow.

Status: BLOCKED

3. Specialty Guidance Integration

The specialty-guidance step could not be executed through an available deployed healthcare endpoint.

Impact: The flow could not progress from patient intake to specialty guidance.

Status: BLOCKED

4. Doctor Search Integration

The AI-to-doctor-search transition could not be verified.

Impact: Doctor search could not be tested as part of the complete healthcare journey.

Status: BLOCKED

5. Backend Handoff

The final AI-to-backend request could not be verified.

Impact: The complete integration contract could not be confirmed through the deployed environment.

Status: BLOCKED

SQA Bug / Finding Log
ID	Finding	Severity	Status	Responsible Team
F-19-01	Healthcare /api/ai/chat endpoint returns Not Found	High	Open / Blocked	AI / Backend
F-19-02	Healthcare intake endpoint is not exposed in deployment	High	Open / Blocked	AI / Backend
F-19-03	Specialty guidance endpoint is not available for E2E testing	High	Open / Blocked	AI
F-19-04	Doctor search integration cannot be verified	High	Open / Blocked	AI / .NET
F-19-05	AI → backend handoff cannot be verified	High	Open / Blocked	AI / .NET
Expected vs Actual Flow
Journey Stage	Expected	Actual	Status
Patient Chat	Healthcare chat response	/api/ai/chat returned Not Found	BLOCKED
Intake Parsing	Structured patient intake	Healthcare intake endpoint unavailable	BLOCKED
Specialty Guidance	Specialty recommendation/guidance	Endpoint unavailable	BLOCKED
Doctor Search	Search doctors based on specialty	Integrated flow unavailable	BLOCKED
Backend Request	Structured AI result sent to backend	Handoff unavailable	BLOCKED
Developer Action Required
AI Team

Please expose and verify the healthcare patient-chat and intake APIs required for the SQA flow.

.NET Team

Please confirm the expected AI → backend request contract and endpoint for the structured patient information and AI result.

Integration Team

Please confirm the deployed healthcare API routes and ensure the SQA environment exposes the same contracts expected by the frontend and backend.

Final SQA Result

Overall Status: BLOCKED

The deployed AI service is reachable and API testing can be performed on the currently exposed endpoints. However, the complete healthcare user journey cannot currently be executed because the required healthcare Chat, Intake, Specialty Guidance, Doctor Search, and Backend integration steps are not available as an executable integrated flow in the tested deployment.

The main blocker was reproduced using concrete API evidence, and the integration friction points were documented for developer follow-up.

Conclusion

The Task 19 simulation confirms that the current deployment does not provide enough exposed healthcare functionality to complete the required end-to-end patient journey.

The identified blockers should be addressed by the responsible AI, .NET, and integration teams before the complete healthcare flow can be retested and verified.
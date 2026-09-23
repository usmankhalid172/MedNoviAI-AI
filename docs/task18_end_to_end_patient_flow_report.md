# Task 18 — End-to-End Patient Flow Simulation & Blocker Logging

**Assignee:** Joyce Hany  
**Role:** End-to-End Flow QA  
**Branch:** `feature/sprint1-flow-simulation-joyce`  
**PR Title:** `Task-sept18-flow-simulation-joycehany`

---

## Objective

Execute an end-to-end patient workflow simulation and verify the integration between:

Patient Chat → Intake Parsing → Specialty Guidance → Doctor Selection → Backend Request

The objective was to identify integration friction points, verify available API behavior, and log blockers for the responsible development teams.

---

## 1. Patient Chat

### Expected

The AI service should provide a healthcare patient-chat endpoint capable of receiving patient input and returning an AI response.

### Test

Endpoint tested:

`/api/ai/chat`

### Actual Result

The endpoint returned:

```json
{
  "detail": "Not Found"
}


tatus

BLOCKED

Blocker

The healthcare chat endpoint was not available on the tested deployment.

2. Intake Parsing
Expected

Patient messages should be processed into structured intake information including relevant symptoms and patient details.

Actual Result

The required healthcare intake endpoint was not exposed in the current Swagger documentation.

Status

BLOCKED

Blocker

No executable healthcare intake API was available through the tested deployment.

3. Specialty Guidance
Expected

The AI should process patient symptoms and provide appropriate specialty guidance.

Actual Result

No executable healthcare specialty-guidance endpoint was available in the current Swagger documentation.

Status

BLOCKED

4. Doctor Selection
Expected

After specialty guidance, the system should allow the patient flow to continue toward doctor selection based on available doctor/specialty data.

Actual Result

The required integrated doctor-selection workflow could not be executed from the available AI deployment.

Status

BLOCKED

5. Backend Request
Expected

The structured patient information and AI result should be handed off to the backend through the expected API integration.

Actual Result

The complete healthcare AI → backend handoff could not be verified because the required healthcare endpoints were not exposed through the current deployment.

Status

BLOCKED

Live API Verification

The deployed AI service was accessible and Swagger documentation was available.

Currently exposed endpoints included:

GET /
GET /api/ai/financial-health/{user_id}

The Financial Health endpoint was successfully executed and returned HTTP 200.

Multiple user IDs were tested:

test-user-001
test-user-002
random-user-999
!!!
Long user ID
Arabic user ID

The endpoint returned the same Financial Health response for all tested IDs.

This behavior was logged as a finding requiring clarification regarding whether the endpoint is intentionally using mock/demo data.

Main Integration Blocker

The main blocker identified during the end-to-end simulation is the absence of the healthcare chat endpoint from the tested deployment.

Tested

/api/ai/chat

Result
{
  "detail": "Not Found"
}

Because Patient Chat is the first step in the required workflow, the remaining flow could not be executed end-to-end.

Blocker Impact

The missing healthcare endpoint prevents verification of:

Patient Chat
Intake Parsing
Specialty Guidance
Doctor Selection
Backend Request

Therefore, the complete patient flow cannot currently be marked as PASS.

SQA Status
Flow Stage	Status
Patient Chat	BLOCKED
Intake Parsing	BLOCKED
Specialty Guidance	BLOCKED
Doctor Selection	BLOCKED
Backend Request	BLOCKED
Complete E2E Flow	BLOCKED
Developer Action Required
AI Team

Please provide/enable the healthcare patient-chat and intake endpoints required for the SQA flow.

.NET Team

Please confirm the expected AI → backend request contract and endpoint for the structured patient summary/handoff.

Integration Team

Please confirm the deployed route(s) for the healthcare AI service and ensure the SQA environment exposes the same contracts expected by the frontend/backend.

Final Result

Overall Status: BLOCKED

The live AI service is reachable and API testing can be performed on the currently exposed Financial Health endpoint. However, the required healthcare patient flow cannot be completed because the healthcare Chat/Intake integration endpoints are not available on the tested deployment.
# Task 24 — Negative Patient Scenarios & API Validation

**Assignee:** Joyce Hany  
**Role:** End-to-End Flow QA  
**Branch:** `feature/sprint1-flow-simulation-joyce`  
**PR Title:** `Task-day24-flow-simulation-joycehany`

---

## Objective

Execute negative patient/API scenarios to verify how the healthcare service handles:

- Unauthorized token access
- Missing Authorization header
- Missing required fields
- Empty input
- Invalid JSON

The objective was to identify whether the deployed healthcare endpoint correctly rejects invalid or unauthorized requests and to document any integration blockers.

---

# 1. Environment Verification

### Branch

```text
feature/sprint1-flow-simulation-joyce

Local API Health

The local health endpoint was tested:

http://127.0.0.1:8000/api/v1/health
Actual Result

The local server was not running.

Observed result:

Unable to connect to the remote server
Status

NOT AVAILABLE

2. Deployed Service Verification

The deployed service root was tested:

https://mednoviai-ai.onrender.com/
Actual Result

HTTP status:

200

The service returned the MedNoviAI AI Service response.

Status

PASS — Deployment Reachable

3. Unauthorized Token Scenario
Test

A healthcare chat request was sent using an invalid Bearer token.

Endpoint:

/api/ai/chat

Request:

POST /api/ai/chat
Authorization: Bearer invalid-token-123

Body:

{
  "message": "I have a headache"
}
Actual Result

HTTP status:

404

Response:

{
  "detail": "Not Found"
}
Expected

An authentication/authorization response such as 401 Unauthorized or another defined authentication error would only be testable if the healthcare chat route were available.

Status

BLOCKED

Finding

The request did not reach healthcare authentication validation because the requested healthcare chat route was not found on the deployed service.

4. Missing Authorization Header
Test

A healthcare chat request was sent without an Authorization header.

Endpoint:

/api/ai/chat

Body:

{
  "message": "I have a headache"
}
Actual Result

HTTP status:

404

Response:

{
  "detail": "Not Found"
}
Status

BLOCKED

Finding

The endpoint returned 404 Not Found before authentication-header validation could be verified.

5. Missing Required Fields — Empty JSON
Test

Request body:

{}

Endpoint:

/api/ai/chat
Actual Result

HTTP status:

404

Response:

{
  "detail": "Not Found"
}
Status

BLOCKED

Finding

Request validation could not be reached because the healthcare chat endpoint was not available.

6. Empty Message
Test

Request body:

{
  "message": ""
}

Endpoint:

/api/ai/chat
Actual Result

HTTP status:

404

Response:

{
  "detail": "Not Found"
}
Status

BLOCKED

Finding

Empty-input validation could not be verified because the healthcare chat endpoint was not available.

7. Invalid JSON
Test

An invalid JSON body was sent:

{"message":

Endpoint:

/api/ai/chat
Actual Result

HTTP status:

404

Response:

{
  "detail": "Not Found"
}
Status

BLOCKED

Finding

Malformed JSON handling could not be verified because the healthcare chat endpoint was not available.

Negative Scenario Summary
Scenario	Expected Validation	Actual Result	Status
Invalid Bearer token	Authentication rejection	404 Not Found	BLOCKED
Missing Authorization	Authentication rejection	404 Not Found	BLOCKED
Empty JSON {}	Required-field validation	404 Not Found	BLOCKED
Empty message	Input validation	404 Not Found	BLOCKED
Invalid JSON	JSON validation error	404 Not Found	BLOCKED
Integration Blocker

The main blocker identified during Task 24 is the unavailable healthcare chat endpoint:

/api/ai/chat

All negative scenarios targeting this endpoint returned:

HTTP 404

with:

{
  "detail": "Not Found"
}

Because the route was not available, the tests could not reach the authentication or request-validation logic.

PowerShell Environment Finding

During the test execution, PowerShell/PSReadLine generated:

System.ArgumentOutOfRangeException

The error occurred while rendering/editing the PowerShell console input.

The API requests that were successfully executed after the console errors still returned clear HTTP responses.

This was treated as a local terminal interaction issue rather than an API result.

Findings
ID	Finding	Severity	Status	Responsible Team
F-24-01	Healthcare /api/ai/chat route returns 404	High	Open / Blocking	AI / Backend
F-24-02	Authentication validation could not be reached	High	Blocked by F-24-01	AI / Backend
F-24-03	Required-field validation could not be reached	Medium	Blocked by F-24-01	AI / Backend
F-24-04	Invalid JSON handling could not be reached	Medium	Blocked by F-24-01	AI / Backend
Developer Action Required
AI / Backend Team
Confirm the correct deployed healthcare chat route.
Expose the healthcare chat endpoint in the SQA environment.
Confirm the expected authentication contract.
Confirm the required request fields.
Provide the expected error responses for unauthorized and invalid requests.
Retest Plan

After the healthcare chat endpoint becomes available, repeat:

1. Valid healthcare chat request
2. Invalid Bearer token
3. Missing Authorization header
4. Empty JSON body
5. Missing required fields
6. Empty message
7. Invalid JSON

The retest should verify the actual HTTP status and response body for each scenario.

Final SQA Status

Overall Status: BLOCKED

The deployed service itself was reachable and returned HTTP 200 from the root endpoint.

However, the healthcare chat endpoint required for the negative patient scenarios returned HTTP 404.
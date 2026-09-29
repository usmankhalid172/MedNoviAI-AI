# Task 26 – Final Release Candidate E2E Walkthrough Report

**Assignee:** Joyce Hany  
**Role:** End-to-End Flow QA  
**Branch:** `feature/sprint1-flow-simulation-joyce`  
**Task:** Day 26 – Final Release Candidate E2E Walkthrough  
**Date:** 29 September 2026

---

## 1. Objective

The objective of Task 26 was to perform a final Release Candidate end-to-end walkthrough across the available deployed system, verify the exposed AI healthcare routes, validate the deployed financial-health service, check the required ML model, and execute the full automated regression suite.

---

## 2. Test Environment

- Repository: `MedNoviAI-AI`
- Branch: `feature/sprint1-flow-simulation-joyce`
- Deployment: `https://mednoviai-ai.onrender.com/`
- Test execution environment: Windows PowerShell
- Automated test command: `python -m pytest -q`

---

## 3. Git State

The test was executed on the required QA branch:

`feature/sprint1-flow-simulation-joyce`

Final Git status:

- Branch is up to date with the remote branch.
- Working tree is clean.
- No uncommitted changes were present.

**Result: PASS**

---

## 4. Deployment Availability

The deployed root endpoint returned:

- HTTP Status: `200`
- Service: `MedNoviAI AI Service`
- Mounted route reported by the service:
  `/api/ai/financial-health/{user_id}`

This confirms that the deployed service was reachable during the Release Candidate walkthrough.

**Result: PASS**

---

## 5. OpenAPI Route Verification

The deployed `/openapi.json` endpoint returned HTTP `200`.

The following routes were checked:

| Route | Result |
|---|---|
| `/api/ai/chat` | NOT FOUND |
| `/api/ai/intake` | NOT FOUND |
| `/api/ai/financial-health` | FOUND |

The required healthcare Chat and Intake routes were not present in the deployed OpenAPI specification.

**Result: BLOCKED for Healthcare E2E**

---

## 6. Healthcare Chat Endpoint

The endpoint:

`GET /api/ai/chat`

returned:

`HTTP 404`

This confirms that the expected healthcare Chat route was not available on the deployed service during the test.

Because the Chat endpoint was unavailable, the Chat portion of the required patient journey could not be executed end-to-end.

**Result: FAIL / BLOCKED**

---

## 7. Healthcare Intake Endpoint

The endpoint:

`GET /api/ai/intake`

returned:

`HTTP 404`

The Intake route was also absent from the deployed OpenAPI specification.

Therefore, the Intake stage of the intended patient flow could not be executed against the deployed Release Candidate.

**Result: FAIL / BLOCKED**

---

## 8. Financial Health Endpoint

The deployed financial-health endpoint was tested with two different user IDs:

- `test-user-001`
- `random-user-999`

Both requests returned structured financial-health responses.

The response included:

- Score: `76.0`
- Status: `Good`
- Income: `150000.0`
- Expenses: `108500.0`
- Budget status: `Over Budget`
- Expense growth: `17.93`
- Factor scores
- Financial insights

The two different user IDs returned the same observed response values.

This confirms endpoint availability, but the identical response for different user identifiers requires clarification to determine whether the endpoint is intentionally using demo/mock data or whether user-specific data is expected.

**Result: PASS for availability; NEEDS INVESTIGATION for user-specific behavior**

---

## 9. ML Model Availability

The expected model file:

`model\expense_categorization_pipeline.pkl`

was not present in the working tree.

The test explicitly reported:

`MODEL MISSING: model\expense_categorization_pipeline.pkl`

This missing artifact directly affected the automated expense-categorization tests.

**Result: FAIL**

---

## 10. Full Regression Test Results

The full regression suite was executed using:

```text
python -m pytest -q

Final result:

61 passed
8 failed
8 errors
4 skipped
Execution time: 5.20 seconds

The failures and errors were associated with the missing:

model\expense_categorization_pipeline.pkl

The affected tests raised FileNotFoundError when attempting to initialize or load the expense categorization model.

Affected areas included:

Expense integration readiness
Confidence-threshold behavior
Prediction finalization
Expense prediction service
Input validation tests dependent on model initialization

Result: FAIL

11. Console/Test Execution Note

A PSReadLine System.ArgumentOutOfRangeException occurred while entering part of the OpenAPI discovery command.

The error was related to PowerShell console rendering/cursor handling. The OpenAPI test was subsequently executed successfully and produced the expected route discovery results.

Therefore, this console rendering issue was not treated as an application failure.

12. E2E Walkthrough Assessment

The Release Candidate walkthrough verified that:

The deployed service was reachable.
The OpenAPI specification was accessible.
The financial-health endpoint was exposed and returned structured data.
The expected healthcare Chat endpoint was not exposed.
The expected healthcare Intake endpoint was not exposed.
The ML model required by the expense-categorization components was missing.
The full regression suite contained 61 passing tests but also 8 failures and 8 errors caused by the missing model artifact.

Because the healthcare Chat and Intake routes were unavailable, the complete intended healthcare patient journey could not be demonstrated against the deployed Release Candidate.

13. Findings
Finding 1 – Healthcare Chat route unavailable

Severity: High / Integration Blocker

/api/ai/chat was not found in OpenAPI and returned HTTP 404.

Impact: The healthcare Chat stage of the patient E2E journey cannot be executed against the deployed service.

Finding 2 – Healthcare Intake route unavailable

Severity: High / Integration Blocker

/api/ai/intake was not found in OpenAPI and returned HTTP 404.

Impact: The Intake stage of the patient E2E journey cannot be executed against the deployed service.

Finding 3 – ML model artifact missing

Severity: High

model\expense_categorization_pipeline.pkl was missing.

Impact: Eight automated tests failed and eight tests errored because the required model could not be loaded.

Finding 4 – Identical financial-health response for different user IDs

Severity: Medium / Needs Investigation

Two different user IDs returned the same observed financial-health response.

Impact: It is not possible from this test alone to determine whether this is expected demo/mock behavior or whether user-specific data handling requires further verification.

14. Overall Result

Overall Status: BLOCKED

The deployed Release Candidate was reachable and the financial-health service was available. However, the intended healthcare E2E journey could not be completed because the expected Chat and Intake routes were not exposed on the deployed service.

In addition, the full regression suite reported 8 failures and 8 errors caused by the missing expense categorization model artifact.

15. Recommended Follow-up
Expose and deploy the required healthcare Chat endpoint:
/api/ai/chat
Expose and deploy the required healthcare Intake endpoint:
/api/ai/intake
Verify the intended request/response contracts for both healthcare endpoints.
Restore or correctly provide the required ML model artifact:
model\expense_categorization_pipeline.pkl
Re-run the full regression suite after the model is available.
Re-test the financial-health endpoint with multiple user IDs and confirm whether identical responses are expected for the current demo environment.
Perform another complete patient E2E walkthrough after the healthcare routes are available.
16. Evidence Summary
Area	Result
QA branch	PASS
Git working tree	PASS
Deployment availability	PASS
OpenAPI availability	PASS
Healthcare Chat route	BLOCKED
Healthcare Intake route	BLOCKED
Financial Health availability	PASS
Different user-ID behavior	NEEDS INVESTIGATION
ML model availability	FAIL
Automated regression	FAIL
Final Release Candidate E2E	BLOCKED
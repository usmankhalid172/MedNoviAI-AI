# Task 25 — Full Regression Verification & Fix Validation

**Assignee:** Joyce Hany  
**Role:** End-to-End Flow QA  
**Branch:** `feature/sprint1-flow-simulation-joyce`  
**PR Title:** `Task-day25-flow-simulation-joycehany`

---

## Objective

Execute a full regression walkthrough to verify that existing functionality remains stable and to identify any remaining failures or integration gaps after recent development changes.

The regression verification covered:

- Git branch and worktree state
- Deployed service availability
- OpenAPI route discovery
- Healthcare Chat endpoint
- Healthcare Intake endpoint
- Financial Health endpoint
- ML model file availability
- Automated pytest regression suite

---

# 1. Branch and Worktree Verification

### Command

```text
git branch --show-current
git status --short

Result

The active branch was:

feature/sprint1-flow-simulation-joyce

The worktree had no uncommitted changes.

Status

PASS

2. Deployment Root Verification
Endpoint
https://mednoviai-ai.onrender.com/
Result

HTTP status:

200

The deployed service returned:

{
  "service": "MedNoviAI AI Service",
  "message": "Financial Health Score API is mounted.",
  "route": "/api/ai/financial-health/{user_id}"
}
Status

PASS

Finding

The deployed AI service is reachable.

3. OpenAPI Route Discovery

The deployed OpenAPI specification was requested successfully.

Result

HTTP status:

200

The following route checks were performed:

Route	Result
/api/ai/chat	NOT FOUND
/api/ai/intake	NOT FOUND
/api/ai/financial-health	FOUND
/api/ai	FOUND
Status

PARTIAL / BLOCKED

Finding

The healthcare Chat and Intake routes are not exposed in the deployed OpenAPI specification.

4. Healthcare Chat Endpoint
Endpoint
/api/ai/chat
Result

HTTP:

404
Status

BLOCKED

Finding

The healthcare Chat endpoint is not available on the tested deployment.

5. Healthcare Intake Endpoint
Endpoint
/api/ai/intake
Result

HTTP:

404
Status

BLOCKED

Finding

The healthcare Intake endpoint is not available on the tested deployment.

6. Financial Health Endpoint
Valid User Test

Endpoint:

/api/ai/financial-health/test-user-001
Result

HTTP:

200

The endpoint returned a structured Financial Health response including:

score
status
income
expenses
saving rate
expense ratio
budget utilization
cash flow
budget status
expense growth
factor scores
insights
Status

PASS

7. Financial Health Different-User Regression Check

A different user ID was tested:

/api/ai/financial-health/random-user-999
Result

HTTP:

200

The response values matched the previously tested user response.

Status

PASS — Endpoint Availability

Finding

The endpoint is available for different user IDs, but the repeated identical response data should be reviewed by the responsible development team to confirm whether the current implementation intentionally uses demo/mock data.

This finding is not classified as a confirmed defect based on the available test evidence.

8. ML Model File Verification
Expected File
model\expense_categorization_pipeline.pkl
Result
MODEL MISSING: model\expense_categorization_pipeline.pkl
Status

FAIL

Finding

The expected expense categorization model file is missing from the local working tree.

9. Automated Pytest Regression
Command
python -m pytest -q
Result
61 passed
8 failed
8 errors
4 skipped
Overall Status

FAIL

The regression suite did not complete successfully.

10. Regression Failure Analysis

The observed failures and errors were associated with the missing model file:

model\expense_categorization_pipeline.pkl

The affected tests included:

tests/test_integration_readiness.py
tests/test_prediction_finalizer.py
tests/test_prediction_service.py

The failures occurred when the application attempted to load the missing model.

Representative error:

FileNotFoundError:
Model file not found:
C:\Users\JoJo\PycharmProjects\MedNoviAI-AI\model\expense_categorization_pipeline.pkl
Impact

Expense categorization functionality cannot be fully regression-tested while the required model artifact is missing.

11. PowerShell / Test Execution Note

During the initial OpenAPI command entry, PowerShell reported a PSReadLine console rendering exception.

The exception was related to console cursor/buffer rendering:

System.ArgumentOutOfRangeException:
The value must be greater than or equal to zero and less than the console's buffer size

The command was subsequently executed successfully and the OpenAPI checks completed.

Classification

Environment / Console Issue

This was not treated as an application regression defect.

Regression Summary
Area	Result
Git Branch	PASS
Git Worktree	PASS
Deployment Root	PASS
OpenAPI Availability	PASS
Healthcare Chat	BLOCKED
Healthcare Intake	BLOCKED
Financial Health	PASS
Different User Financial Health	PASS — availability verified
ML Model File	FAIL
Pytest Regression	FAIL
Overall Regression	FAIL / BLOCKED
Regression Findings
F-25-01 — Missing Expense Categorization Model

Severity: High

Status: Open

Evidence:

model\expense_categorization_pipeline.pkl

was not present.

Impact:

Multiple expense categorization tests fail during model initialization or prediction.

Required Action:

Restore/provide the expected model artifact or update the implementation/test configuration to use the correct model location.

F-25-02 — Healthcare Chat Endpoint Not Exposed

Severity: High

Status: Open / Blocking

Evidence:

/api/ai/chat → HTTP 404

Impact:

Healthcare patient-chat functionality cannot be verified through the deployed service.

Required Action:

Expose and verify the expected healthcare Chat endpoint in the deployed environment.

F-25-03 — Healthcare Intake Endpoint Not Exposed

Severity: High

Status: Open / Blocking

Evidence:

/api/ai/intake → HTTP 404

Impact:

Healthcare intake parsing cannot be verified through the deployed service.

Required Action:

Expose and verify the expected healthcare Intake endpoint.

Developer Action Required
AI Team
Verify healthcare Chat endpoint deployment.
Verify healthcare Intake endpoint deployment.
Confirm the expected healthcare API routes.
ML / AI Integration Team
Restore or correctly provide the required expense categorization model artifact.
Re-run affected expense categorization tests.
.NET / Integration Team
Confirm the expected healthcare API contracts and deployed routes.
Retest Plan

After the identified issues are addressed, rerun:

1. OpenAPI route discovery
2. Healthcare Chat endpoint test
3. Healthcare Intake endpoint test
4. Financial Health endpoint regression
5. ML model file verification
6. Full pytest regression
7. Complete E2E patient/doctor walkthrough

The regression suite should be considered stable only after the previously failing tests are retested successfully.
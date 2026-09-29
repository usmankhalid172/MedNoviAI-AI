# Task 28 – Final MVP Smoke Test Report

**Assignee:** Joyce Hany  
**Role:** End-to-End Flow QA  
**Branch:** `feature/sprint1-flow-simulation-joyce`  
**Task:** Final MVP Smoke Test  
**Date:** 30 September 2026

---

## 1. Objective

The objective of this task was to perform a final MVP smoke test across the available primary system workflows and verify the deployed service, healthcare routes, financial-health functionality, required ML model availability, and the automated test suite.

---

## 2. Test Environment

- Repository: `MedNoviAI-AI`
- Branch: `feature/sprint1-flow-simulation-joyce`
- Deployment: `https://mednoviai-ai.onrender.com/`
- Test environment: Windows PowerShell
- Automated test command:

```text
python -m pytest -q

3. Git Branch and Working Tree

The smoke test was executed on:

feature/sprint1-flow-simulation-joyce

The final Git status showed the branch was clean with no uncommitted changes.

Result: PASS

4. Deployment Availability

The deployed root endpoint returned:

HTTP: 200

The service response identified the deployed service as:

MedNoviAI AI Service

and reported the mounted route:

/api/ai/financial-health/{user_id}

This confirms that the deployed service was reachable during the MVP smoke test.

Result: PASS

5. OpenAPI Availability

The deployed OpenAPI specification was successfully loaded.

HTTP: 200
OpenAPI loaded successfully

Result: PASS

6. Healthcare Chat Route

The expected healthcare Chat route:

/api/ai/chat

was not found in the deployed OpenAPI specification.

A direct request to:

/api/ai/chat

returned:

HTTP: 404

Therefore, the healthcare Chat workflow could not be executed against the deployed MVP service.

Result: BLOCKED

7. Healthcare Intake Route

The expected healthcare Intake route:

/api/ai/intake

was not found in the deployed OpenAPI specification.

A direct request to:

/api/ai/intake

returned:

HTTP: 404

Therefore, the healthcare Intake workflow could not be executed against the deployed MVP service.

Result: BLOCKED

8. Financial Health Route

The deployed Financial Health route was found in OpenAPI:

/api/ai/financial-health/{user_id}

A request using:

test-user-001

returned a structured financial-health response.

Observed response data included:

Expense ratio: 72.33
Budget utilization: 105.34
Cash flow: 41500.0
Budget status: Over Budget
Expense growth: 17.93
Factor scores
Financial insights

The endpoint was therefore available and returning structured data.

Result: PASS

9. Required ML Model

The required expense categorization model:

model\expense_categorization_pipeline.pkl

was checked during the smoke test.

The result was:

MISSING: model\expense_categorization_pipeline.pkl

The model was therefore not available in the current working tree.

Result: FAIL

10. Healthcare Source Route Search

The source code was searched for the expected healthcare routes:

/api/ai/chat
/api/ai/intake

No matching route implementation was returned by the source search.

This is consistent with the deployed OpenAPI result where both healthcare routes were not found.

Result: BLOCKED

11. Full Automated Test Suite

The complete automated test suite was executed using:

python -m pytest -q

Final result:

8 failed, 61 passed, 4 skipped, 8 errors in 6.11s
Test Summary
Result	Count
Passed	61
Failed	8
Errors	8
Skipped	4

The reported failures and errors were related to the missing ML model:

model\expense_categorization_pipeline.pkl

Multiple tests raised FileNotFoundError while attempting to initialize or load the expense categorization model.

Affected test areas included:

Expense integration readiness
Confidence threshold behavior
Prediction finalizer
Expense prediction service
Input validation tests dependent on model initialization

Result: FAIL

12. Main Findings
Finding 1 – Healthcare Chat endpoint unavailable

The expected:

/api/ai/chat

route was not present in OpenAPI and returned HTTP 404.

Impact: The Chat stage of the intended healthcare workflow could not be smoke-tested on the deployed MVP.

Finding 2 – Healthcare Intake endpoint unavailable

The expected:

/api/ai/intake

route was not present in OpenAPI and returned HTTP 404.

Impact: The Intake stage of the intended healthcare workflow could not be smoke-tested on the deployed MVP.

Finding 3 – Required ML model is missing

The required file:

model\expense_categorization_pipeline.pkl

was missing.

Impact: Model-dependent automated tests could not complete successfully.

Finding 4 – Automated regression suite contains failures

The complete test suite finished with:

61 passed
8 failed
4 skipped
8 errors

The failures and errors were associated with the missing ML model artifact.

Impact: The current repository state does not produce a fully passing automated test suite.

13. MVP Smoke Test Assessment

The smoke test confirmed that the deployed service is reachable and that the Financial Health functionality is exposed and returning structured responses.

However, the complete intended healthcare MVP workflow could not be verified because the expected Chat and Intake routes were unavailable on the deployed service.

The automated test suite also remains partially blocked by the missing expense categorization model.

14. Overall Result

Overall Status: BLOCKED

The MVP smoke test successfully verified deployment availability, OpenAPI availability, and Financial Health endpoint availability.

The primary healthcare Chat and Intake workflows could not be completed because their expected deployed routes were unavailable.

The automated test suite also reported failures and errors caused by the missing ML model artifact.

15. Recommended Follow-up
Deploy and expose the required healthcare Chat route:
/api/ai/chat
Deploy and expose the required healthcare Intake route:
/api/ai/intake
Verify the request and response contracts for both healthcare routes.
Restore or provide the required ML model:
model\expense_categorization_pipeline.pkl
Re-run the complete automated test suite after the model is available.
Re-run the final MVP smoke test after the healthcare routes are deployed.
Verify the complete intended patient journey from Chat through Intake and the downstream workflow.
16. Evidence Summary
Area	Result
QA branch	PASS
Git working tree	PASS
Deployment availability	PASS
OpenAPI availability	PASS
Healthcare Chat route	BLOCKED
Healthcare Intake route	BLOCKED
Financial Health route	PASS
Required ML model	FAIL
Automated test suite	FAIL
Final MVP smoke test	BLOCKED
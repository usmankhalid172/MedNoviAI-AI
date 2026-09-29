
# Task 27 – Final MVP Smoke Test Report

**Assignee:** Joyce Hany  
**Role:** End-to-End Flow QA  
**Branch:** `feature/sprint1-flow-simulation-joyce`  
**Task:** Day 27 – Final MVP Smoke Test  
**Date:** 30 September 2026

---

## 1. Objective

The objective of Task 27 was to perform the final MVP smoke test across the primary deployed workflows and verify the current availability of the main AI services and automated test suite.

---

## 2. Test Environment

- Repository: `MedNoviAI-AI`
- Branch: `feature/sprint1-flow-simulation-joyce`
- Deployment: `https://mednoviai-ai.onrender.com/`
- Test environment: Windows PowerShell
- Automated test command: `python -m pytest -q`

---

## 3. Git State

The smoke test was executed on the required QA branch:

`feature/sprint1-flow-simulation-joyce`

The final Git status showed:

- Branch is up to date with the remote branch.
- Working tree is clean.
- No uncommitted changes were present.

**Result: PASS**

---

## 4. Deployment Availability

The deployed root endpoint returned:

- HTTP Status: `200`
- Service: `MedNoviAI AI Service`
- Mounted route:
  `/api/ai/financial-health/{user_id}`

This confirms that the deployed MVP service was reachable during the smoke test.

**Result: PASS**

---

## 5. OpenAPI Smoke Check

The deployed `/openapi.json` endpoint returned HTTP `200`.

The available AI route discovered in the deployed OpenAPI specification was:

`/api/ai/financial-health/{user_id}`

The expected healthcare routes were not present:

- `/api/ai/chat`
- `/api/ai/intake`

**Result: PASS for OpenAPI availability; Healthcare routes unavailable**

---

## 6. Healthcare Chat Smoke Test

The endpoint:

`GET /api/ai/chat`

returned:

`HTTP 404`

Therefore, the healthcare Chat workflow could not be executed against the deployed MVP.

**Result: BLOCKED**

---

## 7. Healthcare Intake Smoke Test

The endpoint:

`GET /api/ai/intake`

returned:

`HTTP 404`

Therefore, the healthcare Intake workflow could not be executed against the deployed MVP.

**Result: BLOCKED**

---

## 8. Financial Health Smoke Test

The deployed financial-health endpoint was tested with two user IDs:

- `test-user-001`
- `random-user-999`

Both requests returned:

`HTTP 200`

The responses included structured financial-health information such as:

- Expense ratio
- Budget utilization
- Cash flow
- Budget status
- Expense growth
- Factor scores
- Financial insights

The observed values were the same for both tested user IDs.

This smoke test confirms endpoint availability. The identical response behavior should be clarified separately if user-specific financial data is expected.

**Result: PASS for endpoint availability; NEEDS INVESTIGATION for user-specific behavior**

---

## 9. ML Model / Expense Categorization Check

The expected model file is:

`model\expense_categorization_pipeline.pkl`

The smoke-test command encountered a PowerShell `else` parsing issue while checking the file, so that specific shell check did not produce a clean model-status message.

However, the subsequent automated tests confirmed that the model file was unavailable.

Multiple tests raised:

`FileNotFoundError: Expense categorization model not found`

for:

`model\expense_categorization_pipeline.pkl`

**Result: FAIL**

---

## 10. Full Automated Smoke Test

The full test suite was executed using:

```text
python -m pytest -q

Final result:

61 passed
8 failed
8 errors
4 skipped
Execution time: 5.22 seconds

The failures and errors were associated with the missing expense categorization model.

Affected areas included:

Expense integration readiness
Confidence-threshold behavior
Prediction finalization
Expense prediction service
Input validation tests dependent on model initialization

Result: FAIL

11. PowerShell Test-Script Note

During the ML model check, PowerShell reported:

else : The term 'else' is not recognized as the name of a cmdlet...

This was caused by the way the conditional block was entered into the interactive PowerShell session.

It was treated as a test-script/console execution issue rather than an application defect.

The automated pytest results independently confirmed that the expected model file was missing.

12. Primary Workflow Smoke-Test Summary
Workflow / Area	Result
QA branch	PASS
Git working tree	PASS
Deployment availability	PASS
OpenAPI availability	PASS
Healthcare Chat	BLOCKED
Healthcare Intake	BLOCKED
Financial Health endpoint	PASS
Different user-ID behavior	NEEDS INVESTIGATION
Expense categorization model	FAIL
Automated regression/smoke tests	FAIL
Final MVP Smoke Test	BLOCKED
13. Findings
Finding 1 – Healthcare Chat route unavailable

Severity: High / Integration Blocker

The deployed OpenAPI specification did not contain /api/ai/chat, and the endpoint returned HTTP 404.

Impact: The healthcare Chat workflow cannot be smoke-tested on the deployed MVP.

Finding 2 – Healthcare Intake route unavailable

Severity: High / Integration Blocker

The deployed OpenAPI specification did not contain /api/ai/intake, and the endpoint returned HTTP 404.

Impact: The healthcare Intake workflow cannot be smoke-tested on the deployed MVP.

Finding 3 – Expense categorization model unavailable

Severity: High

The automated test suite reported FileNotFoundError for:

model\expense_categorization_pipeline.pkl

Impact: Eight tests failed and eight tests errored because the required model could not be loaded.

Finding 4 – Same financial-health response observed for two user IDs

Severity: Medium / Needs Investigation

Both tested user IDs returned the same observed financial-health values.

Impact: Further clarification is required to determine whether the current MVP intentionally uses demo/mock data or whether user-specific financial data is expected.

14. Overall Result

Overall Status: BLOCKED

The deployed MVP was reachable and the Financial Health endpoint was available. However, the primary healthcare Chat and Intake workflows could not be smoke-tested because their expected deployed routes were unavailable.

The automated test suite also reported failures and errors caused by the missing expense categorization model.

Therefore, the final MVP smoke test did not achieve a fully executable primary healthcare workflow.

15. Recommended Follow-up
Deploy and expose the required healthcare Chat endpoint:
/api/ai/chat
Deploy and expose the required healthcare Intake endpoint:
/api/ai/intake
Verify the request/response contracts for the healthcare endpoints.
Restore or correctly provide:
model\expense_categorization_pipeline.pkl
Re-run the full automated test suite after the model is available.
Verify whether the Financial Health endpoint is expected to return demo/mock data for different user IDs.
Repeat the final MVP smoke test after the blocked workflows and missing model are resolved.
16. Evidence Summary
Area	Evidence
Branch	feature/sprint1-flow-simulation-joyce
Deployment	HTTP 200
OpenAPI	HTTP 200
Healthcare Chat	HTTP 404
Healthcare Intake	HTTP 404
Financial Health User 1	HTTP 200
Financial Health User 2	HTTP 200
Pytest	61 passed, 8 failed, 8 errors, 4 skipped
Final Git status	Clean
Final MVP status	BLOCKED
# PR #9 — Anomaly Detection QA Evidence

## PR Details
- PR: #9
- Title: Feature/annanomaly detection
- Author: jaffar066
- Head branch: feature/annanomaly_detection
- Tested commit: ec8604f
- QA branch: feature/sprint1-ai-qa-isma
- Review result: Changes requested

## Scope
Reviewed the anomaly detection endpoint and production service against the Day 12 anomaly validation/reference cases included in the PR.

## Tests Performed

### 1. Existing anomaly integration test
Command:
`python -m pytest -q .\tests\test_integration_api.py -k anomaly`

Result:
- 1 passed
- 5 deselected
- 1 warning

The existing test verifies HTTP 200, user_id, and that anomalies is a list.

### 2. Full pytest suite
Command:
`python -m pytest -q`

Result:
- Test collection stopped because `requests` is not installed.
- `requests` is not listed in `requirements.txt`.

This was recorded as a repository test-environment/dependency issue rather than the primary reason for the PR review result.

### 3. Endpoint verification
Using the intended application entry point `src.main:app`:
- `GET /api/v1/anomalies/U4637`
- Authenticated request returned HTTP 200.
- Response contained structured anomaly records.
- Unauthenticated request returned HTTP 401.
- `analysis_days=0` returned HTTP 422.

### 4. DS-02 controlled test
A controlled dataset was used to compare the implementation with the documented category-baseline rule.

The reference validation defines DS-02 as:
`Single expense at least 2x category baseline`

The Python implementation calculates the unusual-amount baseline using the overall user's expense average rather than the category average.

### 5. DS-03 / DS-04 / DS-05 implementation check
The Day 12 validation defines:
- DS-03: Category spike between 20% and 49.99%
- DS-04: Category spike at least 50%
- DS-05: Category at least 2x historical baseline

The production Python anomaly service does not contain corresponding category-growth or historical-category-baseline logic.

### 6. DS-06 duplicate check
The reference validation uses:
- User
- Amount
- Category
- Date
- Normalized description

The Python implementation instead requires matching user, amount, category, merchant/description and timestamps within 60 seconds.

Therefore the duplicate-detection methodology does not match the documented validation criteria.

## Additional Observation
The anomaly service uses `datetime.utcnow()`, which produced a Python 3.14 deprecation warning during testing.

## Review Findings
Changes were requested because the production implementation does not fully match the documented Day 12 anomaly validation methodology, particularly DS-02 through DS-06.

The current automated anomaly test also does not validate the six documented scenarios.

## Future QA Task
Re-test PR #9 after the author updates the implementation/tests. Re-review the PR only after the updated commit is available.

## Evidence Status
QA review completed for the current PR #9 commit. No merge performed.

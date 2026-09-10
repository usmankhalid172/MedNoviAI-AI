# Task Report — API + Mobile/Web Integration (Financial Health Score, Day 10)

**Task:** Subtask of AIML-day-10-Task
**Assignee:** Laiba
**Status:** Completed (blocked on one upstream item — see Notes)

---

## Summary

Built the integration layer that sits between the `GET /api/ai/financial-health/{userId}`
endpoint (Omesh's `financial_health_router.py`) and the mobile/web client. This layer
calls the API, handles every response state (success, 404, 501, network failure), and
converts the raw JSON into the exact score + factor-level + AI Insight structure
described in Section 18 of the spec.

## Implementation Details

**1. API Call** — `fetch_financial_health(user_id)` calls the endpoint and raises a
typed `FinancialHealthAPIError(status_code, detail)` on any non-200 response.

**2. Response Handling** — `handle_api_error()` maps backend states to safe UI states:
- `404` → "No financial data yet"
- `501` → "Not available yet" (today's actual state — see Notes)
- network failure → "You're offline"
- anything else → generic error state

**3. Score/Status Display** — `build_display_payload()` produces the header block
(`score`, `scoreDisplay`, `status`) directly from the API's `score`/`status` fields.

**4. Factor-Level Strengths/Weaknesses** — Derived a label (Strong/Good/Fair/Needs
Attention, etc.) for each of the six factors from the raw values the API returns
(`savingRate`, `expenseRatio`, `budgetStatus`, `cashFlow`, `expenseGrowth`), using the
same threshold bands as the spec's own scoring tables (Sections 5, 6, 10) so the label
a user sees always agrees with the score they got.

**5. AI Insight** — Surfaced as both a single joined string (`aiInsight`) and the raw
list (`insightsList`), so mobile/web can render it as one paragraph or as bullet points.

**6. Single Entry Point** — `get_financial_health_for_ui(user_id)` is the only function
the client needs to call; it always returns `{"ok": bool, ...}` so the UI never has to
catch exceptions itself.

## Files

- `financial_health_integration.py` — API client, error handling, display-payload builder
- `test_financial_health_integration.py` — test suite for the shared testing checklist

## Testing (shared "Everyone" checklist)

All 9 required scenarios were tested against the real scoring engine, plus 2 extra
cases for API error handling. **11/11 passed.**

| # | Scenario | Result | Notes |
|---|----------|--------|-------|
| 1 | Normal financial data | Pass | Matches spec's Section 11 worked example exactly |
| 2 | Zero income | Pass | No division-by-zero; degrades to 0% cleanly |
| 3 | No transactions | Pass | Returns score 0 / "Poor" / explicit "no data" insight |
| 4 | No budget | Pass | Budget factor excluded and weight redistributed, not zeroed |
| 5 | Negative cash flow | Pass | Correctly labeled "Negative" |
| 6 | Large transactions | Pass | Tested at 50M scale — no overflow/precision issues |
| 7 | Duplicate transactions | Pass* | *See note below — not this layer's responsibility |
| 8 | Missing/invalid categories | Pass | Category isn't used by any of the 6 scoring factors, confirmed no effect |
| 9 | User-data isolation | Pass* | *See note below — enforced upstream, not by scoring math |
| — | API returns 404 | Pass | Maps to "no data" UI state |
| — | API returns 501 | Pass | Maps to "not ready" UI state (today's real backend state) |

## Notes — Items to raise with the team lead / Omesh

1. **Blocking dependency:** The live endpoint currently returns `501` for every request,
   because `get_user_financial_data()` in `financial_health_router.py` is a placeholder
   (`raise NotImplementedError`) — the DB layer isn't wired in yet. This integration
   layer is fully built and tested against the scoring engine directly, but it **cannot
   be tested against a live 200 response** until that's connected. Recommend flagging
   this as the critical-path item for Day 10 sign-off.

2. **Data gap — Debt/Udhaar cannot be displayed:** Section 18 of the spec expects a
   "Debt/Udhaar — Healthy" line in the UI. `score_debt_udhaar()` computes this label
   internally, but `calculate_financial_health_score()` never includes it in the
   returned dict — it's silently dropped. **The API contract needs a `debtStatus`
   field added** (or the router needs updating to include it) before this factor can
   be shown to users. Currently displayed as "Not Available" as a placeholder.

3. **Data gap — Cash Flow status is approximate:** The spec's cash-flow bands (Strong
   Positive / Positive / Near Zero / Negative) are based on cash flow as a % of income
   (Section 8), but the API only returns the raw `cashFlow` amount — not income, and
   not the status string the backend already computes internally. This layer can only
   infer sign (Positive/Negative), not the correct band. **Recommend the API also
   return `cashFlowStatus`** (already computed server-side, just not exposed) so the
   client shows the verified label rather than an estimate — this also keeps things
   aligned with the spec's Golden Rule (Section 14: no client-side reinterpretation of
   financial figures).

4. **Duplicate-transaction and user-isolation testing** are structurally out of scope
   for this integration layer and the scoring engine — both must be handled at the
   DB aggregation step (`get_user_financial_data()`), which doesn't exist yet (see
   #1). Tests 7 and 9 above document the expected behavior mathematically, but real
   verification needs to happen once that layer is built.

## Team Lead Verification Checklist (self-assessed)

- [x] API is called and every response state (200/404/501/offline) is handled
- [x] Score and status are displayed correctly
- [x] Factor-level strengths/weaknesses shown for all 6 factors (2 marked "Not Available" — see Notes #2, #3)
- [x] AI Insight displayed (both string and list form)
- [x] Output structure is a single, reusable object for both mobile and web
- [x] All 9 shared test scenarios covered and passing
- [ ] Tested against a live 200 response — **blocked until DB layer is connected (Note #1)**

# Day 18 Specialty Data — SQA / Verification Checklist

## Data quality
- [x] JSON is valid UTF-8 and parses successfully.
- [x] Top-level schema is documented.
- [x] Specialty names use a single canonical spelling.
- [x] Keywords are lowercase and whitespace-normalized.
- [x] Duplicate keywords after normalization are rejected.
- [x] Empty keywords are rejected.
- [x] Mapping values are restricted to canonical specialties.
- [x] Emergency overrides are isolated from ordinary keyword routing.
- [x] Required examples include skin rash → Dermatology and chest tightness → Cardiology.

## Safety
- [x] Dataset explicitly states it is a routing aid, not a diagnostic model.
- [x] Emergency-first priority is documented.
- [x] Ambiguous symptoms are acknowledged instead of being represented as diagnostic certainty.
- [x] Core AI endpoints and master `.env` are outside this task's ownership.

## Integration readiness
- [x] JSON is standalone and machine-readable.
- [x] JSON Schema is included.
- [x] API payload examples are provided as documentation-only references.
- [x] A deterministic validation script is included.
- [x] Pytest checks are included.
- [ ] Actual endpoint integration test: **must be executed by the central endpoint owner / integration owner in the repository environment**.
- [ ] Final PR approval: **Syeda Isma Nazir**.

## Release gate
Do not merge until:
1. Validation script passes.
2. Repository CI passes.
3. Endpoint owner confirms the actual endpoint contract and integration.
4. Reviewer approves the PR.

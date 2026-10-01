# PR Description — Task-sept18-specialty-data-tahasajjad

## Summary
Adds a cleaned, standardized symptom-keyword → medical-specialty reference dataset for Day 18 Domain Data Support.

## Included
- `data/symptom_to_specialty.json`
- `data/symptom_to_specialty.schema.json`
- `docs/api_payload_examples.json`
- `docs/verification_sources.md`
- `docs/SQA_CHECKLIST.md`
- `scripts/validate_specialty_mapping.py`
- `tests/test_specialty_mapping.py`
- `README_DAY18_SPECIALTY_DATA_TAHA.md`

## Scope
This PR is data/support only. It does not modify the core AI endpoints, chatbot pipeline, or master environment configuration.

## Safety
Emergency patterns are represented separately and should be evaluated before ordinary specialty routing. The dictionary is not a diagnostic model.

## Validation
Expected:
- mapping integrity validation passes
- pytest passes
- repository CI passes

## Reviewer
Syeda Isma Nazir

## Branch
`feature/sprint1-specialty-data-taha`

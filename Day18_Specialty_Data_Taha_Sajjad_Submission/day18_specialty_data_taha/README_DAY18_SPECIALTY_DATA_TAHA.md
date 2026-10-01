# Day 18 — Specialty Data Support — Taha Sajjad

## Assignment
- Assignee: Taha Sajjad
- Role: Domain Data Support
- Date: 18 September 2026
- Branch: `feature/sprint1-specialty-data-taha`
- PR title: `Task-sept18-specialty-data-tahasajjad`
- Reviewer: Syeda Isma Nazir
- Repository: `usmankhalid172/MedNoviAI-AI`

## Scope completed
This package is intentionally limited to the domain-data/support scope. It does **not** modify or claim ownership of:
- `/api/ai/chat`
- `/api/ai/intake`
- `/api/ai/recommend-specialty`
- chatbot pipeline logic
- master `.env` configuration

## Main deliverable
`data/symptom_to_specialty.json` is the standardized reference dictionary. It contains:
- normalized symptom keywords
- canonical specialty names
- emergency-first override patterns
- normalization rules
- routing policy and ambiguity notes

Current size: **99** primary keyword mappings + **11** emergency override patterns.

## Validation
Run:

```bash
python scripts/validate_specialty_mapping.py
```

Optional pytest:

```bash
pytest -q tests/test_specialty_mapping.py
```

The validation checks normalized keys, duplicate prevention, canonical specialties, routing values, and required examples.

## Important safety boundary
This is a routing/reference dataset, not a diagnostic system. Emergency patterns are separated so downstream routing can check urgent patterns before ordinary specialty matching. Chest-pain and similar emergency-sensitive symptoms should never be treated as proof of a diagnosis.

## Suggested Git workflow

```bash
git checkout -b feature/sprint1-specialty-data-taha
# copy data/, docs/, scripts/, tests/, and this README into the repository
python scripts/validate_specialty_mapping.py
pytest -q tests/test_specialty_mapping.py
git add data docs scripts tests README_DAY18_SPECIALTY_DATA_TAHA.md
git commit -m "Task-sept18-specialty-data-tahasajjad"
git push -u origin feature/sprint1-specialty-data-taha
```

Then open a PR with title:

`Task-sept18-specialty-data-tahasajjad`

Request review from **Syeda Isma Nazir** before merge.

## Evidence and design notes
The mapping is a deterministic reference layer. Symptoms can have multiple plausible specialties, so the file documents that limitation rather than pretending that one keyword is a diagnosis.

External medical-safety references used during review:
- American Heart Association — chest pain / heart-attack warning signs
- NHS — urinary tract infection symptom guidance

See `docs/verification_sources.md`.

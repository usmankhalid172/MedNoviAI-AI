#!/usr/bin/env python3
"""Validate the MedNoviAI symptom-to-specialty reference mapping."""

from pathlib import Path
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "symptom_to_specialty.json"

CANONICAL = {
    "Cardiology", "Dermatology", "Neurology", "Gastroenterology",
    "Pulmonology", "ENT", "Ophthalmology", "Orthopedics", "Urology",
    "Nephrology", "Gynecology", "Endocrinology", "Psychiatry",
    "General Practice", "Pediatrics", "Emergency"
}

def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    value = value.strip().lower()
    return re.sub(r"\s+", " ", value)

def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    mapping = payload["symptom_to_specialty"]
    overrides = payload["emergency_overrides"]

    assert payload["schema_version"] == "1.0.0"
    assert set(payload["canonical_specialties"]) == CANONICAL
    assert mapping, "Mapping cannot be empty"

    normalized = [normalize(k) for k in mapping]
    assert all(normalized), "Blank keyword found"
    assert len(normalized) == len(set(normalized)), "Duplicate keywords after normalization"
    assert all(v in CANONICAL - {"Emergency"} for v in mapping.values())
    assert all(v == "Emergency" for v in overrides.values())
    assert all(k == normalize(k) for k in mapping), "Keywords must already be normalized"
    assert all(k == normalize(k) for k in overrides), "Override keywords must already be normalized"

    print(f"PASS: {len(mapping)} specialty keywords, {len(overrides)} emergency overrides.")
    print("PASS: canonical specialties, normalized keys, and routing targets are valid.")

if __name__ == "__main__":
    main()

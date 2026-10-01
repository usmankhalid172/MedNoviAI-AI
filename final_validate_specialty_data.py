import json
import re
from collections import Counter


FILE_NAME = "symptom_specialty.json"


# ============================================================
# 1. LOAD JSON
# ============================================================

print("=" * 70)
print("FINAL SYMPTOM-TO-SPECIALTY DATA VALIDATION")
print("=" * 70)

try:
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        data = json.load(file)

    print("\n[PASS] JSON file is valid and can be parsed.")

except json.JSONDecodeError as error:
    print("\n[FAIL] Malformed JSON.")
    print(f"       Error: {error}")
    raise SystemExit(1)

except FileNotFoundError:
    print(f"\n[FAIL] File not found: {FILE_NAME}")
    raise SystemExit(1)


# ============================================================
# 2. REQUIRED TOP-LEVEL SECTIONS
# ============================================================

print("\n" + "-" * 70)
print("1. REQUIRED DATA SECTIONS")
print("-" * 70)

required_sections = [
    "schema_version",
    "description",
    "canonical_specialties",
    "normalization",
    "symptom_to_specialty",
    "emergency_overrides",
    "routing_policy",
]

missing_sections = [
    section for section in required_sections
    if section not in data
]

if missing_sections:
    print("[FAIL] Missing sections:")
    for section in missing_sections:
        print(f"       - {section}")
else:
    print("[PASS] All required sections are present.")


# ============================================================
# 3. CHECK DATA TYPES / STRUCTURE
# ============================================================

print("\n" + "-" * 70)
print("2. DATA STRUCTURE")
print("-" * 70)

structure_errors = []

if not isinstance(data.get("canonical_specialties"), list):
    structure_errors.append("canonical_specialties must be a list.")

if not isinstance(data.get("symptom_to_specialty"), dict):
    structure_errors.append("symptom_to_specialty must be an object/dictionary.")

if not isinstance(data.get("emergency_overrides"), dict):
    structure_errors.append("emergency_overrides must be an object/dictionary.")

if not isinstance(data.get("normalization"), dict):
    structure_errors.append("normalization must be an object/dictionary.")

if not isinstance(data.get("routing_policy"), dict):
    structure_errors.append("routing_policy must be an object/dictionary.")

if structure_errors:
    print("[FAIL] Structure problems found:")
    for error in structure_errors:
        print(f"       - {error}")
else:
    print("[PASS] Data structures have the expected types.")


# Stop if critical sections are unavailable
if (
    not isinstance(data.get("canonical_specialties"), list)
    or not isinstance(data.get("symptom_to_specialty"), dict)
    or not isinstance(data.get("emergency_overrides"), dict)
):
    print("\nCannot continue safely because critical data structures are invalid.")
    raise SystemExit(1)


# ============================================================
# 4. CANONICAL SPECIALTIES
# ============================================================

print("\n" + "-" * 70)
print("3. CANONICAL SPECIALTY VALIDATION")
print("-" * 70)

canonical_specialties = data["canonical_specialties"]

duplicate_specialties = [
    specialty
    for specialty, count in Counter(canonical_specialties).items()
    if count > 1
]

empty_specialties = [
    specialty
    for specialty in canonical_specialties
    if not isinstance(specialty, str) or not specialty.strip()
]

if duplicate_specialties:
    print("[FAIL] Duplicate canonical specialties:")
    for specialty in duplicate_specialties:
        print(f"       - {specialty}")
else:
    print("[PASS] No duplicate canonical specialties.")

if empty_specialties:
    print("[FAIL] Empty/invalid canonical specialties:")
    for specialty in empty_specialties:
        print(f"       - {repr(specialty)}")
else:
    print("[PASS] No empty canonical specialties.")


canonical_set = set(canonical_specialties)


# ============================================================
# 5. SYMPTOM KEY VALIDATION
# ============================================================

print("\n" + "-" * 70)
print("4. SYMPTOM KEY VALIDATION")
print("-" * 70)

symptom_map = data["symptom_to_specialty"]

malformed_keys = []
empty_keys = []
whitespace_keys = []
suspicious_keys = []

for key in symptom_map:

    # Empty key
    if not isinstance(key, str) or not key.strip():
        empty_keys.append(repr(key))
        continue

    # Leading/trailing whitespace
    if key != key.strip():
        whitespace_keys.append(key)

    # Newline/tab characters
    if "\n" in key or "\r" in key or "\t" in key:
        malformed_keys.append(key)

    # Repeated internal whitespace
    if re.search(r"\s{2,}", key):
        suspicious_keys.append(key)

if empty_keys:
    print("[FAIL] Empty symptom keys found:")
    for key in empty_keys:
        print(f"       - {key}")
else:
    print("[PASS] No empty symptom keys.")

if whitespace_keys:
    print("[FAIL] Keys contain leading/trailing whitespace:")
    for key in whitespace_keys:
        print(f"       - {repr(key)}")
else:
    print("[PASS] No leading/trailing whitespace.")

if malformed_keys:
    print("[FAIL] Keys contain newline/tab characters:")
    for key in malformed_keys:
        print(f"       - {repr(key)}")
else:
    print("[PASS] No newline/tab characters in symptom keys.")

if suspicious_keys:
    print("[WARNING] Keys contain repeated internal whitespace:")
    for key in suspicious_keys:
        print(f"          - {repr(key)}")
else:
    print("[PASS] No repeated internal whitespace.")


# ============================================================
# 6. NORMALIZED DUPLICATE CHECK
# ============================================================

print("\n" + "-" * 70)
print("5. NORMALIZED DUPLICATE KEY CHECK")
print("-" * 70)


def normalize_keyword(keyword):
    """
    Match the dataset's declared normalization rules:
    - case insensitive
    - trim whitespace
    - collapse internal whitespace
    """
    return " ".join(keyword.strip().lower().split())


normalized_keys = {}
normalized_duplicates = []

for key in symptom_map:

    normalized = normalize_keyword(key)

    if normalized in normalized_keys:
        normalized_duplicates.append(
            (key, normalized_keys[normalized], normalized)
        )
    else:
        normalized_keys[normalized] = key


if normalized_duplicates:
    print("[FAIL] Duplicate keys after normalization:")

    for current, previous, normalized in normalized_duplicates:
        print(f"       - {repr(previous)}")
        print(f"         {repr(current)}")
        print(f"         Normalized form: {repr(normalized)}")

else:
    print("[PASS] No duplicate normalized symptom keys found.")


# ============================================================
# 7. SPECIALTY REFERENCE VALIDATION
# ============================================================

print("\n" + "-" * 70)
print("6. SPECIALTY REFERENCE VALIDATION")
print("-" * 70)

invalid_specialty_references = []

for symptom, specialty in symptom_map.items():

    if not isinstance(specialty, str) or not specialty.strip():
        invalid_specialty_references.append(
            (symptom, specialty)
        )

    elif specialty not in canonical_set:
        invalid_specialty_references.append(
            (symptom, specialty)
        )


if invalid_specialty_references:
    print("[FAIL] Invalid or missing specialty references:")

    for symptom, specialty in invalid_specialty_references:
        print(f"       - {repr(symptom)} -> {repr(specialty)}")

else:
    print("[PASS] Every symptom has a valid canonical specialty.")


# ============================================================
# 8. MISSING SPECIALTY CATEGORIES
# ============================================================

print("\n" + "-" * 70)
print("7. SPECIALTY COVERAGE")
print("-" * 70)

mapped_specialties = set(symptom_map.values())

missing_categories = [
    specialty
    for specialty in canonical_specialties
    if specialty not in mapped_specialties
]

if missing_categories:
    print("[WARNING] Canonical specialties without normal symptom mappings:")

    for specialty in missing_categories:
        print(f"          - {specialty}")

else:
    print("[PASS] Every canonical specialty has at least one normal symptom mapping.")


# ============================================================
# 9. EMPTY SPECIALTY MAPPINGS
# ============================================================

print("\n" + "-" * 70)
print("8. EMPTY VALUE CHECK")
print("-" * 70)

empty_values = []

for symptom, specialty in symptom_map.items():

    if not isinstance(specialty, str) or not specialty.strip():
        empty_values.append((symptom, specialty))

if empty_values:
    print("[FAIL] Empty specialty values found:")

    for symptom, specialty in empty_values:
        print(f"       - {repr(symptom)} -> {repr(specialty)}")

else:
    print("[PASS] No empty specialty values.")


# ============================================================
# 10. EMERGENCY OVERRIDE VALIDATION
# ============================================================

print("\n" + "-" * 70)
print("9. EMERGENCY OVERRIDE VALIDATION")
print("-" * 70)

emergency_map = data["emergency_overrides"]

emergency_errors = []

for symptom, specialty in emergency_map.items():

    if not isinstance(symptom, str) or not symptom.strip():
        emergency_errors.append(
            (symptom, specialty, "empty emergency keyword")
        )

    elif not isinstance(specialty, str) or not specialty.strip():
        emergency_errors.append(
            (symptom, specialty, "empty specialty")
        )

    elif specialty != "Emergency":
        emergency_errors.append(
            (symptom, specialty, "must map to Emergency")
        )


if emergency_errors:
    print("[FAIL] Emergency override problems:")

    for symptom, specialty, reason in emergency_errors:
        print(f"       - {repr(symptom)} -> {repr(specialty)}")
        print(f"         Reason: {reason}")

else:
    print("[PASS] All emergency overrides are valid and map to Emergency.")


# ============================================================
# 11. DUPLICATE EMERGENCY KEY CHECK
# ============================================================

print("\n" + "-" * 70)
print("10. EMERGENCY DUPLICATE CHECK")
print("-" * 70)

emergency_normalized = {}
emergency_duplicates = []

for key in emergency_map:

    normalized = normalize_keyword(key)

    if normalized in emergency_normalized:
        emergency_duplicates.append(
            (key, emergency_normalized[normalized], normalized)
        )
    else:
        emergency_normalized[normalized] = key


if emergency_duplicates:
    print("[FAIL] Duplicate emergency keys after normalization:")

    for current, previous, normalized in emergency_duplicates:
        print(f"       - {repr(previous)}")
        print(f"         {repr(current)}")
        print(f"         Normalized: {repr(normalized)}")

else:
    print("[PASS] No duplicate normalized emergency keys.")


# ============================================================
# 12. ROUTING PRIORITY VALIDATION
# ============================================================

print("\n" + "-" * 70)
print("11. ROUTING POLICY VALIDATION")
print("-" * 70)

routing_policy = data.get("routing_policy", {})
priority = routing_policy.get("priority", [])

expected_priority_items = [
    "Emergency",
    "Pediatrics",
    "keyword_specialty",
    "General Practice",
]

if priority == expected_priority_items:
    print("[PASS] Routing priority matches the defined policy.")

else:
    print("[WARNING] Routing priority differs from the expected policy.")
    print(f"          Current:  {priority}")
    print(f"          Expected: {expected_priority_items}")


# ============================================================
# 13. NORMALIZATION POLICY VALIDATION
# ============================================================

print("\n" + "-" * 70)
print("12. NORMALIZATION POLICY")
print("-" * 70)

normalization = data.get("normalization", {})

expected_normalization = {
    "case_sensitive": False,
    "trim_whitespace": True,
    "collapse_internal_whitespace": True,
    "unicode_normalization": "NFKC",
    "match_mode": "exact_keyword_after_normalization",
}

normalization_errors = []

for key, expected_value in expected_normalization.items():

    actual_value = normalization.get(key)

    if actual_value != expected_value:
        normalization_errors.append(
            (key, actual_value, expected_value)
        )


if normalization_errors:
    print("[WARNING] Normalization settings differ from expected values:")

    for key, actual, expected in normalization_errors:
        print(
            f"       - {key}: current={repr(actual)}, "
            f"expected={repr(expected)}"
        )

else:
    print("[PASS] Normalization policy is consistent.")


# ============================================================
# 14. SUMMARY COUNTS
# ============================================================

print("\n" + "=" * 70)
print("FINAL DATASET SUMMARY")
print("=" * 70)

print(f"Canonical specialties : {len(canonical_specialties)}")
print(f"Normal mappings       : {len(symptom_map)}")
print(f"Emergency overrides   : {len(emergency_map)}")
print(f"Normalized keywords   : {len(normalized_keys)}")

print("\nMappings per specialty:")

specialty_counts = Counter(symptom_map.values())

for specialty in canonical_specialties:
    print(
        f"  {specialty}: "
        f"{specialty_counts.get(specialty, 0)}"
    )


# ============================================================
# 15. FINAL STATUS
# ============================================================

critical_failures = (
    missing_sections
    or structure_errors
    or duplicate_specialties
    or empty_specialties
    or malformed_keys
    or empty_keys
    or whitespace_keys
    or normalized_duplicates
    or invalid_specialty_references
    or empty_values
    or emergency_errors
    or emergency_duplicates
)

print("\n" + "=" * 70)
print("FINAL VALIDATION STATUS")
print("=" * 70)

if critical_failures:
    print("[FAIL] Dataset still contains issues that require correction.")
    print("       Do NOT finalize the JSON yet.")

else:
    print("[PASS] No critical structural, formatting, duplicate-key,")
    print("       or missing-specialty-reference problems were found.")

    if missing_categories:
        print("\n[REVIEW] Some canonical specialties have no normal mappings.")

    if normalization_errors:
        print("\n[REVIEW] Normalization settings differ from expected policy.")

    print("\nThe JSON passed the automated final validation.")
    print("Any remaining medical-mapping concerns require domain review.")
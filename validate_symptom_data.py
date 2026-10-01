import json

# Load the JSON dataset
with open("symptom_specialty.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print("=== Symptom Specialty Data Validation ===\n")

# 1. Check required sections
required_sections = [
    "canonical_specialties",
    "normalization",
    "symptom_to_specialty",
    "emergency_overrides",
    "routing_policy"
]

print("1. Checking required sections...")

for section in required_sections:
    if section in data:
        print(f"   ✓ {section}")
    else:
        print(f"   ✗ Missing: {section}")

# 2. Check specialty values
print("\n2. Checking specialty values...")

canonical_specialties = set(data["canonical_specialties"])

invalid_mappings = []

for symptom, specialty in data["symptom_to_specialty"].items():
    if specialty not in canonical_specialties:
        invalid_mappings.append((symptom, specialty))

if invalid_mappings:
    print("   ✗ Invalid specialty mappings found:")
    for symptom, specialty in invalid_mappings:
        print(f"      {symptom} -> {specialty}")
else:
    print("   ✓ All symptom specialties are valid")

# 3. Check emergency specialties
print("\n3. Checking emergency overrides...")

invalid_emergency = []

for symptom, specialty in data["emergency_overrides"].items():
    if specialty not in canonical_specialties:
        invalid_emergency.append((symptom, specialty))

if invalid_emergency:
    print("   ✗ Invalid emergency mappings found:")
    for symptom, specialty in invalid_emergency:
        print(f"      {symptom} -> {specialty}")
else:
    print("   ✓ All emergency mappings are valid")

# 4. Check empty keys or values
print("\n4. Checking for empty symptoms or specialties...")

empty_entries = []

for symptom, specialty in data["symptom_to_specialty"].items():
    if not symptom.strip() or not specialty.strip():
        empty_entries.append((symptom, specialty))

if empty_entries:
    print("   ✗ Empty entries found:")
    for entry in empty_entries:
        print(f"      {entry}")
else:
    print("   ✓ No empty entries found")

# 5. Check duplicate normalized keywords
print("\n5. Checking for duplicate normalized keywords...")

normalized_keywords = {}
duplicates = []

for symptom in data["symptom_to_specialty"]:
    normalized = " ".join(symptom.strip().lower().split())

    if normalized in normalized_keywords:
        duplicates.append(
            (symptom, normalized_keywords[normalized])
        )
    else:
        normalized_keywords[normalized] = symptom

if duplicates:
    print("   ✗ Duplicate normalized keywords found:")
    for first, second in duplicates:
        print(f"      '{first}' conflicts with '{second}'")
else:
    print("   ✓ No duplicate normalized keywords found")

# 6. Count symptoms per specialty
print("\n6. Symptoms per specialty:")

specialty_counts = {}

for specialty in canonical_specialties:
    specialty_counts[specialty] = 0

for specialty in data["symptom_to_specialty"].values():
    specialty_counts[specialty] += 1

for specialty, count in sorted(specialty_counts.items()):
    print(f"   {specialty}: {count}")

# 7. Check routing priority
print("\n7. Checking routing priority...")

priority = data["routing_policy"]["priority"]

for item in priority:
    if item == "keyword_specialty":
        print("   ✓ keyword_specialty (routing rule)")
    elif item in canonical_specialties:
        print(f"   ✓ {item}")
    else:
        print(f"   ✗ Invalid priority: {item}")

print("\n=== Validation Complete ===")
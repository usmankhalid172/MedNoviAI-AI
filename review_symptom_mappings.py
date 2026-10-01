import json

# Load the dataset
with open("symptom_specialty.json", "r", encoding="utf-8") as file:
    data = json.load(file)

symptom_to_specialty = data["symptom_to_specialty"]
emergency_overrides = data["emergency_overrides"]

print("=== Symptom-to-Specialty Review Report ===\n")


# --------------------------------------------------
# 1. Mappings that need human/clinical review
# --------------------------------------------------

print("1. Mappings requiring human review:")
print()

review_items = {
    "flank pain": "Nephrology",
    "fainting": "Neurology",
    "ankle swelling": "Cardiology",
}

for symptom, specialty in review_items.items():
    if symptom in symptom_to_specialty:
        print(f"   • {symptom} -> {specialty}")
        print("     Reason: This symptom can have multiple possible causes/specialties.")
        print()


# --------------------------------------------------
# 2. Check related singular/plural keywords
# --------------------------------------------------

print("2. Related keyword pairs:")
print()

related_pairs = [
    ("seizure", "seizures"),
]

for first, second in related_pairs:
    if first in symptom_to_specialty and second in symptom_to_specialty:
        first_specialty = symptom_to_specialty[first]
        second_specialty = symptom_to_specialty[second]

        print(f"   • {first} -> {first_specialty}")
        print(f"   • {second} -> {second_specialty}")

        if first_specialty == second_specialty:
            print("     ✓ Both route to the same specialty.")
        else:
            print("     ⚠ They route to different specialties.")

        print()


# --------------------------------------------------
# 3. Emergency override review
# --------------------------------------------------

print("3. Emergency override review:")
print()

print(f"   Total emergency overrides: {len(emergency_overrides)}")

for symptom, specialty in emergency_overrides.items():
    print(f"   ✓ {symptom} -> {specialty}")

print()


# --------------------------------------------------
# 4. Check that every emergency mapping is Emergency
# --------------------------------------------------

print("4. Checking emergency mappings:")

emergency_errors = []

for symptom, specialty in emergency_overrides.items():
    if specialty != "Emergency":
        emergency_errors.append((symptom, specialty))

if emergency_errors:
    print("   ✗ Emergency mapping problems found:")

    for symptom, specialty in emergency_errors:
        print(f"      {symptom} -> {specialty}")

else:
    print("   ✓ All emergency overrides correctly map to Emergency")

print()


# --------------------------------------------------
# 5. Check important emergency vs normal routing
# --------------------------------------------------

print("5. Checking emergency vs normal routing:")

routing_checks = [
    ("severe breathing difficulty", "Emergency"),
    ("breathing difficulty", "Pulmonology"),
    ("chest pain with fainting", "Emergency"),
    ("chest pain", "Cardiology"),
]

for symptom, expected_specialty in routing_checks:

    if symptom in emergency_overrides:
        actual = emergency_overrides[symptom]

        if actual == expected_specialty:
            print(f"   ✓ {symptom} -> {actual}")
        else:
            print(
                f"   ✗ {symptom} -> {actual} "
                f"(expected {expected_specialty})"
            )

    elif symptom in symptom_to_specialty:
        actual = symptom_to_specialty[symptom]

        if actual == expected_specialty:
            print(f"   ✓ {symptom} -> {actual}")
        else:
            print(
                f"   ✗ {symptom} -> {actual} "
                f"(expected {expected_specialty})"
            )

    else:
        print(f"   ✗ Missing mapping: {symptom}")

print()


# --------------------------------------------------
# 6. Summary
# --------------------------------------------------

print("=== Review Summary ===")
print()

print(f"Total normal symptom mappings: {len(symptom_to_specialty)}")
print(f"Total emergency overrides: {len(emergency_overrides)}")
print(f"Mappings flagged for human review: {len(review_items)}")

print()
print("No automatic changes were made to the dataset.")
print("Human/clinical review is required before changing flagged mappings.")
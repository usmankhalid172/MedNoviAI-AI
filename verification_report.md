# Symptom-to-Specialty Dictionary Verification Report

## Dataset

- Normal symptom mappings: 99
- Emergency overrides: 11
- Canonical specialties: 16
- Schema version: 1.0.0

## Automated Validation

The dataset was validated using `validate_symptom_data.py`.

Results:

- All required sections are present.
- All normal symptom mappings use valid canonical specialties.
- All emergency overrides use valid specialties.
- No empty symptom keys or specialty values were found.
- No duplicate normalized keywords were found.
- Routing priority contains valid values.
- Emergency overrides correctly map to `Emergency`.

## Mapping Review

Three mappings were flagged for human/domain review because the symptoms can potentially have multiple causes or specialty routes:

| Symptom | Current Specialty | Review Status |
|---|---|---|
| flank pain | Nephrology | Requires domain review |
| fainting | Neurology | Requires domain review |
| ankle swelling | Cardiology | Requires domain review |

These mappings were not automatically changed because the dataset specifies that a symptom may belong to multiple specialties and that the dictionary intentionally stores a primary routing target.

## Related Keywords

The following related keywords were checked:

- `seizure` → Neurology
- `seizures` → Neurology

Both correctly route to the same specialty and are retained because the routing mode uses exact normalized keyword matching.

## Emergency Routing

All 11 emergency overrides were verified to map to `Emergency`.

Emergency routing also takes priority over ordinary specialty routing according to the dataset's routing policy.

Examples:

- `severe breathing difficulty` → Emergency
- `breathing difficulty` → Pulmonology
- `chest pain with fainting` → Emergency
- `chest pain` → Cardiology

No emergency-routing inconsistencies were identified.

## Conclusion

The automated verification found no structural or formatting errors in the lookup dictionary.

Three potentially ambiguous mappings were identified for human/domain review. No automatic clinical changes were made.

The dataset is technically consistent with its defined normalization and routing rules.
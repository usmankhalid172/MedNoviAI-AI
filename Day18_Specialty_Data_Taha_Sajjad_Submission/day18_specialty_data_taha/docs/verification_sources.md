# Verification Sources

These sources were used as high-level safety/clinical-reference checks while cleaning the routing vocabulary. They do not validate the project code and should not be treated as a substitute for clinical governance.

1. American Heart Association — Chest pain: When to see a doctor
   https://www.heart.org/en/health-topics/house-calls/common-causes-of-chest-pain

2. American Heart Association — Warning Signs of a Heart Attack
   https://www.heart.org/en/health-topics/heart-attack/warning-signs-of-a-heart-attack

3. American Heart Association — 2021 Guideline for the Evaluation and Diagnosis of Chest Pain
   https://professional.heart.org/en/science-news/2021-guideline-for-the-evaluation-and-diagnosis-of-chest-pain/top-things-to-know

4. NHS — Urinary tract infections (UTIs)
   https://www.nhs.uk/conditions/urinary-tract-infections-utis/

Review note:
- Chest discomfort/tightness and shortness of breath can be associated with serious cardiac conditions; therefore the dataset separates emergency overrides from ordinary specialty routing.
- Urinary symptoms are grouped under urology as a primary routing target, while the data does not attempt to distinguish infection, stones, kidney disease, or other diagnoses.

# Task 12 — Patient Journey End-to-End Simulation & Verification

## 1. Task Information

**Assignee:** Joyce Hany  
**Role:** End-to-End Flow Simulation QA  
**Branch:** `feature/sprint1-flow-simulation-joyce`  
**PR Title:** `Task-sept12-flow-simulation-joycehany`

## 2. Objective

Simulate and verify the complete target patient journey:

Patient Login → Search Doctor → Check Availability → Book Appointment
→ AI Assistant → Patient Intake → Backend Storage

## 3. Test Environment

**Repository:** MedNoviAI-AI  
**Environment:** Local Windows / PowerShell  
**Testing Type:** End-to-End Flow Simulation and Integration QA

## 4. Journey Verification

| Stage | Expected Behavior | Actual Result | Status |
|---|---|---|---|
| Patient Login | Patient can authenticate | No executable healthcare patient login flow identified | BLOCKED |
| Search Doctor | Patient can search available doctors | Doctor data exists, but no executable search API identified | BLOCKED |
| Check Availability | Available slots are returned | Appointment slot data exists, but no executable availability API identified | BLOCKED |
| Book Appointment | Appointment can be created | No executable booking API identified | BLOCKED |
| AI Assistant | Patient can interact with healthcare AI assistant | No complete executable healthcare assistant flow identified | BLOCKED |
| Patient Intake | Patient information is parsed | No executable healthcare intake parser identified | BLOCKED |
| Backend Storage | Intake/appointment data is persisted | No executable healthcare storage integration identified | BLOCKED |

## 5. Available Healthcare Data

The repository contains healthcare knowledge-base and vector-ready data including:

- Cardiology
  - Dr. Ahmed Khan
  - Dr. Sarah Ali
  - Mon-Fri, 09:00 AM - 01:00 PM

- Dermatology
  - Dr. Fatima Noor
  - Tue-Thu, 02:00 PM - 06:00 PM

- Pediatrics
  - Dr. Usman Tariq
  - Mon-Sat, 10:00 AM - 03:00 PM

- General Medicine
  - Dr. Bilquis Raza
  - Mon-Sun, 08:00 AM - 08:00 PM

These records provide healthcare reference data but do not by themselves provide an executable end-to-end appointment workflow.

## 6. Integration Blockers

The following components could not be executed as a complete local healthcare journey:

1. Patient authentication
2. Doctor search
3. Availability checking
4. Appointment booking
5. Healthcare AI assistant integration
6. Patient intake parsing
7. Backend persistence/storage

The local service check also showed that no service was listening on the tested local port `5000`.

## 7. Bug Log

| Bug ID | Description | Severity | Status |
|---|---|---|---|
| BUG-012-01 | Patient login flow unavailable | High | Open |
| BUG-012-02 | Doctor search flow unavailable | High | Open |
| BUG-012-03 | Availability checking unavailable | High | Open |
| BUG-012-04 | Appointment booking unavailable | High | Open |
| BUG-012-05 | Healthcare AI assistant integration unavailable | High | Open |
| BUG-012-06 | Patient intake integration unavailable | High | Open |
| BUG-012-07 | Backend storage integration unavailable | High | Open |

## 8. Final Status

**Overall Task Status: BLOCKED**

The complete target patient journey could not be executed end-to-end because the required healthcare integration components were not available in the tested local repository/environment.

The healthcare knowledge-base data is present, but executable patient-flow APIs and integrations required for the complete journey were not identified.

## 9. Recommended Next Steps

1. Provide the patient authentication endpoint.
2. Provide doctor search and availability APIs.
3. Provide the appointment booking API.
4. Integrate the healthcare AI assistant.
5. Implement or expose patient intake parsing.
6. Connect patient and appointment data to backend storage.
7. Re-run the complete end-to-end journey after integration.

## 10. QA Conclusion

The QA simulation successfully identified the current integration gap between the available healthcare reference data and the executable patient journey.

Further end-to-end verification should be performed once the required healthcare APIs and backend integrations are available.
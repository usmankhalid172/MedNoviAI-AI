# Task 21 — Complete Patient Journey Simulation & Final MVP Sign-Off

**Assignee:** Joyce Hany  
**Role:** End-to-End Flow QA  
**Branch:** `feature/sprint1-flow-simulation-joyce`  
**PR Title:** `Task-sept21-flow-simulation-joycehany`

---

## Objective

Execute the final end-to-end simulation of the complete patient journey:

Registration → AI Intake → Specialty Guidance → Doctor Selection → Booking Confirmation

The objective is to verify the complete MVP patient workflow, identify any remaining blocking issues, and determine whether the workflow is ready for final SQA sign-off.

---

# 1. Registration

### Expected

The patient should be able to register successfully and continue to the authenticated patient journey.

### Verification Status

**NOT VERIFIED END-TO-END**

### Result

The complete registration-to-AI healthcare journey could not be verified through the tested deployed healthcare flow because the required downstream healthcare AI endpoints were not available.

### Status

**BLOCKED**

---

# 2. AI Intake

### Expected

The patient should be able to provide symptoms and relevant information through the AI assistant, and the system should convert the conversation into structured intake information.

### Verification Status

**BLOCKED**

### Result

The required healthcare AI intake functionality was not exposed through the tested deployment.

The healthcare chat endpoint:

`/api/ai/chat`

returned:

```json
{
  "detail": "Not Found"
}

Status

BLOCKED

3. Specialty Guidance
Expected

The structured patient symptoms and intake information should be used to provide appropriate specialty guidance.

Verification Status

BLOCKED

Result

No executable healthcare specialty-guidance endpoint was available in the tested deployment.

Status

BLOCKED

4. Doctor Selection
Expected

The patient should be able to select or search for a doctor based on the recommended specialty.

Verification Status

BLOCKED

Result

The integrated doctor-selection step could not be verified because the preceding healthcare AI workflow was not available as an executable deployed flow.

Status

BLOCKED

5. Booking Confirmation
Expected

The patient should be able to select an available appointment slot and complete the booking successfully, receiving a booking confirmation.

Verification Status

BLOCKED

Result

The complete patient journey could not reach the booking stage through the tested healthcare AI integration.

Therefore, booking confirmation could not be verified as part of the complete end-to-end journey.

Status

BLOCKED

Complete Patient Journey Verification
Journey Stage	Expected Result	Actual Result	Status
Registration	Patient registration succeeds	Full integrated journey not verifiable	BLOCKED
AI Intake	Patient symptoms converted to structured intake	Healthcare AI endpoint unavailable	BLOCKED
Specialty Guidance	Appropriate specialty guidance	Endpoint unavailable	BLOCKED
Doctor Selection	Doctor selected based on specialty	Integrated flow unavailable	BLOCKED
Booking Confirmation	Appointment successfully booked	End-to-end flow unavailable	BLOCKED
Blocking Bug / Issue Status
ID	Issue	Severity	Status
F-21-01	Healthcare /api/ai/chat endpoint returns Not Found	High	Open / Blocking
F-21-02	Healthcare intake flow unavailable in deployed environment	High	Open / Blocking
F-21-03	Specialty guidance cannot be verified	High	Open / Blocking
F-21-04	Doctor selection integration cannot be verified	High	Open / Blocking
F-21-05	Booking confirmation cannot be verified end-to-end	High	Open / Blocking
MVP Sign-Off Criteria

The complete MVP patient journey should only receive final SQA sign-off after the following conditions are verified:

Registration works successfully.
Patient AI chat is available and functional.
AI intake parsing works correctly.
Symptoms are extracted into structured information.
Specialty guidance is returned correctly.
Doctor selection/search is integrated with the recommended specialty.
Appointment availability can be retrieved.
Doctor booking can be completed successfully.
Booking confirmation is returned to the patient.
AI → Backend integration works correctly.
Previously reported blocking issues are fixed.
Regression testing confirms that the complete journey remains functional.
Final MVP Sign-Off Decision

SQA Sign-Off Status: BLOCKED — NOT READY FOR FINAL SIGN-OFF

The complete patient journey could not be verified as a successful end-to-end workflow in the tested deployment.

The main blocking evidence is the unavailable healthcare chat endpoint:

/api/ai/chat

which returned:

{
  "detail": "Not Found"
}

Because the healthcare AI flow is blocked at the entry point, the subsequent Intake, Specialty Guidance, Doctor Selection, and Booking Confirmation stages cannot be confirmed as a complete integrated journey.

Therefore, zero blocking bugs cannot currently be confirmed.

Required Retest Before Final Sign-Off

After the healthcare AI and backend integrations are available, the following complete journey must be retested:

Registration
      ↓
Patient Login
      ↓
AI Patient Chat
      ↓
AI Intake Parsing
      ↓
Symptom Extraction
      ↓
Specialty Guidance
      ↓
Doctor Search
      ↓
Doctor Selection
      ↓
Available Slot
      ↓
Appointment Booking
      ↓
Booking Confirmation

Each stage must be verified successfully before final MVP SQA sign-off.

Final Conclusion

The final MVP patient journey remains BLOCKED based on the tested deployment evidence.

The current evidence does not support a zero-blocking-bug or final-pass conclusion.

Final SQA sign-off should remain pending until the healthcare AI endpoints and their integration with doctor search and appointment booking are available and successfully retested.
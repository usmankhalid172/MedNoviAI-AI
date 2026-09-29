# Day 27 — Doctor Search and Appointment Guidance Demonstration

## 1. Overview

Day 27 demonstrates the existing doctor search assistance and appointment guidance flows in MedNoviAI.

The demonstration uses the existing automated tests to verify that doctor-information guidance and appointment-assistance behavior work according to the documented prompt and response contracts.

No new chatbot or appointment functionality was introduced for this demonstration.

## 2. Doctor Search Assistance Flow

The doctor search assistance flow is supported by the doctor-information module.

The flow covers:

1. Receiving a doctor-information query.
2. Detecting the requested information type.
3. Using backend-provided doctor information.
4. Maintaining relevant conversation context.
5. Returning structured doctor information.
6. Requesting clarification when required information is unavailable or unclear.

The doctor display information follows the supported fields:

- `doctor_id`
- `doctor_name`
- `specialty`
- `qualifications`
- `experience`
- `clinic`
- `address`
- `consultation_fee`

The assistant does not invent unsupported doctor information.

## 3. Appointment Guidance Flow

The appointment guidance flow supports controlled assistance with doctor availability and appointment-related requests.

The flow covers:

1. Identifying the doctor.
2. Reviewing backend-provided availability.
3. Selecting an available slot.
4. Providing required appointment information.
5. Relying on backend confirmation for booking status.

Appointment slots remain associated with the doctor supplied by the backend.

The assistant does not invent slots, change backend-provided date or time values, or claim that an appointment has been booked without backend confirmation.

## 4. Test Demonstration

### Doctor Information Tests

Command:

```bash
python -m pytest tests\test_doctor_information.py -v

Result:

```bash
python -m pytest tests\test_doctor_information.py -v

Result:

29 passed

The test suite validates doctor-information behavior including:

Profile and schedule intent handling.
Conversation context.
Doctor display-card fields.
Profile and schedule separation.
Unsupported field protection.
Internal information protection.
Doctor search guidance prompt behavior.
Appointment Assistance Tests

Command:

python -m pytest tests\test_appointment_assistance.py -v

Result:

16 passed

The test suite validates appointment guidance behavior including:

Availability handling.
Backend-provided appointment slots.
Doctor and slot association.
Appointment guidance rules.
Booking confirmation requirements.
Protection against invented appointment information.
5. Demonstrated Flow

The validated workflow can be summarized as:

User Doctor Query
        |
        v
Doctor Information Intent
        |
        v
Backend-Provided Doctor Data
        |
        v
Doctor Search Guidance
        |
        v
Structured Doctor Information
        |
        v
Availability Request
        |
        v
Backend-Provided Appointment Slots
        |
        v
Appointment Guidance
        |
        v
Backend Confirmation

The chatbot guidance layer does not independently create doctor records, availability, appointment slots, or booking confirmations.

6. Validation Status

Day 27 demonstration evidence:

Doctor information tests: 29 passed
Appointment assistance tests: 16 passed

The demonstrated flows are supported by the existing doctor-information and appointment-assistance implementation.

7. Scope

This demonstration validates the existing guidance and test behavior.

It does not claim live doctor search or live appointment booking because those operations depend on the project's backend services and available doctor or appointment data.

No new feature was added as part of Day 27.

8. Summary

Day 27 demonstrates the doctor search assistance and appointment guidance flows through the existing automated test suites.

The results confirm that the documented doctor-information and appointment guidance rules are covered by passing tests while keeping doctor and appointment data grounded in backend-provided information.

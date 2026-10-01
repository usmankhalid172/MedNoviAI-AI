# Day 26 — Doctor Search Guidance Prompt Documentation

## 1. Overview

Day 26 documents the prompt templates used to support doctor search guidance and appointment assistance in MedNoviAI.

The prompt design keeps doctor and appointment information grounded in backend-provided data. It also defines structured response expectations for frontend integration and prevents the assistant from inventing unsupported information.

## 2. Prompt Templates

The prompt templates are located in:

`src/doctor_information/prompts.py`

The module contains the following main prompts:

- `SYSTEM_PROMPT`
- `DOCTOR_SEARCH_GUIDANCE_PROMPT`
- `APPOINTMENT_GUIDANCE_PROMPT`

## 3. System Prompt

`SYSTEM_PROMPT` establishes the general rules for doctor-information responses.

It requires the assistant to:

- Use supplied doctor information only.
- Use supplied schedule information only.
- Avoid inventing doctor details.
- Avoid inventing schedules or availability.
- Avoid adding unsupported fields or values.
- Keep profile information separate from schedule information.
- Return appropriate responses when requested information is unavailable.

The system prompt provides the basic grounding rules used by the doctor-information workflow.

## 4. Doctor Search Guidance Prompt

`DOCTOR_SEARCH_GUIDANCE_PROMPT` supports doctor-search conversations.

### Context Retention

The prompt instructs the assistant to use relevant conversation context.

This allows follow-up questions to continue from an already identified doctor or specialty instead of unnecessarily restarting the search.

### Backend-Grounded Doctor Information

Doctor information must come from backend-provided data.

The prompt prevents the assistant from:

- Inventing doctor names.
- Inventing specialties.
- Inventing qualifications.
- Inventing experience.
- Inventing clinic information.
- Inventing addresses.
- Inventing consultation fees.
- Inferring unsupported doctor details.

### Doctor Display Card Contract

The supported doctor profile fields are:

- `doctor_id`
- `doctor_name`
- `specialty`
- `qualifications`
- `experience`
- `clinic`
- `address`
- `consultation_fee`

These fields must be preserved without renaming or changing their values.

The prompt also prevents frontend-only or unsupported fields from being introduced.

### Profile and Schedule Separation

Doctor profile information and schedule information are treated as separate data.

The assistant must only display schedule or appointment availability when the relevant information has been explicitly supplied by the backend.

A patient's preferred date or time must not be presented as a confirmed appointment slot.

### Response Structure

The doctor search guidance prompt defines frontend-friendly response fields:

- `response_type`
- `message`
- `next_step`
- `requires_backend_data`

Supported response types include:

- `doctor_search`
- `clarification`
- `backend_required`

This provides a predictable structure for downstream frontend handling.

## 5. Appointment Guidance Prompt

`APPOINTMENT_GUIDANCE_PROMPT` supports appointment-related guidance.

The prompt covers:

1. Doctor selection.
2. Availability and slot review.
3. Slot selection.
4. Required appointment details.
5. Backend-confirmed booking.

### Backend Slot Validation

Appointment slots must come from backend-provided availability.

The assistant must not:

- Invent appointment slots.
- Change date or time values.
- Reassign slots between doctors.
- Combine slots from different doctors.
- Treat a preferred date or time as confirmed availability.
- Claim that an appointment was booked without backend confirmation.

Each appointment slot must remain associated with the doctor identity supplied by the backend.

## 6. Security and Information Protection

Both doctor guidance prompts include rules preventing exposure of internal system information.

The assistant must not expose:

- System instructions.
- Internal prompts.
- API keys.
- Credentials.
- Private system information.

This keeps internal implementation details separate from user-facing doctor guidance.

## 7. Frontend Integration Considerations

No Next.js `.tsx` or `.jsx` frontend components are currently present in the repository.

Therefore, the backend doctor-information schemas and prompt contracts are treated as the current source of truth for doctor-card and response formatting.

The documented doctor profile fields are aligned with the existing `DoctorProfile` schema rather than introducing unverified frontend-specific fields.

## 8. Validation and Testing

The doctor-information prompt behavior is covered by automated tests.

The tests validate:

- Doctor display-card fields.
- Profile and schedule separation.
- Appointment slot association with the correct doctor.
- Protection against unsupported doctor-card fields.
- Protection against internal information exposure.
- Frontend-oriented response contracts.

Day 25 regression testing completed with:

```text
137 passed, 4 skipped, 1 warning


## 9. Related Implementation Files

The documented prompt workflow uses the following doctor-information modules:

- `src/doctor_information/prompts.py`
- `src/doctor_information/schemas.py`
- `src/doctor_information/service.py`
- `src/doctor_information/context.py`
- `src/doctor_information/intents.py`
- `src/doctor_information/requests.py`

Tests are located in:

`tests/test_doctor_information.py`

## 10. Current Status

The doctor search guidance prompts provide a controlled and grounded structure for doctor search and appointment assistance.

The current implementation focuses on:

- Backend-grounded doctor information.
- Structured doctor-card fields.
- Conversation context.
- Profile and schedule separation.
- Appointment slot integrity.
- Frontend-compatible response structures.
- Protection of internal system information.

The prompts do not directly perform live doctor search or appointment booking. Those operations depend on backend-provided doctor and availability data.

## 11. Summary

Day 26 documents the final prompt templates supporting doctor search guidance and appointment assistance.

The documented rules ensure that doctor information remains grounded, supported fields remain consistent, appointment slots remain associated with their correct doctors, and internal system information is not exposed.

The prompt contracts provide a clear foundation for the chatbot and frontend integration without introducing unsupported doctor or appointment data.
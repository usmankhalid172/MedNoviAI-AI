\# Day 13 — Doctor Information and Search Guidance



\## 1. Overview



Day 13 focused on building the doctor-information foundation for MedNoviAI. The implementation supports structured doctor profile and schedule lookups, multi-turn conversation context, intent detection, and grounded guidance prompts for doctor search and appointment assistance.



The implementation is designed to use backend-provided doctor information and does not invent doctor details, schedules, availability, or appointment confirmations.



\## 2. Objectives



\- Detect doctor profile and schedule information requests.

\- Support structured doctor profile information.

\- Support doctor schedule information.

\- Maintain the active doctor across conversation turns.

\- Return structured responses for frontend use.

\- Add grounded prompts for doctor search and appointment guidance.

\- Prevent unsupported medical, doctor, or appointment information from being generated.



\## 3. Module Structure



The Day 13 implementation is located in `src/doctor\\\_information/`.



\### `intents.py`



Handles doctor-information intent detection.



Supported intents:



\- `profile`

\- `schedule`

\- `unknown`



Profile-related keywords include qualifications, specialty, experience, clinic, address, and consultation fee.



Schedule-related keywords include working hours, working days, timings, and availability.



The input is normalized before keyword matching, and invalid or empty input is rejected.



\### `schemas.py`



Defines the structured data models:



\- `DoctorProfile`

\- `DoctorSchedule`

\- `DoctorInformationResponse`



`DoctorProfile` stores doctor details such as name, specialty, qualifications, experience, clinic, address, and consultation fee.



`DoctorSchedule` stores the doctor's name, ID, and schedule.



`DoctorInformationResponse` provides the returned doctor or schedule data together with availability status and a user-facing message.



\### `requests.py`



Defines `DoctorInformationRequest` for doctor-information lookup requests.



It accepts:



\- query

\- doctor name

\- doctor ID

\- information type



The query must contain at least one character.



\### `context.py`



Defines `DoctorConversationContext` for maintaining multi-turn context.



It stores:



\- active doctor

\- active doctor ID

\- last detected intent



This allows follow-up questions to continue using the doctor already established in the conversation.



\### `service.py`



Contains `DoctorInformationService`, which processes doctor-information requests.



The service:



1\. Detects the user's intent.

2\. Handles unknown requests.

3\. Uses supplied doctor profile data for profile requests.

4\. Uses supplied schedule data for schedule requests.

5\. Updates the active doctor and last intent when information is available.

6\. Returns a structured `DoctorInformationResponse`.



The service uses supplied backend-style data and does not create doctor or schedule information itself.



\### `prompts.py`



Contains grounded guidance prompts for:



\- Doctor search guidance

\- Appointment guidance



The prompts instruct the AI to use backend-provided information only and avoid inventing doctors, specialties, qualifications, fees, locations, schedules, appointment slots, or availability.



\## 4. Doctor Information Workflow



The basic workflow is:



```text

User Query

\&#x20;   ↓

Intent Detection

\&#x20;   ↓

Profile / Schedule / Unknown

\&#x20;   ↓

Use Backend-Provided Data

\&#x20;   ↓

Update Conversation Context

\&#x20;   ↓

Structured Response



If the requested information is unavailable, the service returns an appropriate unavailable response instead of generating unsupported information.



\\## 5. Conversation Context



The implementation supports multi-turn doctor-information queries.



For example, after a doctor is identified, a later query about the doctor's schedule can use the active doctor stored in the conversation context.



The context stores the doctor name, doctor ID, and previous intent to support continuity.



\\## 6. Grounded Doctor Search Guidance



The doctor search guidance prompt requires the assistant to:



\\- Use conversation context when relevant.

\\- Use backend-provided doctor or specialty data.

\\- Avoid inventing doctor information.

\\- Ask for clarification when required information is missing.

\\- Preserve the active doctor or specialty when relevant.

\\- Avoid diagnosis and treatment recommendations.

\\- Return frontend-friendly response fields.



\\## 7. Appointment Guidance



The appointment guidance prompt provides a controlled flow for appointment assistance.



The intended flow is:



1\\. Select a doctor.

2\\. Review available slots.

3\\. Select a slot.

4\\. Provide required details.

5\\. Confirm through the booking system.



Requested dates and times are treated as preferences until confirmed by the backend.



The assistant must not claim that an appointment has been booked without backend confirmation.



\\## 8. Testing



Doctor-information tests were executed using:



```bash

python -m pytest tests/test\\\_doctor\\\_information.py -v



Result:



```text

14 passed



python -m pytest -v



Result:



122 passed



The full test suite passed after restoring the required local expense-categorization model artifact used by existing project tests.



\\## 9. Current Integration Status



The Day 13 implementation provides the doctor-information and guidance foundation.



The service accepts backend-provided doctor and schedule data, but it does not itself connect to a live doctor database, appointment provider, or booking API.



Actual doctor search, real-time availability, and appointment booking require integration with the project's backend services.



\\## 10. Limitations and Future Work



Possible future improvements include:



\\- Connect doctor search to the real doctor database.

\\- Connect schedule lookup to real availability data.

\\- Add appointment API integration.

\\- Add stronger intent detection beyond keyword matching.

\\- Support richer doctor-search filters.

\\- Add end-to-end tests using real backend responses.



\\## 11. Git Evidence



Day 13 work is being developed on:



`feature/sprint1-doctor-info-farheen`



Relevant implementation commit:



`a5fe1ad` — `feat: add doctor search and appointment guidance prompts`



The doctor-information module and its tests are included in the current branch.



\\## 12. Summary



Day 13 established a structured and grounded doctor-information layer for MedNoviAI. It supports profile and schedule intents, structured doctor data, multi-turn context, frontend-friendly responses, and controlled doctor-search and appointment guidance while keeping backend-dependent information grounded.





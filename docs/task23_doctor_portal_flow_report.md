# Task 23 — Doctor Portal Workflow Simulation

**Assignee:** Joyce Hany  
**Role:** End-to-End Flow QA  
**Branch:** `feature/sprint1-flow-simulation-joyce`  
**PR Title:** `Task-day23-flow-simulation-joycehany`

---

## Objective

Conduct an end-to-end simulation of the Doctor Portal workflow:

Doctor Login → Appointments → Patient Intake

The objective is to verify the available doctor-side workflow and identify integration gaps between authentication, appointments, patient intake, and the deployed healthcare services.

---

# Test Environment

**Deployed AI Service:**

`https://mednoviai-ai.onrender.com/`

**Testing Method:**

- PowerShell API requests
- OpenAPI route inspection
- Local repository code search

---

# 1. Deployment Availability

### Test

The deployed AI service root endpoint was checked.

### Actual Result

HTTP Status:

`200`

Response indicated that the deployed service currently exposes the Financial Health API.

### Status

**PASS — Service Reachable**

---

# 2. Swagger / OpenAPI Availability

### Test

The deployed Swagger documentation and OpenAPI specification were checked.

### Actual Result

Swagger returned HTTP 200.

The available OpenAPI routes were:

```text
/
/api/ai/financial-health/{user_id}

No Doctor, Appointment, Patient Intake, Authentication, or Login healthcare routes were exposed in the deployed OpenAPI specification.

Status

BLOCKED

Integration Finding

The tested deployment does not currently expose the healthcare endpoints required to execute the Doctor Portal E2E workflow.

3. Healthcare Chat Endpoint
Test

Endpoint:

/api/ai/chat

Actual Result

HTTP Status:

404

Response:

{
  "detail": "Not Found"
}
Status

BLOCKED

Impact

The healthcare AI entry point required by the patient-to-doctor workflow is not available on the tested deployment.

4. Doctor Login
Expected

A doctor should be able to authenticate and access the Doctor Portal.

Test Evidence

The deployed OpenAPI specification did not expose a doctor login or authentication route.

A local repository search for:

doctor login
authentication
authorization
JWT
token

did not identify an executable Doctor Portal authentication implementation in the searched src and tests areas.

Status

NOT VERIFIED

Integration Finding

Doctor authentication could not be verified as an executable end-to-end workflow from the available QA environment.

5. Doctor Appointments
Expected

After authentication, the doctor should be able to access appointments and view appointment-related information.

Test Evidence

The deployed OpenAPI specification did not expose appointment or booking routes.

A local repository search for:

appointment
appointments
booking
availability

did not identify an executable appointment implementation in the searched src and tests areas.

Status

NOT VERIFIED

Integration Finding

The Doctor Portal appointment workflow could not be executed or verified through the available deployment.

6. Patient Intake
Expected

The doctor should be able to access the relevant patient intake information associated with an appointment.

Test Evidence

The deployed OpenAPI specification did not expose a patient intake route.

A local repository search for:

patient intake
PatientIntake
intake

did not identify an executable patient intake implementation in the searched src and tests areas.

Status

BLOCKED

Integration Finding

The Doctor Portal → Patient Intake handoff could not be verified.

7. Doctor Portal E2E Flow
Expected Flow
Doctor Login
     ↓
Doctor Portal
     ↓
Appointments
     ↓
Select Appointment
     ↓
Patient Intake
Actual Result

The complete flow could not be executed because the required Doctor Portal, Appointment, and Patient Intake functionality was not exposed through the tested deployed API.

Status

BLOCKED

Test Results Summary
Test Area	Evidence	Status
Deployed AI Service	HTTP 200	PASS
Swagger	HTTP 200	PASS
Healthcare OpenAPI Routes	Only / and Financial Health route exposed	BLOCKED
Healthcare Chat	/api/ai/chat → HTTP 404	BLOCKED
Doctor Login	No executable route verified	NOT VERIFIED
Doctor Appointments	No executable route verified	NOT VERIFIED
Patient Intake	No executable route verified	BLOCKED
Complete Doctor Portal Flow	Could not execute	BLOCKED
Integration Gap Log
ID	Integration Gap	Severity	Status	Responsible Team
F-23-01	Healthcare API routes are not exposed in deployed OpenAPI	High	Open / Blocking	AI / Backend
F-23-02	/api/ai/chat returns HTTP 404	High	Open / Blocking	AI / Backend
F-23-03	Doctor authentication flow cannot be verified	High	Open / Not Verified	.NET / MERN
F-23-04	Doctor appointment workflow cannot be verified	High	Open / Not Verified	.NET / MERN
F-23-05	Patient intake handoff to Doctor Portal cannot be verified	High	Open / Blocking	AI / .NET / MERN
Developer Actions Required
AI Team

Expose the healthcare AI routes required for the patient and doctor E2E workflows and confirm the deployed routes.

.NET Team

Provide and verify the doctor authentication, appointment, and patient-related API contracts required for the Doctor Portal workflow.

MERN / Doctor Portal Team

Confirm the Doctor Portal routes, authentication flow, appointment display, and patient intake rendering against the backend APIs.

Integration Team

Confirm that the deployed QA environment contains the healthcare services expected by the SQA workflow.

Retest Plan

After the missing healthcare integrations are available, execute:

Doctor Login
     ↓
Doctor Portal
     ↓
Appointments
     ↓
Select Appointment
     ↓
Patient Information
     ↓
Patient Intake

Then verify:

Authentication success
Authorization behavior
Appointment retrieval
Appointment details
Patient information
Patient intake data
Backend request/response
Error handling
Complete Doctor Portal journey
Testing Note

A PowerShell / PSReadLine console rendering error occurred during the OpenAPI inspection command.

The error was related to console rendering and did not represent an application API failure.

The OpenAPI inspection was subsequently executed successfully and returned HTTP 200 with the available routes.

Final SQA Status

Overall Status: BLOCKED — Doctor Portal E2E Verification Pending

The deployed AI service and Swagger documentation are reachable.

However, the tested deployment currently exposes only the root route and Financial Health endpoint. The required healthcare routes for Doctor Login, Appointments, Patient Intake, and the healthcare Chat entry point were not available for complete E2E execution.

The healthcare chat endpoint /api/ai/chat was directly tested and returned HTTP 404.

Therefore, the complete Doctor Portal workflow:

Doctor Login → Appointments → Patient Intake

cannot currently be marked as PASS.
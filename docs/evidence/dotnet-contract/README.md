# QA Evidence — .NET Integration Contract

## Task
- Date: September 8, 2026
- QA Role: Integration QA Lead
- Reviewer: Syeda Isma Nazir

## Coordination
The .NET backend team was contacted as part of the Sprint 1 Integration QA task to confirm the AI-to-.NET integration requirements.

Following the coordination, the .NET team lead provided the confirmed AI-to-.NET Integration Contract.

## Contract Verification

The confirmed contract defines:

- `POST /api/ai/chat` for AI conversational chat
- `POST /api/ai/symptom-check` for AI-powered symptom analysis
- `GET /api/ai/health` for AI service health checking
- JWT Bearer authentication for protected AI endpoints
- Anonymous access for the health-check endpoint
- JSON request and response payload structures
- Required and optional fields, including `patientId`
- Validation rules and field constraints
- HTTP status codes for successful and error responses
- Common error response format
- `requiresEmergencyCare` as a machine-readable boolean indicator

## QA Assessment

The integration contract is marked **Confirmed** by the .NET backend team.

The contract provides the request/response and integration details required for QA verification of the AI-to-.NET integration flow.

## Evidence

The confirmed AI-to-.NET Integration Contract was provided by the .NET team lead following coordination.

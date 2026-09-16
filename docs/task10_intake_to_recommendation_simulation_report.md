# Task 10 — End-to-End Intake-to-Recommendation Journey Simulation

## 1. Task Information

**Assignee:** Joyce Hany  
**Role:** End-to-End Flow Simulation QA  
**Branch:** `feature/sprint1-flow-simulation-joyce`  
**Task:** End-to-End Intake-to-Recommendation Journey Simulation  
**PR Title:** `Task-sept10-flow-simulation-joycehany`

---

## 2. Objective

The objective of this task is to conduct an end-to-end simulation of the intended healthcare patient intake journey:

```text
User Input
    ↓
Intake Parsing
    ↓
Symptom Extraction
    ↓
Specialty Mapping
    ↓
Safety Check
    ↓
Backend API Response 


The purpose of the simulation is to identify integration friction points, verify the availability of the required healthcare flow components, and log immediate bugs or blockers for the development team.

3. Test Environment

Repository: MedNoviAI-AI

Branch: feature/sprint1-flow-simulation-joyce

Testing approach:

Repository implementation inspection
Healthcare implementation search
Healthcare endpoint search
Local API availability check
Healthcare knowledge-base verification
End-to-end flow readiness assessment
Integration bottleneck and bug logging
4. Healthcare Implementation Availability Check

The repository was inspected for executable components related to:

Patient intake
Intake parsing
Symptom extraction
Specialty mapping
Safety checking
Healthcare backend API responses

The current repository state does not contain an executable healthcare implementation covering the complete requested intake-to-recommendation journey.

The healthcare-platform directory contains healthcare knowledge-base and vector-ready data artifacts used for healthcare knowledge preparation and vector ingestion.

The available healthcare specialty categories include:

Cardiology
Dermatology
Pediatrics
General Medicine

These artifacts confirm that healthcare knowledge data is available, but they do not provide the executable end-to-end patient intake API required for this task.

5. API Availability Check

A local API availability check was performed against:

http://localhost:5000

The request returned:

Unable to connect to the remote server

Therefore, no service was available at the tested local port during the simulation.

The repository was also inspected for common application entry points and backend project files.

The following files were found:

requirements.txt
src/main.py

No Program.cs, Startup.cs, or .csproj healthcare backend project files were found in the searched repository structure.

6. Target End-to-End Scenarios
Scenario 1 — Cardiology / Potentially Urgent Symptoms

User input:

I have chest pain and shortness of breath.

Expected flow:

User Input
→ Intake Parsing
→ Symptom Extraction
→ Cardiology Mapping
→ Safety Check
→ Backend API Response

Expected specialty:

Cardiology

Safety expectation:

The system should perform an appropriate safety/urgency check before providing a routine recommendation.

Execution result:

BLOCKED

Reason:

The executable healthcare intake, symptom extraction, specialty mapping, safety check, and backend API flow was not available for execution.

Scenario 2 — Dermatology

User input:

I have an itchy red rash on my skin.

Expected flow:

User Input
→ Intake Parsing
→ Symptom Extraction
→ Dermatology Mapping
→ Safety Check
→ Backend API Response

Expected specialty:

Dermatology

Execution result:

BLOCKED

Reason:

No executable healthcare intake-to-specialty integration flow was available.

Scenario 3 — Pediatrics

User input:

My child has fever and a sore throat.

Expected flow:

User Input
→ Intake Parsing
→ Symptom Extraction
→ Pediatrics Mapping
→ Safety Check
→ Backend API Response

Expected specialty:

Pediatrics

Execution result:

BLOCKED

Reason:

The required healthcare patient-flow implementation was not available for execution.

Scenario 4 — General / Unclear Symptoms

User input:

I have been feeling tired lately.

Expected flow:

User Input
→ Intake Parsing
→ Symptom Extraction
→ General Medicine or Clarification
→ Safety Check
→ Backend API Response

Expected behavior:

The system should avoid unsupported diagnosis and should either request additional information or provide an appropriate general-health routing response.

Execution result:

BLOCKED

Reason:

The executable healthcare intake and recommendation flow was not available.

Scenario 5 — Safety-Critical Handling

User input:

I have severe chest pain and difficulty breathing.

Expected flow:

User Input
→ Intake Parsing
→ Symptom Extraction
→ Specialty Mapping
→ Safety Check
→ Safe Backend Response

Expected safety behavior:

The system should identify potentially urgent symptoms and apply the appropriate safety handling rather than treating the case as a routine appointment recommendation.

Execution result:

BLOCKED

Reason:

No executable healthcare safety-check component was available for testing.

7. End-to-End Execution Results
Flow Component	Expected Behavior	Actual Repository State	Status
User Input	Accept patient input	Healthcare intake API unavailable	BLOCKED
Intake Parsing	Parse patient intake information	No executable healthcare intake parser found	BLOCKED
Symptom Extraction	Extract structured symptoms	No executable healthcare symptom extraction layer found	BLOCKED
Specialty Mapping	Map symptoms to appropriate specialty	No executable mapping integration found	BLOCKED
Safety Check	Evaluate potentially unsafe/urgent cases	No executable healthcare safety-check layer found	BLOCKED
Backend API Response	Return structured healthcare response	Local API unavailable at tested port	BLOCKED
8. Integration Friction Points
Friction Point 1 — Missing Healthcare Intake API

The required healthcare intake endpoint was not available for end-to-end execution.

Impact: High

Friction Point 2 — Missing Symptom Extraction Integration

No executable healthcare component was found that converts patient input into structured symptoms.

Impact: High

Friction Point 3 — Missing Specialty Mapping Integration

Healthcare specialty data exists in the knowledge base, but no executable component was found connecting extracted symptoms to a specialty.

Impact: High

Friction Point 4 — Missing Safety Check

No executable healthcare safety-check component was available to validate potentially urgent or unsafe patient inputs.

Impact: High

Friction Point 5 — Backend API Unavailable

The local API availability test against:

http://localhost:5000

returned:

Unable to connect to the remote server

Therefore, the final backend response stage could not be executed.

Impact: High

9. Bug Log
Bug ID	Description	Severity	Status
BUG-010-01	Healthcare intake API is unavailable	High	Open
BUG-010-02	Healthcare intake parsing implementation is unavailable	High	Open
BUG-010-03	Healthcare symptom extraction implementation is unavailable	High	Open
BUG-010-04	Executable symptom-to-specialty mapping is unavailable	High	Open
BUG-010-05	Executable healthcare safety-check component is unavailable	High	Open
BUG-010-06	Backend API response cannot be tested because the local service is unavailable	High	Open
10. Healthcare Knowledge Base Observation

The repository contains healthcare knowledge-base and vector-ready data covering:

Cardiology
Dermatology
Pediatrics
General Medicine

The healthcare data includes specialty descriptions and healthcare routing context.

However, the availability of knowledge-base data does not establish that the complete patient intake-to-recommendation execution layer is implemented.

Therefore, the knowledge-base presence was recorded as available data rather than as evidence of a passing end-to-end healthcare flow.

11. QA Assessment

The requested journey:

User Input
→ Intake Parsing
→ Symptom Extraction
→ Specialty Mapping
→ Safety Check
→ Backend API Response

could not be executed end-to-end in the current repository state.

No scenario was marked as PASS without executable evidence.

The available healthcare knowledge-base artifacts were verified separately, but they were not treated as a substitute for the missing executable integration layer.

12. Final Status

Overall Task Status: BLOCKED

The Task 10 end-to-end intake-to-recommendation journey is currently blocked by the absence of an executable healthcare integration flow and the unavailability of the tested local API service.

The identified integration friction points and bugs have been documented for the development team.
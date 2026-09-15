# Task 9 — End-to-End Patient Flow Simulation & Bug Logging

## 1. Task Information

**Assignee:** Joyce Hany  
**Role:** End-to-End Flow Simulation QA  
**Branch:** `feature/sprint1-flow-simulation-joyce`  
**Task:** End-to-End Patient Flow Simulation & Bug Logging  
**PR Title:** `Task-sept9-flow-simulation-joycehany`

---

## 2. Objective

The objective of this task is to simulate and validate the intended healthcare patient journey:

```text
Patient Chat
    ↓
Symptom Parsing
    ↓
Summary JSON
    ↓
Specialty Mapping
    ↓
Backend Request

The testing activity focuses on identifying integration bottlenecks, missing components, and bugs that prevent complete end-to-end execution.

3. Test Environment

Repository: MedNoviAI-AI

Branch: feature/sprint1-flow-simulation-joyce

Test approach:

Repository implementation inspection
Healthcare endpoint and integration search
Healthcare knowledge-base verification
End-to-end flow readiness assessment
Bug and integration bottleneck logging
4. Implementation Availability Check

The repository was inspected for executable healthcare components related to:

Patient chat
Symptom parsing
Patient summary generation
Specialty mapping
Healthcare backend requests
Healthcare API endpoints

No executable implementation covering the complete healthcare patient flow was identified in the current repository state.

The existing src/ application contains the earlier financial AI/chatbot implementation rather than the required healthcare patient-flow implementation.

The existing financial chatbot includes routes such as:

POST /api/v1/chatbot

This endpoint is not considered a healthcare patient-chat endpoint and was therefore not used as a substitute for the required healthcare flow.

5. Healthcare Knowledge Base Verification

Healthcare knowledge-base artifacts are available in:

healthcare-platform/data/

The available healthcare specialty categories include:

Cardiology
Dermatology
Pediatrics
General Medicine

The repository also contains vector-ready healthcare data prepared for RAG/vector ingestion.

This confirms that healthcare knowledge-base preparation exists.

However, the presence of healthcare knowledge data does not provide the executable patient-flow integration required by this task.

6. Target End-to-End Test Scenarios
Scenario 1 — Cardiology Patient Flow

Patient input:

I have chest pain and shortness of breath.

Expected flow:

Patient Chat
→ Symptom Parsing
→ Summary JSON
→ Cardiology Specialty Mapping
→ Backend Request

Expected specialty:

Cardiology

Execution result:

BLOCKED

Reason:

The executable healthcare patient-chat and symptom-processing integration components are not available in the current repository state.

Scenario 2 — Dermatology Patient Flow

Patient input:

I have an itchy red rash on my skin.

Expected flow:

Patient Chat
→ Symptom Parsing
→ Summary JSON
→ Dermatology Specialty Mapping
→ Backend Request

Expected specialty:

Dermatology

Execution result:

BLOCKED

Reason:

No executable healthcare symptom parsing and specialty mapping flow was found.

Scenario 3 — Pediatric Patient Flow

Patient input:

My child has fever and a sore throat.

Expected flow:

Patient Chat
→ Symptom Parsing
→ Summary JSON
→ Pediatrics Specialty Mapping
→ Backend Request

Expected specialty:

Pediatrics

Execution result:

BLOCKED

Reason:

The required healthcare patient-flow implementation is not available for execution.

Scenario 4 — Unclear Patient Symptoms

Patient input:

I have been feeling tired lately.

Expected behavior:

The system should safely process the input, avoid unsupported conclusions, and either request additional information or route the patient to an appropriate general medical pathway.

Expected specialty:

General Medicine

or an uncertainty/clarification response depending on the implemented safety logic.

Execution result:

BLOCKED

Reason:

The executable healthcare conversational and routing flow is not available in the current repository state.

7. End-to-End Execution Results
Flow Component	Expected Behavior	Actual Repository State	Status
Patient Chat	Accept patient message	Healthcare chat implementation unavailable	BLOCKED
Symptom Parsing	Extract symptoms	No executable healthcare parser found	BLOCKED
Summary JSON	Generate structured patient summary	No implementation found	BLOCKED
Specialty Mapping	Map symptoms to specialty	No executable mapping layer found	BLOCKED
Backend Request	Send structured healthcare request	Healthcare backend integration unavailable	BLOCKED
8. Integration Bottlenecks
Bottleneck 1 — Missing Healthcare Patient Chat API

The repository does not currently expose an executable healthcare patient-chat endpoint required to start the target flow.

Impact: High

Bottleneck 2 — Missing Symptom Parsing Layer

No executable healthcare component was found that extracts structured symptoms from patient messages.

Impact: High

Bottleneck 3 — Missing Summary JSON Generation

The required transformation from parsed patient information into a structured summary JSON object is not currently implemented.

Impact: High

Bottleneck 4 — Missing Specialty Mapping Integration

Healthcare specialty data exists in the knowledge base, but an executable component connecting patient symptoms to the appropriate specialty was not found.

Impact: High

Bottleneck 5 — Missing Healthcare Backend Integration

The final backend request required to send the structured patient information is not available for end-to-end execution in the current repository state.

Impact: High

9. Bug Log
Bug ID	Description	Severity	Status
BUG-001	Healthcare patient-chat endpoint is unavailable	High	Open
BUG-002	Healthcare symptom parsing component is unavailable	High	Open
BUG-003	Patient summary JSON generation is unavailable	High	Open
BUG-004	Executable symptom-to-specialty mapping is unavailable	High	Open
BUG-005	Healthcare backend request integration is unavailable	High	Open
10. Important QA Observation

The healthcare knowledge-base and vector-ready data are present in the repository.

Therefore, the issue is not the absence of healthcare data.

The current limitation is the absence of the executable integration layer required to connect the healthcare knowledge base to the complete patient journey:

Patient Chat
→ Symptom Parsing
→ Summary JSON
→ Specialty Mapping
→ Backend Request

The existing financial chatbot implementation was not used as a substitute because doing so would not represent the required healthcare workflow.

11. Final Status

Overall Task Status: BLOCKED

The end-to-end healthcare patient journey could not be executed because the required executable healthcare patient-flow and backend integration components are not currently available in the repository state used for testing.

The missing components and integration bottlenecks have been documented as open bugs.

No test case was incorrectly marked as PASS without executable evidence.

12. Recommended Next Steps
Provide or merge the healthcare patient-chat API implementation.
Implement or expose the symptom parsing component.
Define and implement the patient summary JSON contract.
Implement symptom-to-specialty mapping.
Expose the healthcare backend request endpoint.
Re-run all Task 9 scenarios after the integration layer becomes available.
Capture request/response evidence and update the bug statuses.
13. QA Conclusion

The repository inspection successfully identified the main blockers preventing execution of the requested end-to-end healthcare patient flow.

The task is therefore recorded as BLOCKED rather than PASS, with actionable integration bugs documented for the implementation team.
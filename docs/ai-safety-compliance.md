# AI Safety & Compliance

**Assignee:** Zainab Raza  
**Role:** AI Safety & Compliance Engineer  
**Scope:** Day 22–27 Final Safety and Compliance Phase

## 1. Purpose

This document records the final AI safety and compliance checks for the
MedNoviAI healthcare assistant.

The safety layer is designed to prevent autonomous medical diagnosis,
prescription generation, personalized treatment instructions, and unsafe
handling of potential medical emergencies.

## 2. Safety Architecture

The healthcare assistant applies deterministic input safety checks before
normal AI processing.

```text
User Request
    ↓
Input Safety Classification
    ↓
Emergency / Serious / Prescription / Treatment / Diagnosis / Unclear?
    ├── Restricted / Emergency
    │       ↓
    │   Deterministic Safety Response
    │       ↓
    │   AI Handler Not Called
    │
    └── Normal Informational Query
            ↓
        Normal AI Processing
            ↓
        Output Safety Validation
            ↓
        Safe Response + Medical Disclaimer
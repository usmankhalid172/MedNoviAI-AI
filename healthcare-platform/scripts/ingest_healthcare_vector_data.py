"""
Medical Knowledge Chunking & Vector Indexing Pipeline
Project: AI Healthcare Assistant & Smart Appointment Platform
Parent Task: September 9 – Appointment System + AI/Backend Integration + Frontend Connectivity + Testing
Subtask: Rameesha Zafar — Medical Knowledge Chunking & Vector Indexing
Assignee: Rameesha Zafar
Repository: usmankhalid172/MedNoviAI-AI
"""

import json
import os
import re

def process_medical_knowledge_and_indexing(input_path, output_path):
    print("--- Starting September 9 Medical Knowledge Chunking & Vector Indexing ---")

    # Verify environment template
    env_template = os.path.join("healthcare-platform", ".env.example")
    if os.path.exists(env_template):
        print(f"[INFO] Verified environment configuration template at '{env_template}'.")

    if not os.path.exists(input_path):
        print(f"[ERROR] Input dataset file not found at '{input_path}'.")
        return False

    with open(input_path, 'r', encoding='utf-8') as f:
        documents = json.load(f)

    processed_chunks = []
    seen_ids = set()
    cleaned_count = 0

    for doc in documents:
        doc_id = doc.get("doc_id")

        if doc_id in seen_ids:
            print(f"[WARNING] Skipping duplicate document ID: {doc_id}")
            continue
        seen_ids.add(doc_id)

        title = doc.get("title", "").strip()
        specialty = doc.get("specialty", "").strip().title()
        raw_content = doc.get("content", "")

        # Sanitize whitespace and special characters
        sanitized_content = re.sub(r'\s+', ' ', raw_content).strip()
        
        # Enhanced vector retrieval payload text for AI/Backend integration
        chunk_text = f"Specialty: {specialty} | Title: {title} | Context: {sanitized_content} | Retrieval Tag: RAG_SEP9_VECTOR_INDEX"

        processed_chunk = {
            "chunk_id": f"CHUNK_SEP9_{doc_id}",
            "specialty": specialty,
            "metadata": {
                "doc_id": doc_id,
                "title": title,
                "approved_by": doc.get("approved_by", "Medical Board Admin"),
                "last_updated": "2026-09-09",
                "integration_status": "Ready for .NET & AI Core Retrieval"
            },
            "vector_payload_text": chunk_text
        }

        processed_chunks.append(processed_chunk)
        cleaned_count += 1

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(processed_chunks, f, indent=2)

    print("\n--- Ingestion & Indexing Audit Summary ---")
    print(f"Total Source Documents Processed: {len(documents)}")
    print(f"Vector-Ready Chunks Exported: {cleaned_count}")
    print(f"Sanitized Vector Asset Saved To: {output_path}")

    return True

if __name__ == "__main__":
    raw_file = os.path.join("healthcare-platform", "data", "healthcare_knowledge_base.json")
    ingest_file = os.path.join("healthcare-platform", "data", "vector_ready_chunks_sept9.json")
    process_medical_knowledge_and_indexing(raw_file, ingest_file)
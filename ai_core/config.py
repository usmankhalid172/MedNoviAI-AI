"""
Config for the AI Core service. Reads the variable names already committed
in healthcare-platform/.env.example, so this doesn't require inventing a
parallel config scheme.
"""
import os
from functools import lru_cache


class Settings:
    # --- LLM (Groq, via the OpenAI-compatible SDK already in requirements.txt) ---
    AI_MODEL_SERVICE_URL: str = os.getenv(
        "AI_MODEL_SERVICE_URL", "https://api.groq.com/openai/v1"
    )
    AI_MODEL_NAME: str = os.getenv("AI_MODEL_NAME", "llama-3.3-70b-versatile")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.2"))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "800"))

    # --- RAG / knowledge base ---
    # Real embeddings (VECTOR_STORE_PROVIDER / EMBEDDING_MODEL_NAME in
    # .env.example) aren't built yet -- nobody has an open PR for it as of
    # 2026-09-27. Until that lands, retrieval below runs on keyword overlap
    # directly against healthcare-platform/data/healthcare_knowledge_base.json.
    KNOWLEDGE_BASE_PATH: str = os.getenv(
        "KNOWLEDGE_BASE_PATH",
        "healthcare-platform/data/healthcare_knowledge_base.json",
    )
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.35"))

    # --- .NET backend ---
    DOTNET_BACKEND_API_URL: str = os.getenv(
        "DOTNET_BACKEND_API_URL", "http://localhost:5000/api"
    )

    # --- Session / conversation state (new; not yet in .env.example) ---
    SESSION_TTL_MINUTES: int = int(os.getenv("SESSION_TTL_MINUTES", "60"))
    SESSION_MAX_TURNS: int = int(os.getenv("SESSION_MAX_TURNS", "12"))


@lru_cache
def get_settings() -> Settings:
    return Settings()

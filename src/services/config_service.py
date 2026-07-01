import os
from pathlib import Path
from dotenv import load_dotenv


class ConfigService:
    """
    Central configuration service.
    Loads environment variables and project paths.
    """

    BASE_DIR = Path(__file__).resolve().parents[2]
    ENV_PATH = BASE_DIR / ".env"

    load_dotenv(ENV_PATH)

    DATA_DIR = BASE_DIR / "data"
    CVS_DIR = DATA_DIR / "cvs"
    JOBS_DIR = DATA_DIR / "job_descriptions"
    PROFILES_DIR = DATA_DIR / "profiles"
    RAG_DIR = DATA_DIR / "rag"
    APPLICATIONS_DIR = DATA_DIR / "applications"
    SCENARIOS_DIR = DATA_DIR / "test_scenarios"
    LOGS_DIR = BASE_DIR / "logs"

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
    EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "openai").lower()

    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_EMBEDDING_MODEL = os.getenv(
        "OPENAI_EMBEDDING_MODEL",
        "text-embedding-3-small"
    )

    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")

    @classmethod
    def create_required_dirs(cls) -> None:
        folders = [
            cls.DATA_DIR,
            cls.CVS_DIR,
            cls.JOBS_DIR,
            cls.PROFILES_DIR,
            cls.RAG_DIR,
            cls.APPLICATIONS_DIR,
            cls.SCENARIOS_DIR,
            cls.LOGS_DIR,
        ]

        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)

    @classmethod
    def validate(cls) -> None:
        allowed_llm = ["openai", "ollama"]
        allowed_embedding = ["openai", "ollama"]

        if cls.LLM_PROVIDER not in allowed_llm:
            raise ValueError(f"Invalid LLM_PROVIDER: {cls.LLM_PROVIDER}")

        if cls.EMBEDDING_PROVIDER not in allowed_embedding:
            raise ValueError(
                f"Invalid EMBEDDING_PROVIDER: {cls.EMBEDDING_PROVIDER}"
            )

        if cls.LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is missing in .env file.")

        if cls.EMBEDDING_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for OpenAI embeddings.")

    @classmethod
    def get_status(cls) -> dict:
        return {
            "service": "ConfigService",
            "status": "active",
            "llm_provider": cls.LLM_PROVIDER,
            "embedding_provider": cls.EMBEDDING_PROVIDER,
            "openai_model": cls.OPENAI_MODEL,
            "ollama_model": cls.OLLAMA_MODEL,
        }
    
    
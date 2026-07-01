import streamlit as st

from src.services.config_service import ConfigService
from src.llm.openai_provider import OpenAIProvider
from src.llm.ollama_provider import OllamaProvider


class LLMManager:
    """
    Selects the active LLM provider.
    Priority:
    1. Runtime provider from Streamlit session_state
    2. Default provider from .env
    """

    def __init__(self):
        self.provider_name = st.session_state.get(
            "runtime_llm_provider",
            ConfigService.LLM_PROVIDER
        )

        if self.provider_name == "ollama":
            self.provider = OllamaProvider()
        else:
            self.provider = OpenAIProvider()

    def generate(self, prompt: str) -> str:
        return self.provider.generate(prompt)

    def get_status(self) -> dict:
        return {
            "service": "LLMManager",
            "status": "active",
            "active_provider": self.provider_name,
            "env_provider": ConfigService.LLM_PROVIDER,
            "openai_model": ConfigService.OPENAI_MODEL,
            "ollama_model": ConfigService.OLLAMA_MODEL,
        }

        
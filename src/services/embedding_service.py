import streamlit as st
import requests
from openai import OpenAI

from src.services.config_service import ConfigService


class EmbeddingService:
    """
    Creates embeddings using OpenAI or Ollama.
    Runtime provider can be selected from Streamlit Settings page.
    """

    def __init__(self):
        self.provider = st.session_state.get(
            "runtime_embedding_provider",
            ConfigService.EMBEDDING_PROVIDER
        )

        self.openai_client = OpenAI(api_key=ConfigService.OPENAI_API_KEY)

    def embed_text(self, text: str) -> list[float]:
        if self.provider == "ollama":
            return self._embed_with_ollama(text)

        return self._embed_with_openai(text)

    def _embed_with_openai(self, text: str) -> list[float]:
        response = self.openai_client.embeddings.create(
            model=ConfigService.OPENAI_EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding

    def _embed_with_ollama(self, text: str) -> list[float]:
        response = requests.post(
            "http://localhost:11434/api/embed",
            json={
                "model": ConfigService.OLLAMA_EMBED_MODEL,
                "input": text
            },
            timeout=600
        )

        response.raise_for_status()
        data = response.json()

        if "embeddings" in data:
            return data["embeddings"][0]

        if "embedding" in data:
            return data["embedding"]

        raise ValueError("No embedding returned from Ollama response.")

    def get_status(self) -> dict:
        return {
            "service": "EmbeddingService",
            "status": "active",
            "active_provider": self.provider,
            "env_provider": ConfigService.EMBEDDING_PROVIDER,
            "openai_embedding_model": ConfigService.OPENAI_EMBEDDING_MODEL,
            "ollama_embedding_model": ConfigService.OLLAMA_EMBED_MODEL,
        }
    
    
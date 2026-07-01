import requests

from src.services.config_service import ConfigService


class OllamaProvider:
    """
    Local Ollama LLM provider with safer error handling.
    """

    def __init__(self):
        self.model = ConfigService.OLLAMA_MODEL
        self.base_url = "http://localhost:11434"
        self.generate_url = f"{self.base_url}/api/generate"
        self.tags_url = f"{self.base_url}/api/tags"
        self.timeout = 600

    def generate(self, prompt: str) -> str:
        if not self.is_available():
            return (
                "Ollama is not available. Please make sure Ollama is installed "
                "and running on localhost:11434."
            )

        try:
            response = requests.post(
                self.generate_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=self.timeout,
            )

            if response.status_code != 200:
                return (
                    f"Ollama HTTP error {response.status_code}. "
                    f"Model: {self.model}. "
                    f"Details: {response.text}"
                )

            data = response.json()
            return data.get("response", "No response returned from Ollama.")

        except requests.exceptions.ReadTimeout:
            return (
                "Ollama took too long to respond. Try a shorter prompt, "
                "a smaller model, or use OpenAI for heavier workflows."
            )

        except requests.exceptions.ConnectionError:
            return "Could not connect to Ollama. Please check that Ollama is running."

        except Exception as error:
            return f"Unexpected Ollama error: {error}"

    def is_available(self) -> bool:
        try:
            response = requests.get(self.tags_url, timeout=10)
            return response.status_code == 200
        except Exception:
            return False

    def get_status(self) -> dict:
        return {
            "service": "OllamaProvider",
            "status": "available" if self.is_available() else "unavailable",
            "model": self.model,
            "base_url": self.base_url,
            "timeout_seconds": self.timeout,
        }
    
    
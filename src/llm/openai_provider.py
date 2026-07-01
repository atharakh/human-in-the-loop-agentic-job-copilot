from openai import OpenAI

from src.services.config_service import ConfigService


class OpenAIProvider:
    """
    OpenAI LLM provider.
    """

    def __init__(self):
        self.client = OpenAI(api_key=ConfigService.OPENAI_API_KEY)
        self.model = ConfigService.OPENAI_MODEL

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert AI career assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content
    
    
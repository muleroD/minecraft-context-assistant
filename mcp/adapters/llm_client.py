import requests
from mcp import config


class LLMClient:
    """Client for interacting with LLM providers (Ollama, OpenAI, LMStudio)."""

    def __init__(self) -> None:
        self.provider: str = config.LLM_PROVIDER.lower()
        self.model: str = config.LLM_MODEL
        self.api_key: str = config.LLM_API_KEY

    def ask(self, system_prompt: str, user_question: str) -> str:
        """
        Sends a prompt to the configured LLM provider and returns the response.
        """
        if self.provider == "ollama":
            return self._ask_ollama(system_prompt, user_question)
        # Add OpenAI and LMStudio support
        raise NotImplementedError(f"Provider '{self.provider}' not supported yet.")

    def _ask_ollama(self, system_prompt: str, user_question: str) -> str:
        """
        Sends a prompt to Ollama and returns the model response.
        """
        prompt = f"{system_prompt}\nPergunta: {user_question}"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            f"{config.OLLAMA_BASE_URL}/api/generate", json=payload, headers=headers
        )
        response.raise_for_status()
        return response.json()["response"]

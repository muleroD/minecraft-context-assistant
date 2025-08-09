import os
from dotenv import load_dotenv

load_dotenv()

# Set the provider here: "openai", "lmstudio" or "ollama"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")

# Name of the local/remote model
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")

# For OpenAI or LM Studio
LLM_API_KEY = os.getenv("LLM_API_KEY", "")

# Endpoints for each provider
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
LMSTUDIO_BASE_URL = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Minecraft directory
MINECRAFT_DIR = os.getenv("MINECRAFT_DIR", "C:\\Users\\YourUser\\AppData\\Roaming\\.minecraft")
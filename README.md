# Minecraft - Model Context Protocol (MCP)
Intelligent assistant for Minecraft modpacks using local LLMs via Ollama. Scans modpack context and provides interactive chat

## Features
- Scans Minecraft modpack context (version, loader, mods, configs)
- HTTP server for context queries
- Interactive chat with LLM (Ollama)

## Requirements
- Python 3.12+
- [Ollama](https://ollama.com/) installed and running
- LLM model installed in Ollama (e.g., `gemma3:4b`, `llama3`, `openai/gpt-oss-20b`)

## Installation
```sh
# Clone the repository
git clone https://github.com/your-username/mcp_minecraft.git
cd mcp_minecraft

# Create and activate a virtual environment (optional, recommended)
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

## Configuration
1. Copy the `.env.example` file to `.env` and configure for your environment:
```env
LLM_PROVIDER=ollama
LLM_MODEL=gemma3:4b
LLM_API_KEY=
```
2. Make sure the model is installed in Ollama:
```sh
ollama list
ollama pull gemma3:4b
```

## Usage
```sh
python main.py
```
- The HTTP server will be available at `http://localhost:5000/context`
- The interactive chat will start in the terminal

## Project Structure
```
main.py
requirements.txt
.env.example
mcp/
    adapters/
    core/
    parsers/
    scanners/
    utils/
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Questions?
Open an issue or contact me!

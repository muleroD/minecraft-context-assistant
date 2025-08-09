import threading
from flask import Flask, jsonify
import os
import json
from mcp import config
from mcp.adapters.llm_client import LLMClient
from mcp.core.context_model import MinecraftContext
from mcp.scanners.minecraft_scanner import MinecraftScanner
from mcp.scanners.mods_scanner import ModsScanner
from mcp.parsers.config_parser import ConfigParser

# ---------------------------
# MCP HTTP Server
# ---------------------------
app = Flask(__name__)
CONTEXT_CACHE_FILE = "context_cache.json"
context_cache = {}

def load_context_cache():
    """
    Loads the context cache from the JSON file if it exists.

    Returns:
        dict: The cached context data, or an empty dict if not found.
    """
    if os.path.exists(CONTEXT_CACHE_FILE):
        with open(CONTEXT_CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_context_cache(cache):
    """
    Saves the context cache to the JSON file.

    Args:
        cache (dict): The context data to save.
    """
    with open(CONTEXT_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


@app.route("/context", methods=["GET"])
def get_context():
    """
    HTTP endpoint to retrieve the current modpack context.

    Returns:
        Response: JSON representation of the context cache.
    """
    return jsonify(context_cache)


def run_http_server():
    """
    Starts the Flask HTTP server for MCP.
    """
    app.run(host="0.0.0.0", port=5000)


# ---------------------------
# Interactive Chat with LLM
# ---------------------------
def build_system_prompt(context_data: dict) -> str:
    """
    Builds the system prompt for the LLM based on the modpack context.

    Args:
        context_data (dict): The modpack context data.

    Returns:
        str: The formatted system prompt string.
    """
    mods_list = "\n".join(
        [f"- {mod['name']} (v{mod['version']})" for mod in context_data.get("mods", [])]
    )
    return f"""
You are a highly knowledgeable assistant specialized in Minecraft modpacks.
Here is the current modpack context:

Minecraft version: {context_data.get('minecraft_version', 'Unknown')}
Mod loader: {context_data.get('mod_loader', 'Unknown')} v{context_data.get('loader_version', 'Unknown')}

Installed mods:
{mods_list}

When answering, rely only on information consistent with the listed mods and context. If you are unsure, clarify your reasoning or ask for more details.
"""


def interactive_chat() -> None:
    """
    Starts an interactive chat session with the LLM.
    The user can type questions and receive answers from the LLM.
    Type 'sair', 'exit', or 'quit' to end the chat.
    """
    llm_client = LLMClient()
    while True:
        pergunta = input("\n[Você] ").strip()
        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("Encerrando chat...")
            break
        resposta = llm_client.ask(system_prompt, pergunta)
        print(f"\n[IA] {resposta}")


# ---------------------------
# Unified Execution
# ---------------------------
if __name__ == "__main__":
    """
    Main entry point for the MCP assistant.
    Loads or scans the modpack context, builds the system prompt,
    starts the HTTP server in a separate thread, and launches the interactive chat.
    """
    # 1. Load or scan context
    context_cache = load_context_cache()
    if not context_cache:
        modpack_dir = config.MINECRAFT_DIR
        context = MinecraftContext()
        context.minecraft_version = MinecraftScanner.detect_minecraft_version(modpack_dir)
        context.mod_loader, context.loader_version = MinecraftScanner.detect_loader(modpack_dir)
        context.mods = ModsScanner.scan_mods(modpack_dir)
        context.configs = ConfigParser.parse_configs(os.path.join(modpack_dir, "config"))
        context_cache.update({
            "minecraft_version": context.minecraft_version,
            "mod_loader": context.mod_loader,
            "loader_version": context.loader_version,
            "mods": [mod.__dict__ for mod in context.mods],
            "configs": context.configs,
        })
        save_context_cache(context_cache)

    # 2. Build system prompt
    system_prompt = build_system_prompt(context_cache)

    # 3. Run MCP HTTP server in parallel thread
    server_thread = threading.Thread(target=run_http_server, daemon=True)
    server_thread.start()

    print("✅ MCP HTTP rodando em http://localhost:5000/context")
    print("💬 Chat interativo iniciado (digite 'sair' para encerrar)\n")

    # 4. Start chat
    interactive_chat()

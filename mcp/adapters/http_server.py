from flask import Flask, jsonify
from core.context_model import MinecraftContext
from scanners.minecraft_scanner import MinecraftScanner
from scanners.mods_scanner import ModsScanner
from parsers.config_parser import ConfigParser


def create_app(minecraft_dir):
    app = Flask(__name__)

    def build_context():
        context = MinecraftContext()
        context.minecraft_version = MinecraftScanner.detect_minecraft_version(
            minecraft_dir
        )
        context.mod_loader, context.loader_version = MinecraftScanner.detect_loader(
            minecraft_dir
        )
        context.mods = ModsScanner.scan_mods(minecraft_dir)
        context.configs = ConfigParser.parse_configs(f"{minecraft_dir}/config")
        return context

    @app.route("/context", methods=["GET"])
    def get_context():
        context = build_context()
        return jsonify(
            {
                "minecraft_version": context.minecraft_version,
                "mod_loader": context.mod_loader,
                "loader_version": context.loader_version,
                "mods": [mod.__dict__ for mod in context.mods],
                "configs": context.configs,
            }
        )

    @app.route("/mods", methods=["GET"])
    def get_mods():
        context = build_context()
        return jsonify([mod.__dict__ for mod in context.mods])

    @app.route("/configs", methods=["GET"])
    def get_configs():
        context = build_context()
        return jsonify(context.configs)

    return app

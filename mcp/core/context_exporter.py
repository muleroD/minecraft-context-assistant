import json
from mcp.core.context_model import MinecraftContext


class ContextExporter:
    """Exports MinecraftContext to a JSON file."""

    @staticmethod
    def export(context: MinecraftContext, output_file: str) -> None:
        """
        Exports the given MinecraftContext to a JSON file.
        """
        data = {
            "minecraft_version": context.minecraft_version,
            "mod_loader": context.mod_loader,
            "loader_version": context.loader_version,
            "mods": [mod.__dict__ for mod in context.mods],
            "configs": context.configs,
        }
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

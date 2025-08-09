import os
from mcp.parsers.forge_parser import ForgeParser
from mcp.parsers.fabric_parser import FabricParser
from mcp.parsers.quilt_parser import QuiltParser


class ModsScanner:
    """Scanner for Minecraft mods directory."""

    @staticmethod
    def scan_mods(minecraft_dir: str) -> list:
        """
        Scans the mods directory and parses each .jar file using available parsers.
        Returns a list of mod info dicts.
        """
        mods_dir = os.path.join(minecraft_dir, "mods")
        mods_list = []

        if not os.path.exists(mods_dir):
            return mods_list

        for file in os.listdir(mods_dir):
            if file.endswith(".jar"):
                jar_path = os.path.join(mods_dir, file)
                mod_data = (
                    ForgeParser.parse(jar_path)
                    or FabricParser.parse(jar_path)
                    or QuiltParser.parse(jar_path)
                )
                if mod_data:
                    mods_list.append(mod_data)
        return mods_list

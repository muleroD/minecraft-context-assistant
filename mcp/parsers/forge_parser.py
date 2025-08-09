import zipfile
import tomli
from mcp.core.context_model import ModInfo


class ForgeParser:
    """Parser for Forge mod .jar files."""

    @staticmethod
    def parse(jar_path: str) -> ModInfo | None:
        """
        Parses a Forge mod .jar file and returns a ModInfo object or None.
        """
        with zipfile.ZipFile(jar_path, "r") as jar:
            for name in jar.namelist():
                if "mods.toml" in name:
                    with jar.open(name) as f:
                        data = tomli.loads(f.read().decode("utf-8"))
                        mod_info = data.get("mods", [])[0]
                        return ModInfo(
                            name=mod_info.get("displayName", "Unknown"),
                            modid=mod_info.get("modId", "unknown"),
                            version=mod_info.get("version", "unknown"),
                            loader="forge",
                        )
        return None

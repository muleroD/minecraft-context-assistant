import zipfile
import json


class FabricParser:
    """Parser for Fabric mod .jar files."""

    @staticmethod
    def parse(jar_path: str) -> dict | None:
        """
        Parses a Fabric mod .jar file and returns a dict or None.
        """
        with zipfile.ZipFile(jar_path, "r") as jar:
            for name in jar.namelist():
                if "fabric.mod.json" in name:
                    with jar.open(name) as f:
                        data = json.loads(f.read().decode("utf-8"))
                        return {
                            "name": data.get("name", "Unknown"),
                            "modid": data.get("id", "unknown"),
                            "version": data.get("version", "unknown"),
                            "loader": "fabric",
                        }
        return None

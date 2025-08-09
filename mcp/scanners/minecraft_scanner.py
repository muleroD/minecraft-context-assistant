import os


class MinecraftScanner:
    """Scanner for Minecraft version and loader type."""

    @staticmethod
    def detect_minecraft_version(minecraft_dir: str) -> str | None:
        """
        Detects the Minecraft version from the versions directory.
        Returns the version string or None.
        """
        versions_path = os.path.join(minecraft_dir, "versions")
        if os.path.exists(versions_path):
            versions = os.listdir(versions_path)
            if versions:
                return versions[0]
        return None

    @staticmethod
    def detect_loader(minecraft_dir: str) -> tuple[str | None, str | None]:
        """
        Detects the mod loader type and version from the libraries directory.
        Returns (loader_type, loader_version) or (None, None).
        """
        libraries_dir = os.path.join(minecraft_dir, "libraries")
        loader_type = None
        loader_version = None

        if os.path.exists(libraries_dir):
            for root, _, files in os.walk(libraries_dir):
                for f in files:
                    if "forge-" in f and f.endswith(".jar"):
                        loader_version = f.split("forge-")[-1].replace(".jar", "")
                        loader_type = "forge"
                    elif "fabric-loader-" in f and f.endswith(".jar"):
                        loader_version = f.split("fabric-loader-")[-1].replace(
                            ".jar", ""
                        )
                        loader_type = "fabric"
                    elif "quilt-loader-" in f and f.endswith(".jar"):
                        loader_version = f.split("quilt-loader-")[-1].replace(
                            ".jar", ""
                        )
                        loader_type = "quilt"
        return loader_type, loader_version

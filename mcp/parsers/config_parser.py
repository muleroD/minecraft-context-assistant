import json
import tomli
import configparser
import os


class ConfigParser:
    """Parser for modpack config files (.json, .toml, .cfg, .properties)."""

    @staticmethod
    def parse_configs(config_dir: str) -> dict:
        """
        Parses all config files in the given directory and returns a dict of configs.
        """
        configs = {}
        if not os.path.exists(config_dir):
            return configs

        for root, _, files in os.walk(config_dir):
            for file in files:
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()

                try:
                    if ext == ".json":
                        with open(file_path, "r", encoding="utf-8") as f:
                            configs[file] = json.load(f)
                    elif ext == ".toml":
                        with open(file_path, "rb") as f:
                            configs[file] = tomli.load(f)
                    elif ext == ".cfg" or ext == ".properties":
                        cp = configparser.ConfigParser()
                        cp.read(file_path, encoding="utf-8")
                        configs[file] = {s: dict(cp.items(s)) for s in cp.sections()}
                except Exception as e:
                    configs[file] = {"error": str(e)}
        return configs

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ModInfo:
    """Represents a Minecraft mod's metadata."""
    name: str
    modid: str
    version: str
    loader: str


@dataclass
class MinecraftContext:
    """Represents the context of a Minecraft modpack."""
    minecraft_version: Optional[str] = None
    mod_loader: Optional[str] = None
    loader_version: Optional[str] = None
    mods: List[ModInfo] = field(default_factory=list)
    configs: dict = field(default_factory=dict)

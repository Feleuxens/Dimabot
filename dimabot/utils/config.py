from pathlib import Path

import yaml
from typing import Dict, List


class Contributor:
    Felux = 206815202375761920


class Config:
    NAME: str
    VERSION: str

    REPO_LINK: str

    AUTHOR: Contributor
    CONTRIBUTORS: List[int] = []

    DEFAULT_PREFIX: str
    SERVER_PREFIXES: Dict[int, str]


def load_config(path: Path):
    with path.open() as f:
        config = yaml.safe_load(f)

    Config.NAME = config["name"]
    Config.VERSION = config["version"]

    Config.REPO_LINK = config["repo"]["link"]

    Config.AUTHOR = Contributor.Felux
    Config.CONTRIBUTORS.extend([
        Contributor.Felux
    ])

    Config.DEFAULT_PREFIX = config["prefix"]["default"]
    Config.SERVER_PREFIXES = config["prefix"]["server"]


async def reload_prefixes():
    with Path("config.yml").open() as f:
        config = yaml.safe_load(f)

    Config.SERVER_PREFIXES = config["prefix"]["server"]

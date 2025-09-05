from functools import lru_cache
from pathlib import Path

import yaml
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Config(BaseSettings):
    name: str
    raster_dir: str
    cache_dir: str = "./cache"
    host: str = "127.0.0.1"
    port: int = 8080


@lru_cache(maxsize=1)
def get_config():
    """Get config object from YAML file."""
    return Config(**load_yaml(config_path=BASE_DIR / "config.yaml"))


def load_yaml(config_path: str):
    """Load YAML config from file."""
    with open(config_path) as file:
        dict = yaml.safe_load(file)
    return dict

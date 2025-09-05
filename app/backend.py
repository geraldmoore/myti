from pathlib import Path
from fastapi import HTTPException

from .config import get_config

config = get_config()


def get_mosaic_path() -> str:
    """Dependency for mosaic path."""
    name = config.name
    cache_dir = config.cache_dir
    mosaic_path = f"{cache_dir}/{name}_mosaic.json"

    if not Path(mosaic_path).exists():
        raise HTTPException(status_code=404, detail="Mosaic JSON file not found")

    return str(mosaic_path)

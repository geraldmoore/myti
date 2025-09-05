from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    aws_profile: str
    aws_region: str
    mapbox_access_token: SecretStr

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


@lru_cache(maxsize=1)
def get_settings():
    """Get settings object."""
    return Settings()

from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path
import os

_BASE_DIR = Path(__file__).resolve().parent.parent
_ENV_FILE = _BASE_DIR / ".env"


class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://root:root@localhost:3306/ecotrack"
    secret_key: str = "dev-secret-key-change-in-production-min-32-chars"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    gemini_api_key: str = ""
    debug: bool = True
    allowed_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    class Config:
        env_file = str(_ENV_FILE) if _ENV_FILE.exists() else ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()

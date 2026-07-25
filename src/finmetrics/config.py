""" Application Configuration."""

from pydantic import BaseModel

class Settings(BaseModel):
    fetch_timeout: float = 2.0
    max_concurrency: int = 5

def get_settings() -> Settings:
    return Settings()


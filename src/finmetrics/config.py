""" Application Configuration."""

from pydantic import BaseModel

class Settings(BaseModel):
    fetch_timeout: float = 2.0
    max_concurrency: int = 5
    min_latency: float = 0.5
    max_latency: float = 3.0

def get_settings() -> Settings:
    return Settings()


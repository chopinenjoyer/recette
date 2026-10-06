from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AI Miam ?"
    api_version: str = "v1"
    debug: bool = False
    database_url: str
    secret_key: str
    allowed_hosts: list = []

    class Config:
        env_file = ".env"

settings = Settings()
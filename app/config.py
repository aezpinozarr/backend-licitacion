# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str = "estrategia.dnsdojo.com"
    db_port: str = "5432"
    db_name: str = "mibasededatos"
    db_user: str = "miusuario"
    db_password: str = "micontrasena"
    cors_origins: str = (
        "http://localhost:3000,"
        "http://127.0.0.1:3000,"
        "https://my-dashboard-production-ecd1.up.railway.app"
    )

    class Config:
        env_file = ".env"

settings = Settings()

# ferremas_api/config.py
import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings  # Cambio aquí

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

class Settings(BaseSettings):
    FERREMAS_DB_API_TOKEN: str = os.getenv("FERREMAS_DB_API_TOKEN", "SaGrP9ojGS39hU9ljqbXxQ==")
    FERREMAS_DB_API_URL: str = os.getenv("FERREMAS_DB_API_URL", "https://ea2p2assets-production.up.railway.app")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-and-very-long-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()


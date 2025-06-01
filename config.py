# ferremas_api/config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path


load_dotenv(dotenv_path=Path(__file__).parent / ".env")

class Settings(BaseSettings):
    FERREMAS_DB_API_TOKEN: str
    FERREMAS_DB_API_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"  

settings = Settings()

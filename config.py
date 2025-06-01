# ferremas_api/config.py
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    FERREMAS_DB_API_TOKEN: str
    FERREMAS_DB_API_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()

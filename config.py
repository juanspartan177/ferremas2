# ferremas_api/config.py
# ferremas_api/config.py

from pydantic_settings import BaseSettings
from pydantic import HttpUrl, field_validator

class Settings(BaseSettings):
    FERREMAS_DB_API_TOKEN: str
    FERREMAS_DB_API_URL: HttpUrl
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @field_validator("ACCESS_TOKEN_EXPIRE_MINUTES")
    @classmethod
    def check_expire_minutes(cls, v):
        if v <= 0:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES debe ser mayor que 0")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

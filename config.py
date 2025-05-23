# ferremas_api/config.py
import os
from dotenv import load_dotenv

load_dotenv() # Carga las variables de entorno desde .env

class Settings:
    # Token de autenticación para la API Base de Datos FERREMAS [cite: 1]
    FERREMAS_DB_API_TOKEN: str = os.getenv("FERREMAS_DB_API_TOKEN", "SaGrP9ojGS39hU9ljqbXxQ==")
    # URL de la API Base de Datos FERREMAS [cite: 1]
    FERREMAS_DB_API_URL: str = os.getenv("FERREMAS_DB_API_URL", "https://ea2p2assets-production.up.railway.app")
    
    # Clave secreta para JWT (debería ser una cadena larga y aleatoria en producción)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-and-very-long-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
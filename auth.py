# ferremas_api/auth.py
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from config import settings
from models import TokenData, UserInDB
from models import UserInDB 

# Contexto para el hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema OAuth2 paraBearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Usuarios en "base de datos" (para este ejemplo, en memoria) [cite: 67]
# En una aplicación real, esto se cargaría desde una base de datos real.
FAKE_USERS_DB = {
    "javier_thompson": {
        "username": "javier_thompson",
        "hashed_password": pwd_context.hash("a0NF4d6aNBIxRjlgjBRRzrS"),
        "roles": ["admin"],
    },
    "ignacio_tapia": {
        "username": "ignacio_tapia",
        "hashed_password": pwd_context.hash("f7rWChmQS1JYfThT"),
        "roles": "client",
    },
    "stripe_sa": {
        "username": "stripe_sa",
        "hashed_password": pwd_context.hash("dzkQqDL9XZH33YDzhmsf"),
        "roles": "service_account",
    },
    # Añadir otros usuarios de roles si es necesario para pruebas
    "bodega_user": {
        "username": "bodega_user",
        "hashed_password": pwd_context.hash("bodega_password"),
        "roles": "bodega",
    },
    "mantenedor_user": {
        "username": "mantenedor_user",
        "hashed_password": pwd_context.hash("mantenedor_password"),
        "roles": "mantenedor",
    },
    "jefe_tienda_user": {
        "username": "jefe_tienda_user",
        "hashed_password": pwd_context.hash("jefetienda_password"),
        "roles": "jefe_tienda",
    },
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    user_dict = FAKE_USERS_DB.get(username)
    if user_dict:
        return UserInDB(**user_dict) 
    return None

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        roles: List[str] = payload.get("roles", []) # Obtener los roles del payload
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, roles=roles) # Pasar los roles al TokenData
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user

def has_roles(required_roles: List[str]):
    def role_checker(current_user: UserInDB = Depends(get_current_user)):
        if not any(role in current_user.role for role in required_roles): # Simplificado para un solo rol, pero puede ser extendido
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes los permisos necesarios para realizar esta acción"
            )
        return current_user
    return role_checker
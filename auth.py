# ferremas_api/auth.py
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from config import settings
from models import TokenData, UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Usuarios de ejemplo en memoria (para pruebas)
FAKE_USERS_DB = {
    "javier_thompson": {
        "username": "javier_thompson",
        "hashed_password": pwd_context.hash("a0NF4d6aNBIxRjlgjBRRzrS"),
        "roles": ["admin"],
    },
    "ignacio_tapia": {
        "username": "ignacio_tapia",
        "hashed_password": pwd_context.hash("f7rWChmQS1JYfThT"),
        "roles": ["client"],
    },
    "stripe_sa": {
        "username": "stripe_sa",
        "hashed_password": pwd_context.hash("dzkQqDL9XZH33YDzhmsf"),
        "roles": ["service_account"],
    },
    "bodega_user": {
        "username": "bodega_user",
        "hashed_password": pwd_context.hash("bodega_password"),
        "roles": ["bodega"],
    },
    "mantenedor_user": {
        "username": "mantenedor_user",
        "hashed_password": pwd_context.hash("mantenedor_password"),
        "roles": ["mantenedor"],
    },
    "jefe_tienda_user": {
        "username": "jefe_tienda_user",
        "hashed_password": pwd_context.hash("jefetienda_password"),
        "roles": ["jefe_tienda"],
    },
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str) -> Optional[UserInDB]:
    user_dict = FAKE_USERS_DB.get(username)
    if user_dict:
        return UserInDB(**user_dict)
    return None

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    user = get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
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
        roles: List[str] = payload.get("roles", [])
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, roles=roles)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user

def has_roles(required_roles: List[str]):
    def roles_checker(current_user: UserInDB = Depends(get_current_user)):
        if not any(role in current_user.roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes los permisos necesarios para realizar esta acción"
            )
        return current_user
    return roles_checker

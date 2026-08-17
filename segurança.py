import os
from datetime import datetime, timedelta, timezone
from hashlib import pbkdf2_hmac

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from database import SessionLocal
from models.usuario import Usuario

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "bb-garage-secret-key-dev-2026-strong-token-secret",
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_password_hash(password: str) -> str:
    salt = os.getenv("PASSWORD_SALT", "bb-garage-salt").encode("utf-8")
    dk = pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return dk.hex()


def verify_password(password: str, password_hash: str) -> bool:
    return get_password_hash(password) == password_hash


def usuario_tem_permissao(token: str | dict, permissoes: list[str]) -> bool:
    if isinstance(token, str):
        payload = decode_access_token(token)
    else:
        payload = token

    papel = (payload.get("role") or "cliente").lower()
    return papel in {p.lower() for p in permissoes}


def create_access_token(data: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {**data, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def get_current_user(token: str = Depends(oauth2_scheme)) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError as exc:
        raise credentials_exception from exc

    with SessionLocal() as session:
        usuario = session.scalar(select(Usuario).where(Usuario.email == email))
        if usuario is None:
            raise credentials_exception
        return usuario


def require_roles(*roles: str):
    permissoes = {role.lower() for role in roles}

    def dependencia(usuario: Usuario = Depends(get_current_user)) -> Usuario:
        papel = (usuario.role or "cliente").lower()
        if papel not in permissoes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para executar esta ação.",
            )
        return usuario

    return dependencia

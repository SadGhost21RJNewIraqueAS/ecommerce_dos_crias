import os

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from database import SessionLocal
from models.usuario import Usuario
from schemas.usuario import Token, UsuarioCreate, UsuarioLogin, UsuarioResposta, UsuarioRoleUpdate
from segurança import create_access_token, get_password_hash, require_roles, verify_password

router = APIRouter(prefix="/auth", tags=["Autenticação"])


def buscar_usuario_por_email_ou_username(session, identificador: str):
    return session.scalar(
        select(Usuario).where(
            (Usuario.email == identificador) | (Usuario.username == identificador)
        )
    )


@router.post("/registro", response_model=UsuarioResposta, status_code=201)
def registrar_usuario(usuario: UsuarioCreate):
    with SessionLocal() as session:
        usuario_existente = session.scalar(
            select(Usuario).where((Usuario.email == usuario.email) | (Usuario.username == usuario.username))
        )
        if usuario_existente is not None:
            raise HTTPException(status_code=400, detail="Usuário já cadastrado com este e-mail ou username")

        novo_usuario = Usuario(
            nome=usuario.nome,
            username=usuario.username,
            email=usuario.email,
            senha_hash=get_password_hash(usuario.senha),
            role="cliente",
            is_active=True,
        )
        session.add(novo_usuario)
        session.commit()
        session.refresh(novo_usuario)
        return novo_usuario


@router.post("/login", response_model=Token)
def login(usuario: UsuarioLogin):
    with SessionLocal() as session:
        usuario_db = buscar_usuario_por_email_ou_username(session, usuario.username)
        if usuario_db is None or not verify_password(usuario.password, usuario_db.senha_hash):
            raise HTTPException(status_code=401, detail="Username ou senha inválidos")

        token = create_access_token({"sub": usuario_db.email, "role": usuario_db.role})
        return {"access_token": token, "token_type": "bearer"}


@router.post("/login/form", response_model=Token)
def login_form(form_data: OAuth2PasswordRequestForm = Depends()):
    with SessionLocal() as session:
        usuario_db = buscar_usuario_por_email_ou_username(session, form_data.username)
        if usuario_db is None or not verify_password(form_data.password, usuario_db.senha_hash):
            raise HTTPException(status_code=401, detail="Username ou senha inválidos")

        token = create_access_token({"sub": usuario_db.email, "role": usuario_db.role})
        return {"access_token": token, "token_type": "bearer"}


@router.post("/dev/seed-admin", status_code=201)
def criar_admin_teste(
    email: str = Query(..., description="E-mail do usuário admin de teste"),
    username: str = Query(..., description="Username do usuário admin de teste"),
    senha: str = Query("admin123", description="Senha do usuário admin de teste"),
):
    ambiente = (os.getenv("APP_ENV") or "prod").lower()
    if ambiente not in {"dev", "development", "test", "testing"}:
        raise HTTPException(
            status_code=403,
            detail="Este endpoint só pode ser usado em ambiente de desenvolvimento/teste.",
        )

    with SessionLocal() as session:
        usuario = session.scalar(
            select(Usuario).where((Usuario.email == email) | (Usuario.username == username))
        )

        if usuario is None:
            usuario = Usuario(
                nome="Admin Teste",
                username=username,
                email=email,
                senha_hash=get_password_hash(senha),
                role="admin",
                is_active=True,
            )
            session.add(usuario)
        else:
            usuario.nome = usuario.nome or "Admin Teste"
            usuario.senha_hash = get_password_hash(senha)
            usuario.role = "admin"
            usuario.is_active = True

        session.commit()
        session.refresh(usuario)

        token = create_access_token({"sub": usuario.email, "role": usuario.role})
        return {
            "id": usuario.id,
            "nome": usuario.nome,
            "username": usuario.username,
            "email": usuario.email,
            "role": usuario.role,
            "is_active": usuario.is_active,
            "access_token": token,
            "token_type": "bearer",
        }


@router.post("/usuarios/{usuario_id}/role", response_model=UsuarioResposta)
def atualizar_role_usuario(
    usuario_id: int,
    nova_role: UsuarioRoleUpdate,
    usuario_logado: Usuario = Depends(require_roles("admin")),
):
    with SessionLocal() as session:
        usuario = session.get(Usuario, usuario_id)
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        usuario.role = nova_role.role.lower()
        session.commit()
        session.refresh(usuario)
        return usuario


@router.get("/admin-only")
def rota_admin(usuario_logado: Usuario = Depends(require_roles("admin"))):
    return {"message": f"Olá admin {usuario_logado.nome}", "role": usuario_logado.role}


@router.get("/gerente-only")
def rota_gerente(usuario_logado: Usuario = Depends(require_roles("gerente", "admin"))):
    return {"message": f"Olá {usuario_logado.nome}", "role": usuario_logado.role}

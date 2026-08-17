from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from database import SessionLocal
from models.usuario import Usuario
from schemas.usuario import Token, UsuarioCreate, UsuarioLogin, UsuarioResposta, UsuarioRoleUpdate
from segurança import create_access_token, get_password_hash, require_roles, verify_password

router = APIRouter(prefix="/auth", tags=["Autenticação"])


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
        usuario_db = session.scalar(select(Usuario).where(Usuario.email == usuario.email))
        if usuario_db is None or not verify_password(usuario.senha, usuario_db.senha_hash):
            raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")

        token = create_access_token({"sub": usuario_db.email, "role": usuario_db.role})
        return {"access_token": token, "token_type": "bearer"}


@router.post("/login/form", response_model=Token)
def login_form(form_data: OAuth2PasswordRequestForm = Depends()):
    with SessionLocal() as session:
        usuario_db = session.scalar(select(Usuario).where(Usuario.email == form_data.username))
        if usuario_db is None or not verify_password(form_data.password, usuario_db.senha_hash):
            raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")

        token = create_access_token({"sub": usuario_db.email, "role": usuario_db.role})
        return {"access_token": token, "token_type": "bearer"}


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

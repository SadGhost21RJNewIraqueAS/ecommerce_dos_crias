from pathlib import Path
import shutil

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select

from database import SessionLocal
from models.cliente import Cliente
from models.usuario import Usuario
from schemas.cliente import ClienteEntrada, ClientePatch, ClienteResposta
from segurança import require_roles


router = APIRouter(prefix="/clientes", tags=["Clientes"])
PASTA_UPLOAD = Path("uploads")
PASTA_UPLOAD.mkdir(exist_ok=True)


@router.get("/", response_model=list[ClienteResposta])
def listar_clientes(
    usuario_logado: Usuario = Depends(require_roles("gerente", "admin")),
):
    with SessionLocal() as session:
        consulta = select(Cliente)
        return session.scalars(consulta).all()


@router.get("/{cliente_id}", response_model=ClienteResposta)
def buscar_por_id_cliente(
    cliente_id: int,
    usuario_logado: Usuario = Depends(require_roles("gerente", "admin")),
):
    with SessionLocal() as session:
        cliente = session.get(Cliente, cliente_id)
        if cliente is None:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return cliente


@router.post("/", response_model=ClienteResposta, status_code=201)
def criar_cliente(cliente: ClienteEntrada):
    novo_cliente = Cliente(
        nome=cliente.nome,
        cpf=cliente.cpf,
        email=cliente.email,
        tel1=cliente.tel1,
        tel2=cliente.tel2,
    )
    with SessionLocal() as session:
        session.add(novo_cliente)
        session.commit()
        session.refresh(novo_cliente)
        return novo_cliente

@router.post("/{cliente_id}/foto")
def upload_foto_cliente(
    cliente_id: int,
    foto: UploadFile = File(...),
    usuario_logado: Usuario = Depends(require_roles("gerente", "admin")),
):
    with SessionLocal() as session:
        cliente = session.get(Cliente, cliente_id)
        if cliente is None:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        if foto.content_type not in {"image/jpeg", "image/png"}:
            raise HTTPException(status_code=400, detail="Envie uma imagem JPEG ou PNG")

        nome = f"cliente_{cliente_id}_{Path(foto.filename or 'foto').name}"
        destino = PASTA_UPLOAD / nome

        with destino.open("wb") as buffer:
            shutil.copyfileobj(foto.file, buffer)

        cliente.foto = str(destino)
        session.commit()
        session.refresh(cliente)
        return {"cliente": cliente.nome, "foto": cliente.foto}


@router.patch("/{cliente_id}", response_model=ClienteResposta)
def atualizar_cliente(cliente_id: int, cliente: ClientePatch):
    with SessionLocal() as session:
        cliente_db = session.get(Cliente, cliente_id)
        if cliente_db is None:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        for campo, valor in cliente.model_dump(exclude_unset=True).items():
            setattr(cliente_db, campo, valor)

        session.commit()
        session.refresh(cliente_db)
        return cliente_db


@router.delete("/{cliente_id}", status_code=204)
def deletar_cliente(cliente_id: int):
    with SessionLocal() as session:
        cliente = session.get(Cliente, cliente_id)
        if cliente is None:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        session.delete(cliente)
        session.commit()
        return None


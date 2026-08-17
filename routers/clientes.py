from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from database import SessionLocal
from models.cliente import Cliente
from schemas.cliente import ClienteEntrada, ClientePatch, ClienteResposta


router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/", response_model=list[ClienteResposta])
def listar_clientes():
    with SessionLocal() as session:
        consulta = select(Cliente)
        return session.scalars(consulta).all()


@router.get("/{cliente_id}", response_model=ClienteResposta)
def buscar_por_id_cliente(cliente_id: int):
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


from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from database import SessionLocal
from models.carrinho import Carrinho
from models.cliente import Cliente
from schemas.carrinho import CarrinhoEntrada, CarrinhoPatch, CarrinhoResposta


router = APIRouter(prefix="/carrinhos", tags=["Carrinhos"])


@router.get("/", response_model=list[CarrinhoResposta])
def listar_carrinhos():
    with SessionLocal() as session:
        return session.scalars(select(Carrinho)).all()


@router.get("/{carrinho_id}", response_model=CarrinhoResposta)
def buscar_por_id_carrinho(carrinho_id: int):
    with SessionLocal() as session:
        carrinho = session.get(Carrinho, carrinho_id)
        if carrinho is None:
            raise HTTPException(status_code=404, detail="Carrinho não encontrado")
        return carrinho


@router.post("/", response_model=CarrinhoResposta, status_code=201)
def criar_carrinho(carrinho: CarrinhoEntrada):
    with SessionLocal() as session:
        cliente = session.get(Cliente, carrinho.cliente_id)
        if cliente is None:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        novo_carrinho = Carrinho(cliente_id=carrinho.cliente_id, valor_total=0.0)
        session.add(novo_carrinho)
        session.commit()
        session.refresh(novo_carrinho)
        return novo_carrinho


@router.patch("/{carrinho_id}", response_model=CarrinhoResposta)
def atualizar_carrinho(carrinho_id: int, carrinho: CarrinhoPatch):
    with SessionLocal() as session:
        carrinho_db = session.get(Carrinho, carrinho_id)
        if carrinho_db is None:
            raise HTTPException(status_code=404, detail="Carrinho não encontrado")

        for campo, valor in carrinho.model_dump(exclude_unset=True).items():
            setattr(carrinho_db, campo, valor)

        session.commit()
        session.refresh(carrinho_db)
        return carrinho_db


@router.delete("/{carrinho_id}", status_code=204)
def deletar_carrinho(carrinho_id: int):
    with SessionLocal() as session:
        carrinho = session.get(Carrinho, carrinho_id)
        if carrinho is None:
            raise HTTPException(status_code=404, detail="Carrinho não encontrado")

        session.delete(carrinho)
        session.commit()
        return None

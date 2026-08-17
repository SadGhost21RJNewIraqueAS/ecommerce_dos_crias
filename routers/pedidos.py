from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from database import SessionLocal
from models.pedido import Pedido
from schemas.pedido import PedidoEntrada, PedidoPatch, PedidoResposta


router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.get("/", response_model=list[PedidoResposta])
def listar_pedidos():
    with SessionLocal() as session:
        return session.scalars(select(Pedido)).all()


@router.get("/{pedido_id}", response_model=PedidoResposta)
def buscar_por_id_pedido(pedido_id: int):
    with SessionLocal() as session:
        pedido = session.get(Pedido, pedido_id)
        if pedido is None:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        return pedido


@router.post("/", response_model=PedidoResposta, status_code=201)
def criar_pedido(pedido: PedidoEntrada):
    novo_pedido = Pedido(
        cliente_id=pedido.cliente_id,
        status="pendente",
        forma_pagamento=pedido.forma_pagamento,
        status_pagamento="pendente",
        valor_total=0.0,
        estoque=0,
    )
    with SessionLocal() as session:
        session.add(novo_pedido)
        session.commit()
        session.refresh(novo_pedido)
        return novo_pedido


@router.patch("/{pedido_id}", response_model=PedidoResposta)
def atualizar_pedido(pedido_id: int, pedido: PedidoPatch):
    with SessionLocal() as session:
        pedido_db = session.get(Pedido, pedido_id)
        if pedido_db is None:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")

        for campo, valor in pedido.model_dump(exclude_unset=True).items():
            setattr(pedido_db, campo, valor)

        session.commit()
        session.refresh(pedido_db)
        return pedido_db


@router.delete("/{pedido_id}", status_code=204)
def deletar_pedido(pedido_id: int):
    with SessionLocal() as session:
        pedido = session.get(Pedido, pedido_id)
        if pedido is None:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")

        session.delete(pedido)
        session.commit()
        return None

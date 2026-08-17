from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from database import SessionLocal
from models.item_pedido import ItemPedido
from schemas.item_pedido import ItemPedidoEntrada, ItemPedidoPatch, ItemPedidoResposta


router = APIRouter(prefix="/itens-pedidos", tags=["Itens Pedidos"])


@router.get("/", response_model=list[ItemPedidoResposta])
def listar_itens_pedido():
    with SessionLocal() as session:
        return session.scalars(select(ItemPedido)).all()


@router.get("/{item_pedido_id}", response_model=ItemPedidoResposta)
def buscar_por_id_item_pedido(item_pedido_id: int):
    with SessionLocal() as session:
        item = session.get(ItemPedido, item_pedido_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item do pedido não encontrado")
        return item


@router.post("/", response_model=ItemPedidoResposta, status_code=201)
def criar_item_pedido(item: ItemPedidoEntrada):
    novo_item = ItemPedido(
        pedido_id=item.pedido_id,
        produto_id=item.produto_id,
        quantidade=item.quantidade,
        preco_unitario=item.preco_unitario,
    )
    with SessionLocal() as session:
        session.add(novo_item)
        session.commit()
        session.refresh(novo_item)
        return novo_item


@router.patch("/{item_pedido_id}", response_model=ItemPedidoResposta)
def atualizar_item_pedido(item_pedido_id: int, item: ItemPedidoPatch):
    with SessionLocal() as session:
        item_db = session.get(ItemPedido, item_pedido_id)
        if item_db is None:
            raise HTTPException(status_code=404, detail="Item do pedido não encontrado")

        for campo, valor in item.model_dump(exclude_unset=True).items():
            setattr(item_db, campo, valor)

        session.commit()
        session.refresh(item_db)
        return item_db


@router.delete("/{item_pedido_id}", status_code=204)
def deletar_item_pedido(item_pedido_id: int):
    with SessionLocal() as session:
        item = session.get(ItemPedido, item_pedido_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item do pedido não encontrado")

        session.delete(item)
        session.commit()
        return None

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from database import SessionLocal
from models.item_pedido import ItemPedido
from models.pedido import Pedido
from models.produto import Produto
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
    with SessionLocal() as session:
        pedido = session.get(Pedido, item.pedido_id)
        if pedido is None:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")

        produto = session.get(Produto, item.produto_id)
        if produto is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        if produto.estoque < item.quantidade:
            raise HTTPException(status_code=400, detail="Estoque insuficiente")

        novo_item = ItemPedido(
            pedido_id=item.pedido_id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            preco_unitario=item.preco_unitario,
        )
        session.add(novo_item)
        produto.estoque -= item.quantidade
        pedido.valor_total += item.quantidade * item.preco_unitario
        session.commit()
        session.refresh(novo_item)
        return novo_item


@router.patch("/{item_pedido_id}", response_model=ItemPedidoResposta)
def atualizar_item_pedido(item_pedido_id: int, item: ItemPedidoPatch):
    with SessionLocal() as session:
        item_db = session.get(ItemPedido, item_pedido_id)
        if item_db is None:
            raise HTTPException(status_code=404, detail="Item do pedido não encontrado")

        dados = item.model_dump(exclude_unset=True)
        if "quantidade" in dados:
            produto = session.get(Produto, item_db.produto_id)
            diferenca = dados["quantidade"] - item_db.quantidade
            if produto.estoque < diferenca:
                raise HTTPException(status_code=400, detail="Estoque insuficiente")
            produto.estoque -= diferenca

        for campo, valor in dados.items():
            setattr(item_db, campo, valor)

        pedido = session.get(Pedido, item_db.pedido_id)
        pedido.valor_total = sum(
            item_pedido.quantidade * item_pedido.preco_unitario
            for item_pedido in session.scalars(
                select(ItemPedido).where(ItemPedido.pedido_id == pedido.id)
            )
        )
        session.commit()
        session.refresh(item_db)
        return item_db


@router.delete("/{item_pedido_id}", status_code=204)
def deletar_item_pedido(item_pedido_id: int):
    with SessionLocal() as session:
        item = session.get(ItemPedido, item_pedido_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item do pedido não encontrado")

        produto = session.get(Produto, item.produto_id)
        produto.estoque += item.quantidade
        pedido = session.get(Pedido, item.pedido_id)
        pedido.valor_total -= item.quantidade * item.preco_unitario
        session.delete(item)
        session.commit()
        return None

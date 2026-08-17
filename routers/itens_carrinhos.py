from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from database import SessionLocal
from models.item_carrinho import ItemCarrinho
from schemas.item_carrinho import ItemCarrinhoEntrada, ItemCarrinhoPatch, ItemCarrinhoResposta


router = APIRouter(prefix="/itens-carrinhos", tags=["Itens Carrinho"])


@router.get("/", response_model=list[ItemCarrinhoResposta])
def listar_itens_carrinho():
    with SessionLocal() as session:
        return session.scalars(select(ItemCarrinho)).all()


@router.get("/{item_carrinho_id}", response_model=ItemCarrinhoResposta)
def buscar_por_id_item_carrinho(item_carrinho_id: int):
    with SessionLocal() as session:
        item = session.get(ItemCarrinho, item_carrinho_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item do carrinho não encontrado")
        return item


@router.post("/", response_model=ItemCarrinhoResposta, status_code=201)
def criar_item_carrinho(item: ItemCarrinhoEntrada):
    novo_item = ItemCarrinho(
        carrinho_id=item.carrinho_id,
        produto_id=item.produto_id,
        quantidade=item.quantidade,
        valor_unitario=0.0,
    )
    with SessionLocal() as session:
        session.add(novo_item)
        session.commit()
        session.refresh(novo_item)
        return novo_item


@router.patch("/{item_carrinho_id}", response_model=ItemCarrinhoResposta)
def atualizar_item_carrinho(item_carrinho_id: int, item: ItemCarrinhoPatch):
    with SessionLocal() as session:
        item_db = session.get(ItemCarrinho, item_carrinho_id)
        if item_db is None:
            raise HTTPException(status_code=404, detail="Item do carrinho não encontrado")

        for campo, valor in item.model_dump(exclude_unset=True).items():
            setattr(item_db, campo, valor)

        session.commit()
        session.refresh(item_db)
        return item_db


@router.delete("/{item_carrinho_id}", status_code=204)
def deletar_item_carrinho(item_carrinho_id: int):
    with SessionLocal() as session:
        item = session.get(ItemCarrinho, item_carrinho_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item do carrinho não encontrado")

        session.delete(item)
        session.commit()
        return None

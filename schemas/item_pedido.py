from pydantic import BaseModel, Field


class ItemPedidoEntrada(BaseModel):
    pedido_id: int
    produto_id: int
    quantidade: int = Field(gt=0)
    preco_unitario: float = Field(gt=0)


class ItemPedidoResposta(BaseModel):
    id: int
    pedido_id: int
    produto_id: int
    quantidade: int
    preco_unitario: float


class ItemPedidoPatch(BaseModel):
    quantidade: int | None = Field(default=None, gt=0)
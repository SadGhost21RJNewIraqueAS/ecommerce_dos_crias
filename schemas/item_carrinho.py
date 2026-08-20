from pydantic import BaseModel, Field


class ItemCarrinhoEntrada(BaseModel):
    carrinho_id: int
    produto_id: int
    quantidade: int = Field(gt=0)


class ItemCarrinhoResposta(BaseModel):
    id: int
    carrinho_id: int
    produto_id: int
    quantidade: int
    valor_unitario: float

    class Config:
        from_attributes = True


class ItemCarrinhoPatch(BaseModel):
    quantidade: int | None = Field(default=None, gt=0)

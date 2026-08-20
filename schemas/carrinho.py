from pydantic import BaseModel, Field


class CarrinhoEntrada(BaseModel):
    cliente_id: int


class CarrinhoResposta(BaseModel):
    id: int
    cliente_id: int
    valor_total: float

    class Config:
        from_attributes = True


class CarrinhoPatch(BaseModel):
    valor_total: float | None = Field(default=None, ge=0)

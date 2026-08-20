from pydantic import BaseModel, Field


class PedidoEntrada(BaseModel):
    cliente_id: int
    forma_pagamento: str


class PedidoResposta(BaseModel):
    id: int
    cliente_id: int
    status: str
    valor_total: float
    forma_pagamento: str
    status_pagamento: str

    class Config:
        from_attributes = True


class PedidoPatch(BaseModel):
    status: str | None = None
    status_pagamento: str | None = None

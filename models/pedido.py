from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from sqlalchemy import ForeignKey


class Pedido(Base):
    __tablename__ = "pedido"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"))
    status: Mapped[str]
    forma_pagamento: Mapped[str]
    status_pagamento: Mapped[str]
    valor_total: Mapped[float]
    estoque: Mapped[int]
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from sqlalchemy import ForeignKey


class Carrinho(Base):
    __tablename__ = "carrinho"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"))
    valor_total: Mapped[float]

from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from sqlalchemy import ForeignKey


class ItemCarrinho(Base):
    __tablename__ = "item_carrinho"

    id: Mapped[int] = mapped_column(primary_key=True)
    carrinho_id: Mapped[int] = mapped_column(ForeignKey("carrinho.id"))
    produto_id: Mapped[int] = mapped_column(ForeignKey("produto.id"))
    quantidade: Mapped[int]
    valor_unitario: Mapped[float]
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from sqlalchemy import ForeignKey


class Cliente (Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column (primary_key= True)
    nome: Mapped[str]
    cpf: Mapped[int]
    email: Mapped[str]
    tel1: Mapped[int]
    tel2: Mapped[int]
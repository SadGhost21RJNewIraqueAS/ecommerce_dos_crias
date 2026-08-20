from pydantic import BaseModel, Field


class CategoriaEntrada(BaseModel):
    nome: str = Field(min_length=3)
    descricao: str = Field(min_length=3)


class CategoriaResposta(BaseModel):
    id: int
    nome: str
    descricao: str

    class Config:
        from_attributes = True


class CategoriaPatch(BaseModel):
    nome: str | None = Field(default=None, min_length=3)
    descricao: str | None = Field(default=None, min_length=3)

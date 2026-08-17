from pydantic import BaseModel, Field


class ProdutoEntrada(BaseModel):
    categoria_id: int
    nome: str = Field(min_length=3)
    descricao: str = Field(min_length=3)
    valor_produto: float = Field(gt=0)
    estoque: int = Field(ge=0)


class ProdutoResposta(BaseModel):
    id: int
    categoria_id: int
    nome: str
    descricao: str
    valor_produto: float
    estoque: int



class ProdutoPatch(BaseModel):
    categoria_id: int | None = None
    nome: str | None = Field(default=None, min_length=3)
    descricao: str | None = Field(default=None, min_length=3)
    valor_produto: float | None = Field(default=None, gt=0)
    estoque: int | None = Field(default=None, ge=0)

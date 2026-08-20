from pydantic import BaseModel, Field, EmailStr


class ClienteEntrada(BaseModel):
    nome: str = Field(min_length=3)
    cpf: int = Field(gt=0)
    tel1: int = Field(gt=0)
    tel2: int | None = Field(default=None, gt=0)
    email: EmailStr | None = Field(default=None, min_length=3, max_length=320)


class ClienteResposta(BaseModel):
    id: int
    nome: str
    cpf: int
    tel1: int
    tel2: int | None
    email: str

    class Config:
        from_attributes = True

class ClientePatch(BaseModel):
    nome: str | None = Field (default=None, min_length=3)
    cpf: int | None = Field(default=None, gt=0)
    tel1: int | None = Field (default=None, gt=0)
    tel2: int | None = Field (default=None, gt=0)
    email: EmailStr | None = Field(default=None, min_length=3, max_length=320)

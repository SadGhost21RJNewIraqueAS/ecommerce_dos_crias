from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    senha: str = Field(min_length=6, max_length=255)

    @model_validator(mode="before")
    @classmethod
    def rejeitar_dados_cliente(cls, data):
        if isinstance(data, dict):
            for campo in ("cpf", "telefone"):
                if campo in data and data[campo] not in (None, ""):
                    raise ValueError(f"O campo '{campo}' não pode ser informado no cadastro de usuário comum")
        return data


class UsuarioLogin(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=255)


class UsuarioResposta(BaseModel):
    id: int
    nome: str
    username: str
    email: str
    role: str
    is_active: bool = True

    class Config:
        from_attributes = True


class UsuarioRoleUpdate(BaseModel):
    role: str

    @field_validator("role")
    @classmethod
    def validar_role(cls, value: str):
        papel = value.lower()
        if papel not in {"cliente", "gerente", "admin"}:
            raise ValueError("role inválida. Use: cliente, gerente ou admin")
        return papel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None

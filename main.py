from fastapi import FastAPI, APIRouter

from database import Base, ensure_cliente_columns, ensure_usuario_columns, engine
from routers import (
    auth,
    arquivos,
    carrinhos,
    categorias,
    clientes,
    enderecos,
    itens_carrinhos,
    itens_pedidos,
    pedidos,
    produtos,
)

# Importa os modelos para registrar as tabelas no metadata
from models import (
    carrinho,
    categoria,
    cliente,
    item_carrinho,
    item_pedido,
    pedido,
    produto,
    usuario,
)

router = APIRouter()
app = FastAPI(title="BB Garage",
              description="API para gerenciamento de e-commerce da BB Garage",
              version="1.0")

app.include_router(auth.router)
app.include_router(arquivos.router)
app.include_router(clientes.router)
app.include_router(enderecos.router)
app.include_router(categorias.router)
app.include_router(produtos.router)
app.include_router(carrinhos.router)
app.include_router(itens_carrinhos.router)
app.include_router(pedidos.router)
app.include_router(itens_pedidos.router)

@app.on_event("startup")
def startup():
    ensure_usuario_columns(engine)
    ensure_cliente_columns(engine)
    Base.metadata.create_all(bind=engine)


@app.get("/")
def raiz():
    return {"mensagem": "API da BB Garage está funcionando!"}


@app.get("/status")
def status():
    return {"status": "OK", "versao": "1.0"}

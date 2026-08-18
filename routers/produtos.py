from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select

from database import SessionLocal
from models.categoria import Categoria
from models.produto import Produto
from models.usuario import Usuario
from schemas.produto import ProdutoEntrada, ProdutoPatch, ProdutoResposta
from segurança import require_roles


router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.get("/", response_model=list[ProdutoResposta])
def listar_produtos(categoria_id: int | None = None, limite: int = Query(10, ge=1, le=100)):
    with SessionLocal() as session:
        consulta = select(Produto)
        if categoria_id is not None:
            consulta = consulta.where(Produto.categoria_id == categoria_id)
        consulta = consulta.limit(limite)
        return session.scalars(consulta).all()


@router.get("/{produto_id}", response_model=ProdutoResposta)
def buscar_por_id_produto(produto_id: int):
    with SessionLocal() as session:
        produto = session.get(Produto, produto_id)
        if produto is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return produto


@router.post("/", response_model=ProdutoResposta, status_code=201)
def criar_produto(
    produto: ProdutoEntrada,
    usuario_logado: Usuario = Depends(require_roles("gerente", "admin")),
):
    with SessionLocal() as session:
        categoria = session.get(Categoria, produto.categoria_id)
        if categoria is None:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")

        novo_produto = Produto(
            categoria_id=produto.categoria_id,
            nome=produto.nome,
            descricao=produto.descricao,
            valor_produto=produto.valor_produto,
            estoque=produto.estoque,
        )
        session.add(novo_produto)
        session.commit()
        session.refresh(novo_produto)
        return novo_produto


@router.patch("/{produto_id}", response_model=ProdutoResposta)
def atualizar_produto(
    produto_id: int,
    produto: ProdutoPatch,
    usuario_logado: Usuario = Depends(require_roles("gerente", "admin")),
):
    with SessionLocal() as session:
        produto_db = session.get(Produto, produto_id)
        if produto_db is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        dados = produto.model_dump(exclude_unset=True)
        if "categoria_id" in dados and dados["categoria_id"] is not None:
            categoria = session.get(Categoria, dados["categoria_id"])
            if categoria is None:
                raise HTTPException(status_code=404, detail="Categoria não encontrada")

        for campo, valor in dados.items():
            setattr(produto_db, campo, valor)

        session.commit()
        session.refresh(produto_db)
        return produto_db


@router.delete("/{produto_id}", status_code=204)
def deletar_produto(
    produto_id: int,
    usuario_logado: Usuario = Depends(require_roles("admin")),
):
    with SessionLocal() as session:
        produto = session.get(Produto, produto_id)
        if produto is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        session.delete(produto)
        session.commit()
        return None


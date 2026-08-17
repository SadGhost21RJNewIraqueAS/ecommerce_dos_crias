from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from database import SessionLocal
from models.categoria import Categoria
from models.usuario import Usuario
from schemas.categoria import CategoriaEntrada, CategoriaPatch, CategoriaResposta
from segurança import get_current_user, require_roles


router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.get("/", response_model=list[CategoriaResposta])
def listar_categorias():
    with SessionLocal() as session:
        categorias = session.scalars(select(Categoria)).all()
        return categorias


@router.get("/{categoria_id}", response_model=CategoriaResposta)
def buscar_por_id_categoria(categoria_id: int):
    with SessionLocal() as session:
        categoria = session.get(Categoria, categoria_id)
        if categoria is None:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        return categoria


@router.post("/", response_model=CategoriaResposta, status_code=201)
def criar_categoria(
    categoria: CategoriaEntrada,
    usuario_logado: Usuario = Depends(require_roles("gerente", "admin")),
):
    nova_categoria = Categoria(nome=categoria.nome, descricao=categoria.descricao)
    with SessionLocal() as session:
        session.add(nova_categoria)
        session.commit()
        session.refresh(nova_categoria)
        return nova_categoria


@router.patch("/{categoria_id}", response_model=CategoriaResposta)
def atualizar_categoria(
    categoria_id: int,
    categoria: CategoriaPatch,
    usuario_logado: Usuario = Depends(require_roles("gerente", "admin")),
):
    with SessionLocal() as session:
        categoria_db = session.get(Categoria, categoria_id)
        if categoria_db is None:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")

        for campo, valor in categoria.model_dump(exclude_unset=True).items():
            setattr(categoria_db, campo, valor)

        session.commit()
        session.refresh(categoria_db)
        return categoria_db


@router.delete("/{categoria_id}", status_code=204)
def deletar_categoria(
    categoria_id: int,
    usuario_logado: Usuario = Depends(require_roles("admin")),
):
    with SessionLocal() as session:
        categoria = session.get(Categoria, categoria_id)
        if categoria is None:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")

        session.delete(categoria)
        session.commit()
        return None

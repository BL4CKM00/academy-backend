from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import date

from app.database.database import SessionLocal

from app.schemas.produto_schema import (
    ProdutoCreate,
    ProdutoUpdate,
    ReposicaoEstoque,
    ProdutoResponse
)
from app.schemas.venda_schema import VendaResponse, ResumoVendasMes
from app.models.venda_model import Venda
from app.dao.produto_dao import ProdutoDAO

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/",
    response_model=ProdutoResponse
)
def criar_produto(
    produto: ProdutoCreate,
    db: Session = Depends(get_db)
):

    return ProdutoDAO.criar(
        db,
        produto
    )


@router.get(
    "/",
    response_model=list[ProdutoResponse]
)
def listar_produtos(
    db: Session = Depends(get_db)
):

    return ProdutoDAO.listar(
        db
    )


@router.put(
    "/{produto_id}",
    response_model=ProdutoResponse
)
def editar_produto(
    produto_id: int,
    produto: ProdutoUpdate,
    db: Session = Depends(get_db)
):

    return ProdutoDAO.editar(
        db,
        produto_id,
        produto
    )


@router.patch(
    "/{produto_id}/repor",
    response_model=ProdutoResponse
)
def repor_estoque(
    produto_id: int,
    reposicao: ReposicaoEstoque,
    db: Session = Depends(get_db)
):

    return ProdutoDAO.repor_estoque(
        db,
        produto_id,
        reposicao.quantidade
    )


@router.patch(
    "/{produto_id}/desativar",
    response_model=ProdutoResponse
)
def desativar_produto(
    produto_id: int,
    db: Session = Depends(get_db)
):

    return ProdutoDAO.desativar(
        db,
        produto_id
    )


@router.patch(
    "/{produto_id}/ativar",
    response_model=ProdutoResponse
)
def ativar_produto(
    produto_id: int,
    db: Session = Depends(get_db)
):

    produto = ProdutoDAO.ativar(
        db,
        produto_id
    )

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return produto


@router.patch(
    "/{produto_id}/vender",
    response_model=ProdutoResponse
)
def vender_produto(
    produto_id: int,
    body: ReposicaoEstoque,
    db: Session = Depends(get_db)
):

    try:

        return ProdutoDAO.vender(
            db,
            produto_id,
            body.quantidade
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.delete("/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    deletado = ProdutoDAO.deletar(db, produto_id)
    if not deletado:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"message": "Produto deletado com sucesso"}


@router.get(
    "/vendas/resumo",
    response_model=list[ResumoVendasMes]
)
def resumo_vendas(
    db: Session = Depends(get_db)
):

    hoje = date.today()

    resultados = (
        db.query(
            func.to_char(
                Venda.data_venda,
                "MM/YYYY"
            ).label("mes"),

            func.count(
                Venda.id
            ).label("total_vendas"),

            func.sum(
                Venda.quantidade
            ).label("total_itens"),

            func.sum(
                Venda.valor_total
            ).label("receita_total")
        )
        .filter(
            extract(
                "year",
                Venda.data_venda
            ) == hoje.year
        )
        .group_by(
            func.to_char(
                Venda.data_venda,
                "MM/YYYY"
            )
        )
        .order_by(
            func.to_char(
                Venda.data_venda,
                "MM/YYYY"
            )
        )
        .all()
    )

    return [
        ResumoVendasMes(
            mes=r.mes,
            total_vendas=r.total_vendas,
            total_itens=r.total_itens,
            receita_total=float(
                r.receita_total or 0
            )
        )
        for r in resultados
    ]
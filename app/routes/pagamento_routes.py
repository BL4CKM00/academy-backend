from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.dao.pagamento_dao import PagamentoDAO
from app.dao.aluno_dao import AlunoDAO
from app.services.pagamento_service import PagamentoService
from app.services.notificacao_service import NotificacaoService

from app.schemas.pagamento_schema import (
    PagamentoResponse
)

router = APIRouter(
    prefix="/pagamentos",
    tags=["Pagamentos"]
)


@router.get(
    "/",
    response_model=list[PagamentoResponse]
)
def listar_pagamentos(
    db: Session = Depends(get_db)
):

    return PagamentoDAO.listar(db)


@router.put(
    "/pagar/{termo}",
    response_model=PagamentoResponse
)
def pagar_mensalidade(
    termo: str,
    db: Session = Depends(get_db)
):

    aluno = AlunoDAO.buscar_unico(
        db,
        termo
    )

    if not aluno:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado"
        )

    pagamento = (
        PagamentoDAO.buscar_pendente_por_aluno(
            db,
            aluno.id
        )
    )

    if not pagamento:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma mensalidade pendente encontrada"
        )

    return PagamentoDAO.pagar(
        db,
        pagamento
    )


@router.post(
    "/gerar/{aluno_id}",
    response_model=PagamentoResponse
)
def gerar_mensalidade(
    termo: str,
    db: Session = Depends(get_db)
):

    aluno = AlunoDAO.buscar_unico(
        db,
        termo
    )

    if not aluno:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado"
        )

    pagamento_pendente = (
        PagamentoDAO.buscar_pendente_por_aluno(
            db,
            aluno.id
        )
    )

    if pagamento_pendente:
        raise HTTPException(
            status_code=400,
            detail="Existe uma mensalidade pendente para este aluno"
        )

    ultimo_pagamento = (
        PagamentoDAO.buscar_ultimo_pagamento(
            db,
            aluno.id
        )
    )

    dados = (
        PagamentoService
        .gerar_dados_mensalidade(
            aluno,
            ultimo_pagamento
        )
    )

    pagamento_existente = (
        PagamentoDAO.buscar_por_aluno_competencia(
            db,
            aluno.id,
            dados["competencia"]
        )
    )

    if pagamento_existente:
        raise HTTPException(
            status_code=400,
            detail="Já existe uma mensalidade para esta competência"
        )

    return PagamentoDAO.criar(
        db,
        aluno.id,
        dados["competencia"],
        dados["data_vencimento"]
    )

@router.post("/testar-notificacoes")
def testar_notificacoes(
    db: Session = Depends(get_db)
):

    NotificacaoService.verificar_pagamentos(
        db
    )

    return {
        "message": "Notificações testadas." 
    }
from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.dao.pagamento_dao import PagamentoDAO

from app.services.pagamento_service import PagamentoService

from app.schemas.relatorio_schema import (
    RelatorioAlunoResponse
)

router = APIRouter(
    prefix="/relatorio",
    tags=["Relatório"]
)


@router.get(
    "/alunos",
    response_model=list[RelatorioAlunoResponse]
)
def relatorio_alunos(
    db: Session = Depends(get_db)
):

    pagamentos = (
        PagamentoDAO.listar_com_alunos(db)
    )

    resultado = []

    for pagamento in pagamentos:

        status = (
            PagamentoService.calcular_status(
                pagamento.data_vencimento,
                pagamento.pago
            )
        )

        resultado.append(
            {
                "codigo": pagamento.aluno.codigo,
                "nome": pagamento.aluno.nome,
                "competencia": pagamento.competencia,
                "status": status
            }
        )

    return resultado
from datetime import date
from datetime import timedelta

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.aluno_model import Aluno
from app.models.pagamento_model import Pagamento


class DashboardDAO:

    @staticmethod
    def obter_indicadores(db: Session):

        hoje = date.today()

        alunos_ativos = (
            db.query(Aluno)
            .filter(Aluno.ativo.is_(True))
            .count()
        )

        alunos_diario = (
            db.query(Aluno)
            .filter(Aluno.tipo_plano == "DIARIO")
            .count()
        )

        alunos_mensal = (
            db.query(Aluno)
            .filter(Aluno.tipo_plano == "MENSAL")
            .count()
        )

        alunos_trimestral = (
            db.query(Aluno)
            .filter(Aluno.tipo_plano == "TRIMESTRAL")
            .count()
        )

        alunos_semestral = (
            db.query(Aluno)
            .filter(Aluno.tipo_plano == "SEMESTRAL")
            .count()
        )

        alunos_anual = (
            db.query(Aluno)
            .filter(Aluno.tipo_plano == "ANUAL")
            .count()
        )

        mensalidades_abertas = (
            db.query(Pagamento)
            .filter(Pagamento.pago.is_(False))
            .count()
        )

        mensalidades_atrasadas = (
            db.query(Pagamento)
            .filter(
                Pagamento.pago.is_(False),
                Pagamento.data_vencimento < hoje
            )
            .count()
        )

        vencendo_hoje = (
            db.query(Pagamento)
            .filter(
                Pagamento.pago.is_(False),
                Pagamento.data_vencimento >= hoje,
                Pagamento.data_vencimento <= hoje + timedelta(days=2)
            )
            .count()
        )

        receita_recebida = (
            db.query(
                func.sum(Aluno.mensalidade)
            )
            .join(
                Pagamento,
                Pagamento.aluno_id == Aluno.id
            )
            .filter(
                Pagamento.pago.is_(True)
            )
            .scalar()
        ) or 0

        receita_prevista = (
            db.query(
                func.sum(Aluno.mensalidade)
            )
            .scalar()
        ) or 0

        return {
            "alunos_ativos": alunos_ativos,
            "mensalidades_abertas": mensalidades_abertas,
            "mensalidades_atrasadas": mensalidades_atrasadas,
            "vencendo_hoje": vencendo_hoje,
            "receita_recebida": receita_recebida,

            "receita_prevista": receita_prevista,

            "alunos_diario": alunos_diario,
            "alunos_mensal": alunos_mensal,
            "alunos_trimestral": alunos_trimestral,
            "alunos_semestral": alunos_semestral,
            "alunos_anual": alunos_anual
        }
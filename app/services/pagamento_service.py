from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from app.models.aluno_model import Aluno


class PagamentoService:

    PLANOS = {
        "DIARIO": {"days": 1},
        "MENSAL": {"months": 1},
        "TRIMESTRAL": {"months": 3},
        "SEMESTRAL": {"months": 6},
        "ANUAL": {"years": 1}
    }

    @staticmethod
    def calcular_status(data_vencimento: date, pago: bool):

        if pago:
            return "PAGO"

        hoje = date.today()
        limite = hoje + timedelta(days=2)

        if data_vencimento < hoje:
            return "ATRASADO"

        if hoje <= data_vencimento <= limite:
            return "VENCENDO"

        return "PENDENTE"
    
    @staticmethod
    def gerar_dados_mensalidade(
        aluno: Aluno,
        ultimo_pagamento=None
    ):

        periodo = (
            PagamentoService.PLANOS[
                aluno.tipo_plano.upper()
            ]
        )

        if ultimo_pagamento:
            data_base = (
                ultimo_pagamento
                .data_vencimento
            )
        else:
            data_base = (
                aluno
                .data_inscricao
            )

        data_vencimento = (
            data_base +
            relativedelta(**periodo)
        )

        competencia = (
            f"{data_vencimento.month:02d}/{data_vencimento.year}"
        )

        return {
            "competencia": competencia,
            "data_vencimento": data_vencimento
        }
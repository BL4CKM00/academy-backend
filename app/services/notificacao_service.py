from sqlalchemy.orm import Session

from app.dao.pagamento_dao import PagamentoDAO
from app.services.pagamento_service import PagamentoService
from app.integrations.whatsapp_service import WhatsappService


class NotificacaoService:

    @staticmethod
    def verificar_pagamentos(
        db: Session
    ):

        pagamentos = (
            PagamentoDAO.listar_pendentes(db)
        )

        for pagamento in pagamentos:

            status = (
                PagamentoService.calcular_status(
                    pagamento.data_vencimento,
                    pagamento.pago
                )
            )

            print(
                f"{pagamento.aluno.nome} -> {status}"
            )

            if status == "VENCENDO":

                WhatsappService.enviar_notificacao(
                    pagamento
                )
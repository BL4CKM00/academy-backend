from datetime import date

from sqlalchemy.orm import Session

from app.models.pagamento_model import Pagamento
from app.models.aluno_model import Aluno


class PagamentoDAO:

    @staticmethod
    def criar(
        db: Session,
        aluno_id: int,
        competencia: str,
        data_vencimento: date
    ):

        pagamento = Pagamento(
            aluno_id=aluno_id,
            competencia=competencia,
            data_vencimento=data_vencimento
        )

        db.add(pagamento)
        db.commit()
        db.refresh(pagamento)

        return pagamento
    
    @staticmethod
    def listar(
        db: Session
    ):

        return db.query(Pagamento).all()

    @staticmethod
    def marcar_como_pago(
        db: Session,
        pagamento_id: int
    ):

        pagamento = (
            db.query(Pagamento)
            .filter(Pagamento.id == pagamento_id)
            .first()
        )

        if not pagamento:
            return None

        pagamento.pago = True
        pagamento.data_pagamento = date.today()

        db.commit()
        db.refresh(pagamento)

        return pagamento
    
    @staticmethod
    def listar_com_alunos(
        db: Session
    ):

        return (
            db.query(Pagamento)
            .join(Aluno)
            .all()
        )

    @staticmethod
    def buscar_por_aluno_competencia(
        db: Session,
        aluno_id: int,
        competencia: str
    ):

        return (
            db.query(Pagamento)
            .filter(
                Pagamento.aluno_id == aluno_id,
                Pagamento.competencia == competencia
            )
            .first()
        )
    
    @staticmethod
    def buscar_ultimo_pagamento(
        db: Session,
        aluno_id: int
    ):

        return (
            db.query(Pagamento)
            .filter(
                Pagamento.aluno_id == aluno_id
            )
            .order_by(
                Pagamento.data_vencimento.desc()
            )
            .first()
        )
    
    @staticmethod
    def buscar_pendente_por_aluno(
        db: Session,
        aluno_id: int
    ):

        return (
            db.query(Pagamento)
            .filter(
                Pagamento.aluno_id == aluno_id,
                Pagamento.pago.is_(False)
            )
            .first()
        )
    
    @staticmethod
    def pagar(
        db: Session,
        pagamento: Pagamento
    ):

        pagamento.pago = True
        pagamento.data_pagamento = date.today()

        db.commit()
        db.refresh(pagamento)

        return pagamento
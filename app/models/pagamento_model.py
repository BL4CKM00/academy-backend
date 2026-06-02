from sqlalchemy import Column, Integer, Date, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Pagamento(Base):

    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)

    aluno_id = Column(
        Integer,
        ForeignKey("alunos.id"),
        nullable=False
    )

    data_vencimento = Column(Date, nullable=False)

    data_pagamento = Column(Date, nullable=True)

    pago = Column(Boolean, default=False)

    competencia = Column(String(7), nullable=False)

    aluno = relationship(
        "Aluno",
        back_populates="pagamentos"
    )
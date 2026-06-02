from sqlalchemy import Column, Integer, String, Date, Float, Boolean
from sqlalchemy.orm import relationship

from app.database.database import Base


class Aluno(Base):

    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)

    codigo = Column(String(3), unique=True, nullable=False)

    nome = Column(String(100), nullable=False)

    data_inscricao = Column(Date, nullable=False)

    mensalidade = Column(Float, nullable=False)

    tipo_plano = Column(String(20), nullable=False)

    ativo = Column(Boolean, default=True, nullable=False)

    cpf = Column(
        String(11),
        unique=True,
        nullable=False
    )

    telefone = Column(
        String(11),
        unique=True,
        nullable=True
    )
    
    email = Column(
        String(255),
        unique=True,
        nullable=True
    )

    pagamentos = relationship(
        "Pagamento",
        back_populates="aluno",
        cascade="all, delete-orphan"
    )
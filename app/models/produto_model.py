from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean
)

from app.database.database import Base


class Produto(Base):

    __tablename__ = "produtos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    codigo = Column(
        String(10),
        unique=True,
        nullable=False
    )

    tipo = Column(
        String(50),
        nullable=False
    )

    tamanho = Column(
        String(5),
        nullable=False
    )

    cor = Column(
        String(30),
        nullable=False
    )

    descricao = Column(
        String(255),
        nullable=True
    )

    valor_compra = Column(
        Float,
        nullable=False
    )

    percentual_lucro = Column(
        Float,
        nullable=False
    )

    valor_venda = Column(
        Float,
        nullable=False
    )

    quantidade = Column(
        Integer,
        nullable=False
    )

    saldo = Column(
        Integer,
        nullable=False
    )

    estoque_minimo = Column(
        Integer,
        nullable=False,
        default=5
    )

    ativo = Column(
        Boolean,
        nullable=False,
        default=True
    )
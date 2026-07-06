from sqlalchemy import Column, Integer, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from datetime import date
from app.database.database import Base


class Venda(Base):

    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, index=True)

    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)

    quantidade = Column(Integer, nullable=False)

    valor_unitario = Column(Float, nullable=False)

    valor_total = Column(Float, nullable=False)

    data_venda = Column(Date, nullable=False, default=date.today)

    produto = relationship("Produto")
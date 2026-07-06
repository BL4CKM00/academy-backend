from pydantic import BaseModel
from datetime import date


class VendaCreate(BaseModel):
    quantidade: int


class VendaResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    valor_unitario: float
    valor_total: float
    data_venda: date

    class Config:
        from_attributes = True


class ResumoVendasMes(BaseModel):
    mes: str
    total_vendas: int
    total_itens: int
    receita_total: float
from datetime import date

from pydantic import BaseModel

class PagamentoResponse(BaseModel):
    id: int
    aluno_id: int
    competencia: str
    data_vencimento: date
    data_pagamento: date | None
    pago: bool

    class Config:
        from_attributes = True
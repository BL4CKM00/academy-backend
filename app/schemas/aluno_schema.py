from datetime import date

from pydantic import EmailStr

from pydantic import BaseModel

from enum import Enum

class TipoPlano(str, Enum):
    DIARIO = "DIARIO"
    MENSAL = "MENSAL"
    TRIMESTRAL = "TRIMESTRAL"
    SEMESTRAL = "SEMESTRAL"
    ANUAL = "ANUAL"

class AlunoCreate(BaseModel):
    nome: str
    cpf: str | None = None
    telefone: str
    email: EmailStr | None = None
    data_inscricao: date
    mensalidade: float
    tipo_plano: TipoPlano

class AlunoResponse(BaseModel):
    id: int
    codigo: str
    nome: str
    cpf: str | None = None
    telefone: str
    email: EmailStr | None = None
    data_inscricao: date
    mensalidade: float
    tipo_plano: TipoPlano
    ativo: bool 

    class Config:
        from_attributes = True
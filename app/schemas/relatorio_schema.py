from pydantic import BaseModel


class RelatorioAlunoResponse(BaseModel):

    codigo: str

    nome: str

    competencia: str

    status: str
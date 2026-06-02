from pydantic import BaseModel


class DashboardResponse(BaseModel):

    alunos_ativos: int

    mensalidades_abertas: int
    mensalidades_atrasadas: int
    vencendo_hoje: int

    receita_recebida: float
    receita_prevista: float

    alunos_diario: int
    alunos_mensal: int
    alunos_trimestral: int
    alunos_semestral: int
    alunos_anual: int
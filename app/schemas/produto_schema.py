from pydantic import BaseModel
from typing import Optional


class ProdutoCreate(BaseModel):

    tipo: str

    tamanho: str

    cor: str

    descricao: Optional[str] = None

    valor_compra: float

    percentual_lucro: float

    quantidade: int

    estoque_minimo: int = 5

class ProdutoUpdate(BaseModel):

    tipo: str

    tamanho: str

    cor: str

    descricao: str | None = None

    valor_compra: float

    percentual_lucro: float

    quantidade: int

    estoque_minimo: int

    ativo: bool

class ReposicaoEstoque(BaseModel):

    quantidade: int

class ProdutoResponse(BaseModel):

    id: int

    codigo: str

    tipo: str

    tamanho: str

    cor: str

    descricao: Optional[str]

    valor_compra: float

    percentual_lucro: float

    valor_venda: float

    quantidade: int

    saldo: int

    estoque_minimo: int

    ativo: bool

    class Config:
        from_attributes = True
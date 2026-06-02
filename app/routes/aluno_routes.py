from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.dao.aluno_dao import AlunoDAO

from app.schemas.aluno_schema import (
    AlunoCreate,
    AlunoResponse
)

router = APIRouter(
    prefix="/alunos",
    tags=["Alunos"]
)


@router.post(
    "/",
    response_model=AlunoResponse
)
def criar_aluno(
    aluno: AlunoCreate,
    db: Session = Depends(get_db)
):

    return AlunoDAO.criar(db, aluno)


@router.get(
    "/",
    response_model=list[AlunoResponse]
)
def listar_alunos(
    db: Session = Depends(get_db)
):
    AlunoDAO.verificar_e_atualizar_status(db)

    return AlunoDAO.listar(db)

@router.get("/busca/{termo}")
def buscar_aluno(
    termo: str,
    db: Session = Depends(get_db)
):

    return AlunoDAO.buscar(
        db,
        termo
    )

@router.put(
    "/{codigo}",
    response_model=AlunoResponse
)
def atualizar_aluno(
    codigo: str,
    aluno: AlunoCreate,
    db: Session = Depends(get_db)
):

    aluno_atualizado = AlunoDAO.atualizar(
        db,
        codigo,
        aluno
    )

    if not aluno_atualizado:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado"
        )

    return aluno_atualizado


@router.delete("/{codigo}")
def deletar_aluno(
    codigo: str,
    db: Session = Depends(get_db)
):

    removido = AlunoDAO.deletar(
        db,
        codigo
    )

    if not removido:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado"
        )

    return {
        "message": "Aluno removido com sucesso"
    }
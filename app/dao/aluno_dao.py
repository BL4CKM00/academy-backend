from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.aluno_model import Aluno
from app.models.pagamento_model import Pagamento
from app.schemas.aluno_schema import AlunoCreate


class AlunoDAO:

    @staticmethod
    def criar(db: Session, aluno: AlunoCreate):
        codigo = AlunoDAO.gerar_codigo(db)

        novo_aluno = Aluno(
            codigo=codigo,
            nome=aluno.nome,
            cpf=aluno.cpf,
            telefone=aluno.telefone,
            email=aluno.email,
            data_inscricao=aluno.data_inscricao,
            mensalidade=aluno.mensalidade,
            tipo_plano=aluno.tipo_plano
        )
        db.add(novo_aluno)
        db.commit()
        db.refresh(novo_aluno)

        return novo_aluno

    @staticmethod
    def listar(db: Session):

        return db.query(Aluno).all()
    
    @staticmethod
    def buscar_por_id(
        db: Session,
        aluno_id: int
    ):

        return (
            db.query(Aluno)
            .filter(Aluno.id == aluno_id)
            .first()
        )
    
    @staticmethod
    def buscar_unico(
        db: Session,
        termo: str
    ):

        return (
            db.query(Aluno)
            .filter(
                or_(
                    Aluno.codigo == termo,
                    Aluno.cpf == termo,
                    Aluno.telefone == termo
                )
            )
            .first()
        )

    @staticmethod
    def buscar(
        db: Session,
        termo: str
    ):

        return (
            db.query(Aluno)
            .filter(
                or_(
                    Aluno.codigo == termo,
                    Aluno.cpf == termo,
                    Aluno.telefone == termo,
                    Aluno.nome.ilike(f"%{termo}%")
                )
            )
            .all()
        )
    
    @staticmethod
    def atualizar(
        db: Session,
        codigo: str,
        dados: AlunoCreate
    ):

        aluno = (
            db.query(Aluno)
            .filter(Aluno.codigo == codigo)
            .first()
        )

        if not aluno:
            return None

        aluno.nome = dados.nome
        aluno.cpf = dados.cpf
        aluno.telefone = dados.telefone
        aluno.email = dados.email

        aluno.data_inscricao = dados.data_inscricao
        aluno.mensalidade = dados.mensalidade
        aluno.tipo_plano = dados.tipo_plano

        db.commit()
        db.refresh(aluno)

        AlunoDAO.verificar_e_atualizar_status(db)

        return aluno

    @staticmethod
    def deletar(
        db: Session,
        codigo: str
    ):

        aluno = (
            db.query(Aluno)
            .filter(Aluno.codigo == codigo)
            .first()
        )

        if not aluno:
            return False

        db.delete(aluno)
        db.commit()

        return True
    
    @staticmethod
    def gerar_codigo(db: Session):

        ultimo_aluno = (
            db.query(Aluno)
            .order_by(Aluno.id.desc())
            .first()
        )

        if not ultimo_aluno:
            return "001"

        proximo = ultimo_aluno.id + 1

        return str(proximo).zfill(3)
    
    @staticmethod
    def verificar_e_atualizar_status(db: Session):
        hoje = date.today()
        alunos = db.query(Aluno).all()

        for aluno in alunos:
            ultimo = (
                db.query(Pagamento)
                .filter(Pagamento.aluno_id == aluno.id)
                .order_by(Pagamento.data_vencimento.desc())
                .first()
            )

            # ❌ SEM PAGAMENTO = INATIVO
            if not ultimo:
                aluno.ativo = False
                continue

            # ❌ NÃO PAGO = INATIVO
            if not ultimo.pago:
                aluno.ativo = not (ultimo.data_vencimento < hoje and not ultimo.pago)
                continue

            # ✅ PAGO = ATIVO
            aluno.ativo = True

        db.commit()
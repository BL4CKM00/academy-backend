from sqlalchemy.orm import Session

from app.models.produto_model import Produto


class ProdutoDAO:

    @staticmethod
    def criar(
        db: Session,
        produto
    ):

        # Busca o último produto cadastrado
        ultimo = (
            db.query(Produto)
            .order_by(Produto.id.desc())
            .first()
        )

        if ultimo:
            numero = ultimo.id + 1
        else:
            numero = 1

        codigo = f"PRD{numero:03d}"

        valor_venda = (
            produto.valor_compra *
            (1 + produto.percentual_lucro / 100)
        )

        novo_produto = Produto(

            codigo=codigo,

            tipo=produto.tipo,

            tamanho=produto.tamanho,

            cor=produto.cor,

            descricao=produto.descricao,

            valor_compra=produto.valor_compra,

            percentual_lucro=produto.percentual_lucro,

            valor_venda=valor_venda,

            quantidade=produto.quantidade,

            saldo=produto.quantidade,

            estoque_minimo=produto.estoque_minimo,

            ativo=True
        )

        db.add(novo_produto)

        db.commit()

        db.refresh(novo_produto)

        return novo_produto

    @staticmethod
    def listar(db: Session):
        return (
            db.query(Produto)
            .order_by(Produto.codigo)
            .all()
        )
    
    @staticmethod
    def editar(
        db: Session,
        produto_id: int,
        dados
    ):

        produto = (
            db.query(Produto)
            .filter(
                Produto.id == produto_id
            )
            .first()
        )

        if not produto:
            return None

        produto.tipo = dados.tipo

        produto.tamanho = dados.tamanho

        produto.cor = dados.cor

        produto.descricao = dados.descricao

        produto.valor_compra = dados.valor_compra

        produto.percentual_lucro = dados.percentual_lucro

        produto.valor_venda = (
            dados.valor_compra *
            (1 + dados.percentual_lucro / 100)
        )

        diferenca = (
            dados.quantidade -
            produto.quantidade
        )

        produto.quantidade = dados.quantidade

        produto.saldo += diferenca

        produto.estoque_minimo = dados.estoque_minimo

        produto.ativo = dados.ativo

        db.commit()

        db.refresh(produto)

        return produto
    
    @staticmethod
    def repor_estoque(
        db: Session,
        produto_id: int,
        quantidade: int
    ):

        produto = (
            db.query(Produto)
            .filter(
                Produto.id == produto_id
            )
            .first()
        )

        if not produto:
            return None

        produto.quantidade += quantidade

        produto.saldo += quantidade

        db.commit()

        db.refresh(produto)

        return produto
    
    @staticmethod
    def desativar(
        db: Session,
        produto_id: int
    ):

        produto = (
            db.query(Produto)
            .filter(
                Produto.id == produto_id
            )
            .first()
        )

        if not produto:
            return None

        produto.ativo = False

        db.commit()

        db.refresh(produto)

        return produto
    
    @staticmethod
    def ativar(db: Session, produto_id: int):
        produto = db.query(Produto).filter(Produto.id == produto_id).first()
        if not produto:
            return None
        produto.ativo = True
        db.commit()
        db.refresh(produto)
        return produto

    @staticmethod
    def vender(db: Session, produto_id: int, quantidade: int):
        from app.models.venda_model import Venda
        from datetime import date

        produto = db.query(Produto).filter(Produto.id == produto_id).first()
        if not produto:
            return None
        if not produto.ativo:
            raise ValueError("Produto inativo não pode ser vendido")
        if produto.saldo < quantidade:
            raise ValueError(f"Saldo insuficiente. Saldo atual: {produto.saldo}")

        produto.saldo -= quantidade

        venda = Venda(
            produto_id=produto.id,
            quantidade=quantidade,
            valor_unitario=produto.valor_venda,
            valor_total=produto.valor_venda * quantidade,
            data_venda=date.today()
        )
        db.add(venda)
        db.commit()
        db.refresh(produto)
        return produto
    
    @staticmethod
    def deletar(db: Session, produto_id: int):
        produto = (
            db.query(Produto)
            .filter(Produto.id == produto_id)
            .first()
        )
        if not produto:
            return False
        db.delete(produto)
        db.commit()
        return True
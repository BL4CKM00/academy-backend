class WhatsappService:

    @staticmethod
    def enviar_notificacao(
        pagamento
    ):

        mensagem = f"""
Olá, {pagamento.aluno.nome}!

Sua mensalidade vence em {pagamento.data_vencimento.strftime("%d/%m/%Y")}.

Evite atrasos e mantenha seu plano ativo.

Academy System
"""

        print("=" * 40)
        print("WHATSAPP")
        print(f"Telefone: {pagamento.aluno.telefone}")
        print(mensagem)
        print("=" * 40)
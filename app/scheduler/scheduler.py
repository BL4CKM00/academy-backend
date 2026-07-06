from apscheduler.schedulers.background import BackgroundScheduler

from app.database.database import SessionLocal

from app.services.notificacao_service import NotificacaoService

scheduler = BackgroundScheduler()


def executar_notificacoes():

    db = SessionLocal()

    try:

        print("Verificando pagamentos...")

        NotificacaoService.verificar_pagamentos(db)

    finally:

        db.close()


scheduler.add_job(
    executar_notificacoes,
    trigger="interval",
    minutes=1,
    id="notificacoes",
    replace_existing=True
)

def iniciar_scheduler():

    scheduler.start()

    print("Scheduler iniciado.")
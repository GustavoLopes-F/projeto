# auto_envio.py (Arquivo Corrigido)
import time
import datetime
import schedule
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
import pywhatkit

# Garante que o banco e tabelas existem
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def enviar_mensagens():
    print(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] Verificando agendamentos...")
    db: Session = next(get_db())
    # Filtra apenas os agendamentos não enviados
    agendamentos = db.query(models.Agendamento).filter(models.Agendamento.enviado == False).all() 

    if not agendamentos:
        print("🎉 Todos os agendamentos pendentes foram enviados.")
        db.close()
        print("🔁 Fim do ciclo de envio.\n")
        return

    for ag in agendamentos:
        # A nova lógica de filtro acima já garante que enviado é False
        if not hasattr(ag, "telefone") or not ag.telefone:
            print(f"⚠️ Agendamento {ag.id} sem telefone, pulando...")
            continue
        
        # O campo 'telefone' deve ser tratado para o formato internacional
        numero = str(ag.telefone).strip().replace(" ", "")
        
        # Adiciona o DDI (+55) se o número não tiver DDI/DDD no formato correto
        if not numero.startswith("+"):
            # Assumindo que o número já tem o DDD
            numero = "+55" + numero
            
        # Garante que o DDI tem o "+" (formato esperado pelo pywhatkit)
        if not numero.startswith("+"):
            numero = "+" + numero

        mensagem = (
            f"Olá {ag.paciente},\n"
            f"Sua consulta/exame foi agendada pelo Departamento de Saúde.\n\n"
            f"📅 Data: {ag.data}\n"
            f"🕑 Hora: {ag.hora}\n"
            f"📍 Local: {ag.local}\n"
            f"🧪 Exame: {ag.exame or '-'}\n"
            f"🔍 Tipo: {ag.tipoexame or '-'}\n\n"
            f"Por favor, compareça no horário marcado."
        )

        print(f"📨 Enviando mensagem para {ag.paciente} ({numero})...")

        try:
            # CORREÇÃO: aumentar wait_time para 20-30 segundos para garantir o carregamento do WhatsApp Web
            pywhatkit.sendwhatmsg_instantly(
                phone_no=numero,
                message=mensagem,
                wait_time=30,      # AUMENTADO DE 10 PARA 30s
                tab_close=True     # fecha a aba após enviar
            )

            # marca como enviado
            ag.enviado = True
            db.commit()

            print(f"✅ Mensagem enviada para {ag.paciente}.")
            
            # pausa: adiciona um pequeno delay entre os envios para evitar sobrecarga e falha de automação
            time.sleep(5) 
            
        except Exception as e:
            # se a automação falhar, o status de 'enviado' não é alterado, e a mensagem será tentada novamente
            db.rollback() 
            print(f"❌ Erro ao enviar para {ag.paciente}. Tente aumentar o wait_time: {e}")

    db.close()
    print("🔁 Fim do ciclo de envio.\n")

# roda a cada 10 minutos (teste)
schedule.every(10).minutes.do(enviar_mensagens)

print("🚀 Sistema automático iniciado! Verificando a cada 10 minutos...")
enviar_mensagens()  # primeira execução

while True:
    schedule.run_pending()
    time.sleep(10)



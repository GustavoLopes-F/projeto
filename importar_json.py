import json
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models


Base.metadata.create_all(bind=engine)


with open("consultas.json", "r", encoding="utf-8") as f:
    consultas = json.load(f)

db: Session = SessionLocal()

for c in consultas:
    
    existe = db.query(models.Agendamento).filter_by(
        paciente=c.get("nome"),
        data=c.get("data")
    ).first()

    if existe:
        print(f"⏭️ Já existe agendamento de {c['nome']} para {c['data']}, pulando...")
        continue

    novo = models.Agendamento(
        paciente=c.get("nome"),
        data=c.get("data"),
        hora=None,  # não tem no JSON
        local=c.get("local"),
        telefone=c.get("telefone"),
        enviado=False
    )
    db.add(novo)
    db.commit()
    print(f"✅ Adicionado: {c['nome']} - {c['data']}")

db.close()
print("\n🎯 Importação concluída!")

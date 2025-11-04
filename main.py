from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, schemas
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()

# dependencia para pegar a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ======================
#       CRUD
# ======================

# Criar agendamento
@app.post("/agendar", response_model=schemas.AgendamentoOut)
def criar_agendamento(agendamento: schemas.AgendamentoCreate, db: Session = Depends(get_db)):
    novo = models.Agendamento(**agendamento.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


# Listar todos agendamentos
@app.get("/agendamentos", response_model=list[schemas.AgendamentoOut])
def listar_agendamentos(db: Session = Depends(get_db)):
    return db.query(models.Agendamento).all()


# Buscar agendamento por ID
@app.get("/agendamentos/{agendamento_id}", response_model=schemas.AgendamentoOut)
def buscar_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    ag = db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()
    if not ag:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return ag


# Atualizar agendamento
@app.put("/agendamentos/{agendamento_id}", response_model=schemas.AgendamentoOut)
def atualizar_agendamento(agendamento_id: int, dados: schemas.AgendamentoUpdate, db: Session = Depends(get_db)):
    ag = db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()
    if not ag:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    for campo, valor in dados.dict().items():
        setattr(ag, campo, valor)

    db.commit()
    db.refresh(ag)
    return ag


# Deletar agendamento
@app.delete("/agendamentos/{agendamento_id}")
def deletar_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    ag = db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()
    if not ag:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    db.delete(ag)
    db.commit()
    return {"mensagem": "Agendamento deletado com sucesso"}


# ======================
#     FRONTEND
# ======================

# Servir arquivos estáticos (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rota raiz "/" que abre o index.html
@app.get("/")
def home():
    return FileResponse(os.path.join("static", "index.html"))


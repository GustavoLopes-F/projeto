from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    paciente = Column(String, index=True)
    telefone = Column(String)
    data = Column(String)
    hora = Column(String)
    local = Column(String)
    exame = Column(String, nullable=True)
    tipoexame = Column(String, nullable=True)
    enviado = Column(Boolean, default=False)  # 👈 NOVA COLUNA

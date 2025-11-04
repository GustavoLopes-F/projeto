from pydantic import BaseModel

# Campos base do agendamento
class AgendamentoBase(BaseModel):
    paciente: str
    telefone: str              # 👈 ADICIONADO campo telefone
    data: str
    hora: str
    local: str
    exame: str | None = None
    tipoexame: str | None = None


# Para criação de agendamento
class AgendamentoCreate(AgendamentoBase):
    pass


# Para atualização
class AgendamentoUpdate(AgendamentoBase):
    pass


# Para retorno (inclui o ID)
class AgendamentoOut(AgendamentoBase):
    id: int

    class Config:
        from_attributes = True

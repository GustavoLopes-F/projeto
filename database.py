from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Caminho do banco SQLite
DATABASE_URL = "sqlite:///./agendamentos.db"

# Cria o motor de conexão
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Cria a sessão do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

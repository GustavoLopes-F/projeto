from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# caminho do banco SQLite
DATABASE_URL = "sqlite:///./agendamentos.db"

# cria o motor de conexão
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# cria a sessão do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base para os modelos
Base = declarative_base()

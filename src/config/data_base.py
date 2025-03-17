from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==== src/Domain/user.py ====
from sqlalchemy import Column, Integer, String
from src.config.data_base import Base

class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    cnpj = Column(String)
    email = Column(String, unique=True)
    celular = Column(String)
    senha = Column(String)
    status = Column(String, default="Inativo")
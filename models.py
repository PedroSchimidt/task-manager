from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)

    tarefas = relationship("TarefaModel", back_populates="dono")


class TarefaModel(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, default="")
    concluida = Column(Boolean, default=False)
    dono_id = Column(Integer, ForeignKey("usuarios.id"))

    dono = relationship("UsuarioModel", back_populates="tarefas")
from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class TarefaModel(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, default="")
    concluida = Column(Boolean, default=False)
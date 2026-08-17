from pydantic import BaseModel

class TarefaBase(BaseModel):
    titulo: str
    descricao: str = ""
    concluida: bool = False

class TarefaCriar(TarefaBase):
    pass

class TarefaResposta(TarefaBase):
    id: int

    class Config:
        from_attributes = True
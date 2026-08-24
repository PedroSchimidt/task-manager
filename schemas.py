from pydantic import BaseModel, EmailStr

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


class UsuarioCriar(BaseModel):
    email: EmailStr
    senha: str

class UsuarioResposta(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
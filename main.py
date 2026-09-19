import os
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
import models
import schemas

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import auth

from fastapi.middleware.cors import CORSMiddleware

import random
from datetime import datetime


# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

app = FastAPI()


# =========================
# CORS
# =========================

origens_permitidas = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    os.getenv("FRONTEND_URL", ""),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# BANCO DE DADOS
# =========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# AUTENTICAÇÃO
# =========================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def obter_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = auth.decodificar_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )

    email = payload.get("sub")

    usuario = db.query(models.UsuarioModel).filter(
        models.UsuarioModel.email == email
    ).first()

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )

    return usuario


# =========================
# SUGESTÕES
# =========================

SUGESTOES_MODELO = [
    {"titulo": "Estudar Python", "categoria": "estudo", "periodo": "manha"},
    {"titulo": "Revisar anotações do dia anterior", "categoria": "estudo", "periodo": "manha"},
    {"titulo": "Planejar as tarefas da semana", "categoria": "organizacao", "periodo": "manha"},
    {"titulo": "Responder e-mails pendentes", "categoria": "trabalho", "periodo": "manha"},
    {"titulo": "Fazer uma pausa para alongamento", "categoria": "saude", "periodo": "tarde"},
    {"titulo": "Revisar código do projeto pessoal", "categoria": "estudo", "periodo": "tarde"},
    {"titulo": "Organizar arquivos e downloads", "categoria": "organizacao", "periodo": "tarde"},
    {"titulo": "Praticar exercícios de lógica de programação", "categoria": "estudo", "periodo": "tarde"},
    {"titulo": "Ler um artigo sobre tecnologia", "categoria": "estudo", "periodo": "noite"},
    {"titulo": "Planejar o dia de amanhã", "categoria": "organizacao", "periodo": "noite"},
    {"titulo": "Revisar metas da semana", "categoria": "organizacao", "periodo": "noite"},
]


def obter_periodo_do_dia() -> str:
    hora = datetime.now().hour

    if 5 <= hora < 12:
        return "manha"
    elif 12 <= hora < 18:
        return "tarde"
    else:
        return "noite"


@app.get("/sugestoes")
def obter_sugestoes(
    db: Session = Depends(get_db),
    usuario_atual: models.UsuarioModel = Depends(obter_usuario_atual)
):
    periodo_atual = obter_periodo_do_dia()

    titulos_existentes = {
        t.titulo.lower()
        for t in db.query(models.TarefaModel).filter(
            models.TarefaModel.dono_id == usuario_atual.id
        ).all()
    }

    candidatas = [
        s for s in SUGESTOES_MODELO
        if s["periodo"] == periodo_atual
        and s["titulo"].lower() not in titulos_existentes
    ]

    if not candidatas:
        candidatas = [
            s for s in SUGESTOES_MODELO
            if s["titulo"].lower() not in titulos_existentes
        ]

    quantidade = min(3, len(candidatas))

    return random.sample(candidatas, quantidade) if quantidade > 0 else []


# =========================
# ROTAS
# =========================

@app.get("/")
def read_root():
    return {"mensagem": "Minha API de tarefas está no ar!"}


@app.post("/usuarios", response_model=schemas.UsuarioResposta)
def criar_usuario(
    usuario: schemas.UsuarioCriar,
    db: Session = Depends(get_db)
):
    usuario_existente = db.query(models.UsuarioModel).filter(
        models.UsuarioModel.email == usuario.email
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )

    novo_usuario = models.UsuarioModel(
        email=usuario.email,
        senha_hash=auth.hash_senha(usuario.senha)
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


@app.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = db.query(models.UsuarioModel).filter(
        models.UsuarioModel.email == form_data.username
    ).first()

    if not usuario or not auth.verificar_senha(
        form_data.password,
        usuario.senha_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Email ou senha incorretos"
        )

    token = auth.criar_token_acesso({"sub": usuario.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/tarefas", response_model=list[schemas.TarefaResposta])
def listar_tarefas(
    db: Session = Depends(get_db),
    usuario_atual: models.UsuarioModel = Depends(obter_usuario_atual)
):
    return db.query(models.TarefaModel).filter(
        models.TarefaModel.dono_id == usuario_atual.id
    ).all()


@app.post("/tarefas", response_model=schemas.TarefaResposta)
def criar_tarefa(
    tarefa: schemas.TarefaCriar,
    db: Session = Depends(get_db),
    usuario_atual: models.UsuarioModel = Depends(obter_usuario_atual)
):
    nova_tarefa = models.TarefaModel(
        **tarefa.model_dump(),
        dono_id=usuario_atual.id
    )

    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)

    return nova_tarefa


@app.get("/tarefas/{tarefa_id}", response_model=schemas.TarefaResposta)
def buscar_tarefa(
    tarefa_id: int,
    db: Session = Depends(get_db),
    usuario_atual: models.UsuarioModel = Depends(obter_usuario_atual)
):
    tarefa = db.query(models.TarefaModel).filter(
        models.TarefaModel.id == tarefa_id,
        models.TarefaModel.dono_id == usuario_atual.id
    ).first()

    if not tarefa:
        raise HTTPException(
            status_code=404,
            detail="Tarefa não encontrada"
        )

    return tarefa


@app.put("/tarefas/{tarefa_id}", response_model=schemas.TarefaResposta)
def atualizar_tarefa(
    tarefa_id: int,
    tarefa_atualizada: schemas.TarefaCriar,
    db: Session = Depends(get_db),
    usuario_atual: models.UsuarioModel = Depends(obter_usuario_atual)
):
    tarefa = db.query(models.TarefaModel).filter(
        models.TarefaModel.id == tarefa_id,
        models.TarefaModel.dono_id == usuario_atual.id
    ).first()

    if not tarefa:
        raise HTTPException(
            status_code=404,
            detail="Tarefa não encontrada"
        )

    for campo, valor in tarefa_atualizada.model_dump().items():
        setattr(tarefa, campo, valor)

    db.commit()
    db.refresh(tarefa)

    return tarefa


@app.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(
    tarefa_id: int,
    db: Session = Depends(get_db),
    usuario_atual: models.UsuarioModel = Depends(obter_usuario_atual)
):
    tarefa = db.query(models.TarefaModel).filter(
        models.TarefaModel.id == tarefa_id,
        models.TarefaModel.dono_id == usuario_atual.id
    ).first()

    if not tarefa:
        raise HTTPException(
            status_code=404,
            detail="Tarefa não encontrada"
        )

    db.delete(tarefa)
    db.commit()

    return {"mensagem": "Tarefa deletada com sucesso"}
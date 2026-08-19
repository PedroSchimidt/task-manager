from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
import models
import schemas

# Cria as tabelas no banco (se ainda não existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Fornece uma sessão do banco pra cada requisição, e garante que ela é fechada depois
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"mensagem": "Minha API de tarefas está no ar!"}

@app.get("/tarefas", response_model=list[schemas.TarefaResposta])
def listar_tarefas(db: Session = Depends(get_db)):
    return db.query(models.TarefaModel).all()

@app.post("/tarefas", response_model=schemas.TarefaResposta)
def criar_tarefa(tarefa: schemas.TarefaCriar, db: Session = Depends(get_db)):
    nova_tarefa = models.TarefaModel(**tarefa.model_dump())
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa

@app.get("/tarefas/{tarefa_id}", response_model=schemas.TarefaResposta)
def buscar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(models.TarefaModel).filter(models.TarefaModel.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

@app.put("/tarefas/{tarefa_id}", response_model=schemas.TarefaResposta)
def atualizar_tarefa(tarefa_id: int, tarefa_atualizada: schemas.TarefaCriar, db: Session = Depends(get_db)):
    tarefa = db.query(models.TarefaModel).filter(models.TarefaModel.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    for campo, valor in tarefa_atualizada.model_dump().items():
        setattr(tarefa, campo, valor)
    db.commit()
    db.refresh(tarefa)
    return tarefa

@app.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(models.TarefaModel).filter(models.TarefaModel.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(tarefa)
    db.commit()
    return {"mensagem": "Tarefa deletada com sucesso"}
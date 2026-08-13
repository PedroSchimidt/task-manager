from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Tarefa(BaseModel):
    titulo: str
    descricao: str = ""
    concluida: bool = False

# Nosso "banco" em memória: um dicionário {id: tarefa}
tarefas: dict[int, Tarefa] = {}
proximo_id = 1

@app.get("/")
def read_root():
    return {"mensagem": "Minha API de tarefas está no ar!"}

@app.get("/tarefas")
def listar_tarefas():
    return tarefas

@app.post("/tarefas")
def criar_tarefa(tarefa: Tarefa):
    global proximo_id
    tarefas[proximo_id] = tarefa
    proximo_id += 1
    return tarefa

@app.get("/tarefas/{tarefa_id}")
def buscar_tarefa(tarefa_id: int):
    if tarefa_id not in tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefas[tarefa_id]

@app.put("/tarefas/{tarefa_id}")
def atualizar_tarefa(tarefa_id: int, tarefa_atualizada: Tarefa):
    if tarefa_id not in tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tarefas[tarefa_id] = tarefa_atualizada
    return tarefas[tarefa_id]

@app.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(tarefa_id: int):
    if tarefa_id not in tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    del tarefas[tarefa_id]
    return {"mensagem": "Tarefa deletada com sucesso"}
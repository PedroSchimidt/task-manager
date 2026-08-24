import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app, get_db
from database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_criar_tarefa():
    resposta = client.post("/tarefas", json={"titulo": "Estudar Pytest"})
    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados["titulo"] == "Estudar Pytest"
    assert dados["concluida"] == False


def test_listar_tarefas():
    resposta = client.get("/tarefas")
    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)


def test_buscar_tarefa_inexistente():
    resposta = client.get("/tarefas/9999")
    assert resposta.status_code == 404
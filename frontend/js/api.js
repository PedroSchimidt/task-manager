const API_URL = "http://127.0.0.1:8000";

async function cadastrarUsuario(email, senha) {
  const resposta = await fetch(`${API_URL}/usuarios`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, senha }),
  });

  const dados = await resposta.json();

  if (!resposta.ok) {
    throw new Error(dados.detail || "Não foi possível criar a conta");
  }

  return dados;
}

async function login(email, senha) {
  const corpo = new URLSearchParams();
  corpo.append("username", email);
  corpo.append("password", senha);

  const resposta = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: corpo,
  });

  const dados = await resposta.json();

  if (!resposta.ok) {
    throw new Error(dados.detail || "Não foi possível entrar");
  }

  return dados;
}

function obterCabecalhosAutenticados() {
  const token = localStorage.getItem("token");
  return {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`,
  };
}

async function listarTarefas() {
  const resposta = await fetch(`${API_URL}/tarefas`, {
    headers: obterCabecalhosAutenticados(),
  });

  if (resposta.status === 401) {
    throw new Error("SESSAO_EXPIRADA");
  }

  return await resposta.json();
}

async function criarTarefa(titulo, descricao) {
  const resposta = await fetch(`${API_URL}/tarefas`, {
    method: "POST",
    headers: obterCabecalhosAutenticados(),
    body: JSON.stringify({ titulo, descricao }),
  });
  return await resposta.json();
}

async function atualizarTarefa(id, titulo, descricao, concluida) {
  const resposta = await fetch(`${API_URL}/tarefas/${id}`, {
    method: "PUT",
    headers: obterCabecalhosAutenticados(),
    body: JSON.stringify({ titulo, descricao, concluida }),
  });
  return await resposta.json();
}

async function deletarTarefa(id) {
  await fetch(`${API_URL}/tarefas/${id}`, {
    method: "DELETE",
    headers: obterCabecalhosAutenticados(),
  });
}
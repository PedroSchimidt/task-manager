// ===== Proteção da rota: exige token =====

const token = localStorage.getItem("token");
if (!token) {
  window.location.href = "index.html";
}

// ===== Referências dos elementos da tela =====

const listaTarefasEl = document.getElementById("lista-tarefas");
const estadoVazioEl = document.getElementById("estado-vazio");
const tituloPaginaEl = document.getElementById("titulo-pagina");
const subtituloPaginaEl = document.getElementById("subtitulo-pagina");
const contagemTodasEl = document.getElementById("contagem-todas");
const contagemPendentesEl = document.getElementById("contagem-pendentes");
const contagemConcluidasEl = document.getElementById("contagem-concluidas");
const emailUsuarioEl = document.getElementById("email-usuario");
const avatarUsuarioEl = document.getElementById("avatar-usuario");

const modalFundoEl = document.getElementById("modal-fundo");
const modalTituloEl = document.getElementById("modal-titulo");
const formTarefaEl = document.getElementById("form-tarefa");
const tarefaIdEl = document.getElementById("tarefa-id");
const tarefaTituloEl = document.getElementById("tarefa-titulo");
const tarefaDescricaoEl = document.getElementById("tarefa-descricao");

let todasAsTarefas = [];
let filtroAtual = "todas";

// ===== Carregar dados iniciais =====

async function carregarTarefas() {
  try {
    todasAsTarefas = await listarTarefas();
    renderizarTarefas();
  } catch (erro) {
    if (erro.message === "SESSAO_EXPIRADA") {
      localStorage.removeItem("token");
      window.location.href = "index.html";
    }
  }
}

function carregarUsuario() {
  const payload = JSON.parse(atob(token.split(".")[1]));
  const email = payload.sub;
  emailUsuarioEl.textContent = email;
  avatarUsuarioEl.textContent = email.charAt(0);
}

// ===== Renderizar a lista de tarefas na tela =====

function renderizarTarefas() {
  const pendentes = todasAsTarefas.filter((t) => !t.concluida);
  const concluidas = todasAsTarefas.filter((t) => t.concluida);

  contagemTodasEl.textContent = todasAsTarefas.length;
  contagemPendentesEl.textContent = pendentes.length;
  contagemConcluidasEl.textContent = concluidas.length;

  const total = todasAsTarefas.length;
  const porcentagem = total === 0 ? 0 : Math.round((concluidas.length / total) * 100);

  document.getElementById("anel-progresso").style.setProperty("--progresso", porcentagem);
  document.getElementById("anel-porcentagem").textContent = `${porcentagem}%`;
  document.getElementById("stat-total").textContent = total;
  document.getElementById("stat-pendentes").textContent = pendentes.length;
  document.getElementById("stat-concluidas").textContent = concluidas.length;

  let tarefasFiltradas = todasAsTarefas;
  if (filtroAtual === "pendentes") tarefasFiltradas = pendentes;
  if (filtroAtual === "concluidas") tarefasFiltradas = concluidas;

  listaTarefasEl.innerHTML = "";

  if (tarefasFiltradas.length === 0) {
    estadoVazioEl.classList.remove("escondido");
    listaTarefasEl.classList.add("escondido");
    return;
  }

  estadoVazioEl.classList.add("escondido");
  listaTarefasEl.classList.remove("escondido");

  tarefasFiltradas.forEach((tarefa, indice) => {
    const cartao = document.createElement("div");
    cartao.className = "cartao-tarefa" + (tarefa.concluida ? " concluida" : "");
    cartao.style.animationDelay = `${indice * 0.04}s`;

    cartao.innerHTML = `
      <button class="check-tarefa" data-id="${tarefa.id}" aria-label="Marcar como concluída">
        <svg viewBox="0 0 12 12" fill="none"><path d="M2 6.2L4.6 8.8L10 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
      <div class="corpo-tarefa">
        <span class="titulo-tarefa">${tarefa.titulo}<span class="risco-conclusao"></span></span>
        ${tarefa.descricao ? `<p class="descricao-tarefa">${tarefa.descricao}</p>` : ""}
      </div>
      <div class="acoes-tarefa">
        <button class="botao-icone editar" data-id="${tarefa.id}" aria-label="Editar">
          <svg viewBox="0 0 16 16" fill="none"><path d="M11.5 2.5L13.5 4.5L5 13H3V11L11.5 2.5Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>
        </button>
        <button class="botao-icone excluir" data-id="${tarefa.id}" aria-label="Excluir">
          <svg viewBox="0 0 16 16" fill="none"><path d="M3 4.5H13M6 4.5V3C6 2.5 6.5 2 7 2H9C9.5 2 10 2.5 10 3V4.5M11.5 4.5V13C11.5 13.5 11 14 10.5 14H5.5C5 14 4.5 13.5 4.5 13V4.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
      </div>
    `;

    listaTarefasEl.appendChild(cartao);
  });
}

// ===== Alternar filtros (Todas / Pendentes / Concluídas) =====

document.querySelectorAll(".filtro-btn").forEach((botao) => {
  botao.addEventListener("click", () => {
    document.querySelectorAll(".filtro-btn").forEach((b) => b.classList.remove("ativo"));
    botao.classList.add("ativo");
    filtroAtual = botao.dataset.filtro;

    const titulos = {
      todas: ["Todas as tarefas", "Tudo o que você precisa fazer."],
      pendentes: ["Tarefas pendentes", "O que ainda está por vir."],
      concluidas: ["Tarefas concluídas", "Olha só o que você já resolveu."],
    };
    tituloPaginaEl.textContent = titulos[filtroAtual][0];
    subtituloPaginaEl.textContent = titulos[filtroAtual][1];

    renderizarTarefas();
  });
});


function confirmarAcao(mensagem, subtitulo = "Essa ação não pode ser desfeita.", textoBotao = "Confirmar") {
  return new Promise((resolve) => {
    const modal = document.getElementById("modal-confirmacao");
    const textoEl = document.getElementById("texto-confirmacao");
    const subtituloEl = document.querySelector("#modal-confirmacao .subtitulo-confirmacao");
    const botaoConfirmar = document.getElementById("botao-confirmar-confirmacao");
    const botaoCancelar = document.getElementById("botao-cancelar-confirmacao");

    textoEl.textContent = mensagem;
    subtituloEl.textContent = subtitulo;
    botaoConfirmar.textContent = textoBotao;
    modal.classList.remove("escondido");

    function limpar(resultado) {
      modal.classList.add("escondido");
      botaoConfirmar.removeEventListener("click", aoConfirmar);
      botaoCancelar.removeEventListener("click", aoCancelar);
      resolve(resultado);
    }

    function aoConfirmar() { limpar(true); }
    function aoCancelar() { limpar(false); }

    botaoConfirmar.addEventListener("click", aoConfirmar);
    botaoCancelar.addEventListener("click", aoCancelar);
  });
}
// ===== Clique em marcar/editar/excluir (delegação de eventos) =====

listaTarefasEl.addEventListener("click", async (evento) => {
  const botaoCheck = evento.target.closest(".check-tarefa");
  const botaoEditar = evento.target.closest(".editar");
  const botaoExcluir = evento.target.closest(".excluir");

  if (botaoCheck) {
    const id = botaoCheck.dataset.id;
    const tarefa = todasAsTarefas.find((t) => t.id == id);
    await atualizarTarefa(id, tarefa.titulo, tarefa.descricao, !tarefa.concluida);
    await carregarTarefas();
  }

  if (botaoEditar) {
    const id = botaoEditar.dataset.id;
    const tarefa = todasAsTarefas.find((t) => t.id == id);
    abrirModal(tarefa);
  }

      if (botaoExcluir) {
    const id = botaoExcluir.dataset.id;
    const confirmado = await confirmarAcao(
      "Tem certeza que deseja excluir essa tarefa?",
      "Essa ação não pode ser desfeita.",
      "Excluir"
    );
    if (confirmado) {
      await deletarTarefa(id);
      await carregarTarefas();
    }
  }
});

// ===== Modal: abrir, fechar, salvar =====

function abrirModal(tarefa = null) {
  if (tarefa) {
    modalTituloEl.textContent = "Editar tarefa";
    tarefaIdEl.value = tarefa.id;
    tarefaTituloEl.value = tarefa.titulo;
    tarefaDescricaoEl.value = tarefa.descricao || "";
  } else {
    modalTituloEl.textContent = "Nova tarefa";
    formTarefaEl.reset();
    tarefaIdEl.value = "";
  }
  modalFundoEl.classList.remove("escondido");
  tarefaTituloEl.focus();
}

function fecharModal() {
  modalFundoEl.classList.add("escondido");
}

document.getElementById("botao-abrir-modal").addEventListener("click", () => abrirModal());
document.getElementById("botao-cancelar-modal").addEventListener("click", fecharModal);
modalFundoEl.addEventListener("click", (evento) => {
  if (evento.target === modalFundoEl) fecharModal();
});

formTarefaEl.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const id = tarefaIdEl.value;
  const titulo = tarefaTituloEl.value;
  const descricao = tarefaDescricaoEl.value;

  if (id) {
    const tarefaAtual = todasAsTarefas.find((t) => t.id == id);
    await atualizarTarefa(id, titulo, descricao, tarefaAtual.concluida);
  } else {
    await criarTarefa(titulo, descricao);
  }

  fecharModal();
  await carregarTarefas();
});

// ===== Logout =====

document.getElementById("botao-sair").addEventListener("click", async () => {
  const confirmado = await confirmarAcao(
    "Deseja sair da sua conta?",
    "Você precisará entrar novamente para ver suas tarefas.",
    "Sair"
  );
  if (confirmado) {
    localStorage.removeItem("token");
    window.location.href = "index.html";
  }
});
// ===== Inicialização =====

carregarUsuario();
carregarTarefas();
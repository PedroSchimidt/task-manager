// ===== Alternar entre abas "Entrar" e "Criar conta" =====

const botoesAba = document.querySelectorAll(".aba-btn");
const formEntrar = document.getElementById("form-entrar");
const formCadastrar = document.getElementById("form-cadastrar");
const indicador = document.getElementById("aba-indicador");
const tituloCartao = document.getElementById("titulo-cartao");
const subtituloCartao = document.getElementById("subtitulo-cartao");

botoesAba.forEach((botao) => {
  botao.addEventListener("click", () => {
    const aba = botao.dataset.aba;

    botoesAba.forEach((b) => b.classList.remove("ativa"));
    botao.classList.add("ativa");

    if (aba === "entrar") {
      formEntrar.classList.remove("escondido");
      formCadastrar.classList.add("escondido");
      indicador.classList.remove("deslocado");
      tituloCartao.textContent = "Bem-vindo de volta";
      subtituloCartao.textContent = "Entre para ver suas tarefas.";
    } else {
      formEntrar.classList.add("escondido");
      formCadastrar.classList.remove("escondido");
      indicador.classList.add("deslocado");
      tituloCartao.textContent = "Criar sua conta";
      subtituloCartao.textContent = "Leva menos de um minuto.";
    }
  });
});

// ===== Mostrar/ocultar senha =====

document.querySelectorAll(".botao-olho").forEach((botao) => {
  botao.addEventListener("click", () => {
    const campo = document.getElementById(botao.dataset.alvo);
    campo.type = campo.type === "password" ? "text" : "password";
  });
});

// ===== Envio do formulário de login =====

formEntrar.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const email = document.getElementById("entrar-email").value;
  const senha = document.getElementById("entrar-senha").value;
  const erroEl = document.getElementById("erro-entrar");
  erroEl.textContent = "";

  try {
    const dados = await login(email, senha);
    localStorage.setItem("token", dados.access_token);
    window.location.href = "dashboard.html";
  } catch (erro) {
    erroEl.textContent = erro.message;
  }
});

// ===== Envio do formulário de cadastro =====

formCadastrar.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const email = document.getElementById("cadastrar-email").value;
  const senha = document.getElementById("cadastrar-senha").value;
  const erroEl = document.getElementById("erro-cadastrar");
  erroEl.textContent = "";

  try {
    await cadastrarUsuario(email, senha);
    const dados = await login(email, senha);
    localStorage.setItem("token", dados.access_token);
    window.location.href = "dashboard.html";
  } catch (erro) {
    erroEl.textContent = erro.message;
  }
});
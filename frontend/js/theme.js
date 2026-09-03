(function () {
  const temaSalvo = localStorage.getItem("tema") || "escuro";
  document.documentElement.setAttribute("data-tema", temaSalvo);
})();

document.addEventListener("DOMContentLoaded", () => {
  const botaoTema = document.getElementById("botao-tema");

  botaoTema.addEventListener("click", () => {
    const temaAtual = document.documentElement.getAttribute("data-tema");
    const novoTema = temaAtual === "claro" ? "escuro" : "claro";

    document.documentElement.setAttribute("data-tema", novoTema);
    localStorage.setItem("tema", novoTema);
  });
});
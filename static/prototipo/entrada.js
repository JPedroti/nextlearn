// Tela de entrada: o Next troca de cenário e de cor a cada 5 s (pausável, para quem prefere sem movimento).
(function () {
  var palco = document.querySelector(".palco");
  var cenas = JSON.parse(document.getElementById("dados-cenas").textContent);
  var fala = document.querySelector("[data-fala]");
  var pontos = document.querySelectorAll("[data-ir]");
  var botaoPausa = document.querySelector("[data-pausa]");
  var reduzir = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var atual = 0, timer = null, pausado = reduzir;

  function mostrar(i) {
    atual = (i + cenas.length) % cenas.length;
    palco.dataset.cena = cenas[atual].id;
    fala.textContent = cenas[atual].fala;
    pontos.forEach(function (p, j) { if (j === atual) p.setAttribute("aria-current", "true"); else p.removeAttribute("aria-current"); });
  }
  function tocar() { clearInterval(timer); if (!pausado) timer = setInterval(function () { mostrar(atual + 1); }, 5000); }
  function atualizarPausa() { botaoPausa.textContent = pausado ? "Continuar" : "Pausar"; botaoPausa.setAttribute("aria-pressed", pausado ? "true" : "false"); }

  pontos.forEach(function (p) { p.addEventListener("click", function () { mostrar(Number(p.dataset.ir)); tocar(); }); });
  botaoPausa.addEventListener("click", function () { pausado = !pausado; atualizarPausa(); tocar(); });
  atualizarPausa(); tocar();

  // Janela de entrar/cadastrar: as três opções levam ao mesmo login (o papel está no usuário).
  var janela = document.querySelector("[data-janela]");
  document.querySelectorAll("[data-abrir]").forEach(function (b) {
    b.addEventListener("click", function () {
      var cadastro = b.dataset.abrir === "cadastro";
      janela.querySelector("[data-titulo]").textContent = cadastro ? "Criar acesso" : "Entrar como";
      janela.querySelector("[data-sub]").textContent = cadastro
        ? "No NextLearn, quem cria os acessos é a escola e o professor. Veja como funciona para você:"
        : "Escolha quem você é. Depois é só usuário e senha.";
      janela.querySelectorAll("[data-desc-entrar]").forEach(function (e) { e.hidden = cadastro; });
      janela.querySelectorAll("[data-desc-cadastro]").forEach(function (e) { e.hidden = !cadastro; });
      janela.querySelectorAll(".opcao-papel").forEach(function (a) {
        if (cadastro) { a.dataset.href = a.dataset.href || a.getAttribute("href"); a.removeAttribute("href"); a.setAttribute("role", "note"); }
        else if (a.dataset.href) { a.setAttribute("href", a.dataset.href); a.removeAttribute("role"); }
      });
      janela.showModal();
    });
  });
})();

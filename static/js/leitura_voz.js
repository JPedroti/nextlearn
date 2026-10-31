// Leitura em voz alta com a Web Speech API do próprio navegador: nada é enviado para servidor nenhum.
// Cada botão com data-ouvir="id1 id2" lê o texto desses elementos. Clicar de novo para a leitura.
(function () {
  var botoes = document.querySelectorAll("[data-ouvir]");
  if (!botoes.length) return;

  if (!("speechSynthesis" in window)) {
    botoes.forEach(function (botao) {
      botao.disabled = true;
      botao.textContent = "Leitura em voz alta indisponível neste navegador";
    });
    return;
  }

  var voz = null;
  function escolherVoz() {
    var vozes = window.speechSynthesis.getVoices();
    voz =
      vozes.find(function (v) { return /^pt[-_]BR/i.test(v.lang); }) ||
      vozes.find(function (v) { return /^pt/i.test(v.lang); }) ||
      null;
  }
  escolherVoz();
  window.speechSynthesis.onvoiceschanged = escolherVoz;

  var botaoAtivo = null;
  function pararTudo() {
    window.speechSynthesis.cancel();
    if (botaoAtivo) {
      botaoAtivo.textContent = botaoAtivo.dataset.rotulo;
      botaoAtivo.setAttribute("aria-pressed", "false");
      botaoAtivo = null;
    }
  }

  botoes.forEach(function (botao) {
    botao.dataset.rotulo = botao.textContent;
    botao.addEventListener("click", function () {
      var eraEste = botaoAtivo === botao;
      pararTudo();
      if (eraEste) return;

      var texto = botao.dataset.ouvir
        .split(" ")
        .map(function (id) {
          var elemento = document.getElementById(id);
          return elemento ? elemento.innerText : "";
        })
        .join("\n");
      // Frases curtas uma de cada vez: alguns navegadores cortam falas longas no meio.
      var trechos = texto.split(/(?<=[.!?:;])\s+|\n+/).filter(function (t) { return t.trim(); });
      if (!trechos.length) return;

      botaoAtivo = botao;
      botao.textContent = "Parar leitura";
      botao.setAttribute("aria-pressed", "true");
      trechos.forEach(function (trecho, i) {
        var fala = new SpeechSynthesisUtterance(trecho);
        fala.lang = "pt-BR";
        fala.rate = 0.95;
        if (voz) fala.voice = voz;
        if (i === trechos.length - 1) {
          fala.onend = function () {
            if (botaoAtivo === botao) pararTudo();
          };
        }
        window.speechSynthesis.speak(fala);
      });
    });
  });
})();

// Tela da aula do aluno: mostra uma parte por vez (passos do texto, questões e correção), com "anterior" e "próximo".
// Sem JavaScript, tudo aparece de uma vez e a página continua funcionando (o servidor confere as respostas).
(function () {
  // Cada bloco [data-paginas="Nome"] tem itens [data-pagina], um contador, e botões [data-anterior] e [data-proximo].
  function paginar(bloco) {
    var paginas = Array.prototype.slice.call(bloco.querySelectorAll("[data-pagina]"));
    if (paginas.length < 2) return null;
    var anterior = bloco.querySelector("[data-anterior]");
    var proximo = bloco.querySelector("[data-proximo]");
    var contador = bloco.querySelector("[data-contador]");
    var barraPassos = bloco.querySelector("[data-barra-passos]");
    var nome = bloco.dataset.paginas;
    var atual = 0;
    if (barraPassos) barraPassos.parentElement.hidden = false;

    function mostrar(indice, rolar) {
      atual = indice;
      paginas.forEach(function (pagina, i) { pagina.hidden = i !== indice; });
      var ultima = indice === paginas.length - 1;
      anterior.disabled = indice === 0;
      proximo.textContent = ultima ? proximo.dataset.rotuloFim : proximo.dataset.rotulo;
      proximo.disabled = ultima && !proximo.dataset.irPara;
      if (contador) {
        contador.hidden = false;
        contador.textContent = nome + " " + (indice + 1) + " de " + paginas.length;
      }
      if (barraPassos) barraPassos.style.width = (100 * (indice + 1) / paginas.length) + "%";
      if (rolar) bloco.scrollIntoView({ block: "start" });
    }

    anterior.addEventListener("click", function () {
      if (atual > 0) mostrar(atual - 1, true);
    });
    proximo.addEventListener("click", function () {
      if (atual < paginas.length - 1) {
        mostrar(atual + 1, true);
      } else if (proximo.dataset.irPara) {
        document.getElementById(proximo.dataset.irPara).scrollIntoView({ block: "start" });
      }
    });
    bloco.querySelector("[data-navegacao]").hidden = false;
    mostrar(0, false);
    return { mostrar: mostrar, paginas: paginas };
  }

  document.querySelectorAll("[data-paginas]").forEach(function (bloco) {
    var paginador = paginar(bloco);
    if (!bloco.hasAttribute("data-respostas")) return;

    // Formulário de respostas: barra de progresso e aviso se faltar alguma questão.
    var questoes = Array.prototype.slice.call(bloco.querySelectorAll("fieldset[data-pagina]"));
    var barra = bloco.querySelector("[data-barra]");
    var respondidas = bloco.querySelector("[data-respondidas]");
    var faltam = bloco.querySelector("[data-faltam]");

    function semResposta() {
      return questoes.filter(function (q) { return !q.querySelector("input[type=radio]:checked"); });
    }
    function atualizar() {
      var feitas = questoes.length - semResposta().length;
      respondidas.textContent = feitas + " de " + questoes.length + " respondida" + (feitas === 1 ? "" : "s");
      barra.style.width = (100 * feitas / questoes.length) + "%";
      if (!semResposta().length) faltam.hidden = true;
    }

    bloco.querySelector("[data-progresso]").hidden = false;
    if (!paginador) bloco.querySelector("[data-contador]").textContent = "";
    // A validação do navegador não consegue apontar uma questão escondida; este script faz a conferência no lugar dela.
    bloco.noValidate = true;
    bloco.addEventListener("change", atualizar);
    bloco.addEventListener("submit", function (evento) {
      var pendentes = semResposta();
      if (!pendentes.length) return;
      evento.preventDefault();
      faltam.hidden = false;
      if (paginador) paginador.mostrar(questoes.indexOf(pendentes[0]), true);
    });
    atualizar();
  });

  // Modo concentração: tela cheia, sem abas nem barras do navegador. Só aparece onde o navegador permite.
  var telaCheia = document.querySelector("[data-tela-cheia]");
  if (telaCheia && document.fullscreenEnabled) {
    telaCheia.hidden = false;
    telaCheia.addEventListener("click", function () {
      if (document.fullscreenElement) {
        document.exitFullscreen();
      } else {
        document.documentElement.requestFullscreen();
      }
    });
    document.addEventListener("fullscreenchange", function () {
      telaCheia.textContent = document.fullscreenElement ? "Sair do modo concentração" : "Modo concentração";
    });
  }
})();

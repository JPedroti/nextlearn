// Protótipo NextLearn: preferências (salvas no navegador), leitura em voz alta, passos e questões.
(function () {
  var body = document.body;
  var aviso = document.getElementById("aviso");
  function avisar(texto) {
    aviso.textContent = texto;
    aviso.classList.add("visivel");
    setTimeout(function () { aviso.classList.remove("visivel"); }, 2200);
  }
  function ler(chave) { try { return localStorage.getItem("nl-" + chave) === "1"; } catch (e) { return false; } }
  function gravar(chave, v) { try { localStorage.setItem("nl-" + chave, v ? "1" : "0"); } catch (e) {} }

  // Preferências de interface (no app real: vêm do Perfil e geram EventoUso)
  ["letras", "voz"].forEach(function (pref) {
    var ligado = ler(pref);
    body.classList.toggle("pref-" + pref, ligado);
    document.querySelectorAll('[data-pref="' + pref + '"]').forEach(function (b) {
      b.setAttribute("aria-pressed", ligado ? "true" : "false");
      b.addEventListener("click", function () {
        ligado = !ligado;
        gravar(pref, ligado);
        body.classList.toggle("pref-" + pref, ligado);
        document.querySelectorAll('[data-pref="' + pref + '"]').forEach(function (x) { x.setAttribute("aria-pressed", ligado ? "true" : "false"); });
        avisar((ligado ? "Ligado: " : "Desligado: ") + b.textContent.trim());
      });
    });
  });

  // Leitura em voz alta (Web Speech API, voz pt-BR)
  var falando = null;
  document.querySelectorAll("[data-ouvir]").forEach(function (botao) {
    botao.addEventListener("click", function () {
      if (!("speechSynthesis" in window)) { avisar("Seu navegador não tem leitura em voz alta."); return; }
      if (falando === botao) { speechSynthesis.cancel(); return; }
      speechSynthesis.cancel();
      var texto = Array.prototype.map.call(document.querySelectorAll(botao.dataset.ouvir), function (el) { return el.innerText; }).join(" ");
      var fala = new SpeechSynthesisUtterance(texto);
      fala.lang = "pt-BR";
      fala.rate = 0.95;
      var rotulo = botao.textContent;
      fala.onstart = function () { falando = botao; botao.textContent = "Parar"; };
      fala.onend = fala.onerror = function () { falando = null; botao.textContent = rotulo; };
      speechSynthesis.speak(fala);
    });
  });

  // Aula em passos (apoio de foco)
  var bloco = document.querySelector("[data-passos]");
  if (bloco) {
    var passos = bloco.querySelectorAll("[data-passo]");
    var atual = 0;
    var contador = bloco.querySelector("[data-contador]");
    var barra = bloco.querySelector("[data-barra]");
    var ant = bloco.querySelector("[data-anterior]");
    var prox = bloco.querySelector("[data-proximo]");
    function mostrar() {
      passos.forEach(function (p, i) { p.hidden = i !== atual; });
      contador.textContent = "Passo " + (atual + 1) + " de " + passos.length;
      barra.style.width = ((atual + 1) / passos.length * 100) + "%";
      ant.disabled = atual === 0;
      prox.textContent = atual === passos.length - 1 ? "Ir para as questões" : "Próximo passo";
    }
    ant.addEventListener("click", function () { if (atual > 0) { atual--; mostrar(); } });
    prox.addEventListener("click", function () {
      if (atual < passos.length - 1) { atual++; mostrar(); passos[atual].querySelector("h2").focus && passos[atual].querySelector("h2").setAttribute("tabindex", "-1"); passos[atual].querySelector("h2").focus(); }
      else { document.getElementById("q-titulo").scrollIntoView({ behavior: "auto" }); }
    });
    mostrar();
  }

  // Questões: feedback na hora, com texto (não só cor)
  var quiz = document.querySelector("[data-quiz]");
  if (quiz) {
    quiz.addEventListener("submit", function (e) {
      e.preventDefault();
      var acertos = 0, total = 0;
      quiz.querySelectorAll("fieldset[data-correta]").forEach(function (f) {
        total++;
        var marcada = f.querySelector("input:checked");
        var certa = marcada && marcada.value === f.dataset.correta;
        if (certa) acertos++;
        var fb = f.querySelector("[data-feedback]");
        var letra = String.fromCharCode(65 + Number(f.dataset.correta));
        fb.textContent = certa ? "✓ Certo!" : "✗ Ainda não. A resposta certa é a " + letra + ".";
        fb.hidden = false;
      });
      avisar("Você acertou " + acertos + " de " + total + ".");
    });
  }

  // Sugestões do professor (no app real: SugestaoPerfil.aceitar/recusar)
  document.querySelectorAll("[data-decidir]").forEach(function (b) {
    b.addEventListener("click", function () {
      var card = b.closest("[data-sugestao]");
      card.innerHTML = '<p class="font-bold">' + (b.dataset.decidir === "aceita" ? "Sugestão aceita. O perfil do aluno foi atualizado." : "Sugestão recusada.") + "</p>";
      avisar(b.dataset.decidir === "aceita" ? "Sugestão aceita" : "Sugestão recusada");
    });
  });
})();

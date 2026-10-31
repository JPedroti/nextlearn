// Tela de entrada do NextLearn: o Next troca de pose e de cor (hero) e, com o scroll,
// anda até a beirada, salta, mergulha e nada pelo "Saiba mais".
(function () {
  var body = document.body;
  var cenas = JSON.parse(document.getElementById("dados-cenas").textContent);
  var historia = document.querySelector(".historia");
  var mundo = document.querySelector(".mundo");
  var decor = document.querySelector(".decor");
  var ator = document.querySelector(".ator");
  var hero = document.querySelector(".hero");
  var submerso = document.querySelector(".submerso");
  var frase = document.querySelector(".frase-mar");
  var respingo = document.querySelector(".respingo");
  var nadador = document.querySelector(".nadador");
  var fala = document.querySelector("[data-fala]");
  var pontos = document.querySelectorAll("[data-ir]");
  var botaoPausa = document.querySelector("[data-pausa]");
  var reduzir = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---------- Hero: pose + cor + fala ----------
  var atual = 0, timer = null, pausado = reduzir, progresso = 0;
  function mostrar(i) {
    atual = (i + cenas.length) % cenas.length;
    body.dataset.cena = cenas[atual].id;
    if (progresso < 0.03) ator.dataset.pose = cenas[atual].pose;
    fala.textContent = cenas[atual].fala;
    pontos.forEach(function (p, j) { if (j === atual) p.setAttribute("aria-current", "true"); else p.removeAttribute("aria-current"); });
  }
  function tocar() {
    clearInterval(timer);
    if (!pausado) timer = setInterval(function () { if (progresso < 0.02) mostrar(atual + 1); }, 5000);
  }
  function rotuloPausa() { botaoPausa.textContent = pausado ? "Continuar" : "Pausar"; botaoPausa.setAttribute("aria-pressed", pausado ? "true" : "false"); }
  pontos.forEach(function (p) { p.addEventListener("click", function () { mostrar(Number(p.dataset.ir)); tocar(); }); });
  botaoPausa.addEventListener("click", function () { pausado = !pausado; rotuloPausa(); tocar(); });
  rotuloPausa(); tocar();

  // ---------- Utilidades ----------
  function clamp(v, a, b) { return Math.min(b, Math.max(a, v)); }
  function faixa(p, a, b) { return clamp((p - a) / (b - a), 0, 1); }      // 0..1 dentro do trecho [a, b]
  function suave(t) { return t * t * (3 - 2 * t); }
  function lerp(a, b, t) { return a + (b - a) * t; }

  // ---------- Cena guiada pelo scroll ----------
  var W, H, A, AH;
  function medir() { W = innerWidth; H = innerHeight; A = ator.offsetWidth; AH = A * 260 / 340; }

  function quadro() {
    var y = scrollY;
    var total = historia.offsetHeight - H;
    var p = clamp((y - historia.offsetTop) / total, 0, 1);
    progresso = p;

    var chaoTopo = 0.748 * H;          // topo do chão (ver .terreno no CSS)
    var beirada = 1.52 * W;            // x da beirada do penhasco
    var superficie = 0.92 * H;         // linha d'água
    var emPe = chaoTopo - AH * 0.79;   // y do Next em pé (pés no chão)
    var x0 = W * (W < 760 ? 0.30 : 0.50) - A * 0.25;
    var xBeira = beirada - A * 0.66;

    var x, yy, rot = 0, camX = 0, camY = 0, pf = 0, pt = 0, pose;

    var andar = faixa(p, 0.06, 0.42);
    var salto = faixa(p, 0.42, 0.80);
    var nado = faixa(p, 0.80, 1);

    if (salto === 0) {
      // Fase 1: anda até a beirada; o cenário passa por trás
      var t = suave(andar);
      x = lerp(x0, xBeira, t);
      yy = emPe - (andar > 0 && andar < 1 ? Math.abs(Math.sin(p * 140)) * 6 : 0);
      var telaX = lerp(x0, W * 0.80 - A * 0.66, t);
      camX = Math.max(0, x - telaX);
      if (andar > 0 && andar < 1) { pf = Math.sin(p * 140) * 24; pt = -pf; }
      pose = andar > 0 ? "andar" : cenas[atual].pose;
    } else {
      // Fase 2: salta da beirada e cai na água; a câmera desce junto
      var s = salto;
      x = xBeira + W * 0.30 * (1 - Math.pow(1 - s, 2));
      if (s < 0.3) yy = emPe - 0.16 * H * Math.sin((s / 0.3) * Math.PI / 2);
      else yy = emPe - 0.16 * H + Math.pow((s - 0.3) / 0.7, 1.6) * (superficie - emPe + 0.16 * H + 0.75 * H);
      rot = 85 * suave(faixa(s, 0.15, 0.55));
      pf = -40; pt = 40;
      var telaX2 = lerp(W * 0.80 - A * 0.66, W * 0.72 - A * 0.5, s);
      camX = x - telaX2;
      camY = Math.max(0, yy - 0.40 * H);
      pose = s > 0.62 ? "nadar" : "pular";
      if (nado > 0) {
        // Fase 3: nada para baixo pelo canto direito
        yy += nado * 0.45 * H;
        camY = Math.max(0, yy - 0.40 * H);
        rot = 85 - 15 * nado + Math.sin(p * 90) * 4;
        pf = -40 + Math.sin(p * 120) * 25; pt = -pf;
        pose = "nadar";
      }
    }

    // Aplica posições
    mundo.style.transform = "translate(" + (-camX) + "px," + (-camY) + "px)";
    decor.style.transform = "translate(" + (-camX * 0.12) + "px," + (-camY * 0.5) + "px)";
    ator.style.transform = "translate(" + (x - camX) + "px," + (yy - camY) + "px) rotate(" + rot + "deg)";
    ator.style.setProperty("--pf", pf + "deg");
    ator.style.setProperty("--pt", pt + "deg");
    if (ator.dataset.pose !== pose) ator.dataset.pose = pose;

    // Respingo ao tocar a água
    var centroY = yy + AH * 0.55;
    var perto = 1 - clamp(Math.abs(centroY - superficie) / (0.14 * H), 0, 1);
    respingo.style.left = (x + A * 0.55) + "px";
    respingo.style.opacity = salto > 0.3 ? perto : 0;
    respingo.style.transform = "scale(" + (0.6 + perto) + ")";

    // Fica submerso e aparece a frase
    var sub = clamp((camY - (superficie - 0.55 * H)) / (0.45 * H), 0, 1);
    submerso.style.opacity = sub;
    body.classList.toggle("no-mar", sub > 0.5);
    var f = suave(faixa(p, 0.80, 0.88));
    frase.style.opacity = f;
    frase.style.transform = "translateY(" + ((1 - f) * 40 - nado * 60) + "px)";

    // Texto do hero some ao começar a rolar
    var h = 1 - faixa(p, 0.02, 0.08);
    hero.style.opacity = h;
    hero.style.visibility = h < 0.02 ? "hidden" : "visible";

    // Nadador do "Saiba mais"
    var onda = Math.sin(y / 140);
    nadador.style.transform = "translateY(" + (onda * 18) + "px) rotate(" + (72 + onda * 5) + "deg)";
    nadador.style.setProperty("--pf", (-40 + Math.sin(y / 60) * 25) + "deg");
    nadador.style.setProperty("--pt", (40 - Math.sin(y / 60) * 25) + "deg");
  }

  var pedido = false;
  function agendar() { if (!pedido) { pedido = true; requestAnimationFrame(function () { pedido = false; quadro(); }); } }

  if (reduzir) {
    // Versão estática: sem história no scroll
    document.documentElement.classList.add("estatico");
    medir();
    var chao = 0.748 * innerHeight;
    ator.style.transform = "translate(" + (innerWidth * 0.5) + "px," + (chao - ator.offsetWidth * 260 / 340 * 0.79) + "px)";
    nadador.style.transform = "rotate(72deg)";
  } else {
    medir(); quadro();
    addEventListener("scroll", agendar, { passive: true });
    addEventListener("resize", function () { medir(); agendar(); });
  }

  // ---------- Janela de entrar/cadastrar ----------
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
        if (cadastro) { a.dataset.href = a.dataset.href || a.getAttribute("href"); a.removeAttribute("href"); }
        else if (a.dataset.href) { a.setAttribute("href", a.dataset.href); }
      });
      janela.showModal();
    });
  });
})();

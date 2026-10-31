// Tela de entrada do NextLearn (deserto): o Next troca de cor e de pose; com o scroll ele anda até a
// beirada, salta no lago, a tela fica submersa e o "Saiba mais" desce com ele nadando à direita.
(function () {
  var body = document.body;
  var cenas = JSON.parse(document.getElementById("dados-cenas").textContent);
  var historia = document.querySelector(".historia");
  var mundo = document.querySelector(".mundo");
  var decor = document.querySelector(".decor");
  var sol = document.querySelector(".sol");
  var ator = document.querySelector(".ator");
  var hero = document.querySelector(".hero");
  var submerso = document.querySelector(".submerso");
  var frase = document.querySelector(".frase-mar");
  var respingo = document.querySelector(".respingo");
  var nadador = document.querySelector(".nadador");
  var mosca = document.querySelector("[data-mosca]");
  var lingua = document.querySelector("[data-lingua]");
  var fala = document.querySelector("[data-fala]");
  var pontos = document.querySelectorAll("[data-ir]");
  var botaoPausa = document.querySelector("[data-pausa]");
  var reduzir = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---------- Hero: cor + pose + fala ----------
  var atual = 0, timer = null, pausado = reduzir, progresso = 0;
  function mostrar(i) {
    atual = (i + cenas.length) % cenas.length;
    body.dataset.cor = cenas[atual].id;
    if (progresso < 0.03) ator.dataset.pose = cenas[atual].pose;
    fala.textContent = cenas[atual].fala;
    pontos.forEach(function (p, j) { if (j === atual) p.setAttribute("aria-current", "true"); else p.removeAttribute("aria-current"); });
  }
  function tocar() { clearInterval(timer); if (!pausado) timer = setInterval(function () { if (progresso < 0.02) mostrar(atual + 1); }, 5000); }
  function rotuloPausa() { botaoPausa.textContent = pausado ? "Continuar" : "Pausar"; botaoPausa.setAttribute("aria-pressed", pausado ? "true" : "false"); }
  pontos.forEach(function (p) { p.addEventListener("click", function () { mostrar(Number(p.dataset.ir)); tocar(); }); });
  botaoPausa.addEventListener("click", function () { pausado = !pausado; rotuloPausa(); tocar(); });
  rotuloPausa(); tocar();

  // ---------- Utilidades ----------
  function clamp(v, a, b) { return Math.min(b, Math.max(a, v)); }
  function faixa(p, a, b) { return clamp((p - a) / (b - a), 0, 1); }
  function suave(t) { return t * t * (3 - 2 * t); }
  function lerp(a, b, t) { return a + (b - a) * t; }

  var W, H, A, AH;
  function medir() { W = innerWidth; H = innerHeight; A = ator.offsetWidth; AH = A * 260 / 340; }

  // ---------- Cena guiada pelo scroll ----------
  function cena(y) {
    var total = historia.offsetHeight - H;
    var p = clamp((y - historia.offsetTop) / total, 0, 1);
    progresso = p;
    var chaoTopo = 0.748 * H, beirada = 1.14 * W, superficie = 0.90 * H;
    var emPe = chaoTopo - AH * 0.79;
    var x0 = W * (W < 760 ? 0.30 : 0.52) - A * 0.25;
    var xBeira = beirada - A * 0.66;
    var andar = faixa(p, 0.04, 0.22), salto = faixa(p, 0.22, 0.52), nado = faixa(p, 0.52, 1);
    var x, yy, rot = 0, camX = 0, camY = 0, pf = 0, pt = 0, pose;

    if (salto === 0) {
      var t = suave(andar);
      x = lerp(x0, xBeira, t);
      yy = emPe - (andar > 0 && andar < 1 ? Math.abs(Math.sin(p * 220)) * 6 : 0);
      camX = Math.max(0, x - lerp(x0, W * 0.80 - A * 0.66, t));
      if (andar > 0 && andar < 1) { pf = Math.sin(p * 220) * 24; pt = -pf; }
      pose = andar > 0 ? "andar" : cenas[atual].pose;
    } else {
      var s = salto;
      x = xBeira + W * 0.24 * (1 - Math.pow(1 - s, 2));
      if (s < 0.3) yy = emPe - 0.16 * H * Math.sin((s / 0.3) * Math.PI / 2);
      else yy = emPe - 0.16 * H + Math.pow((s - 0.3) / 0.7, 1.5) * (superficie - emPe + 0.16 * H + 0.7 * H);
      rot = 85 * suave(faixa(s, 0.15, 0.55));
      pf = -40; pt = 40;
      camX = x - lerp(W * 0.80 - A * 0.66, W * 0.72 - A * 0.5, s);
      camY = Math.max(0, yy - 0.40 * H);
      pose = s > 0.6 ? "nadar" : "pular";
      if (nado > 0) {
        yy += nado * 0.45 * H;
        camY = Math.max(0, yy - 0.40 * H);
        rot = 85 - 15 * nado + Math.sin(p * 90) * 4;
        pf = -40 + Math.sin(p * 120) * 25; pt = -pf;
        pose = "nadar";
      }
    }
    mundo.style.transform = "translate(" + (-camX) + "px," + (-camY) + "px)";
    decor.style.transform = "translate(" + (-camX * 0.15) + "px," + (-camY * 0.5) + "px)";
    // Sol desce devagar (pôr do sol) enquanto ele anda e salta; fica mais alaranjado perto do horizonte
    var desce = faixa(p, 0, 0.5);
    sol.style.transform = "translateY(" + (desce * 0.42 * H) + "px)";
    sol.style.background = "rgb(242," + Math.round(lerp(181, 128, desce)) + "," + Math.round(lerp(68, 50, desce)) + ")";
    ator.style.transform = "translate(" + (x - camX) + "px," + (yy - camY) + "px) rotate(" + rot + "deg)";
    ator.style.setProperty("--pf", pf + "deg"); ator.style.setProperty("--pt", pt + "deg");
    if (ator.dataset.pose !== pose) ator.dataset.pose = pose;

    var perto = 1 - clamp(Math.abs(yy + AH * 0.55 - superficie) / (0.14 * H), 0, 1);
    respingo.style.left = (x + A * 0.55) + "px";
    respingo.style.opacity = salto > 0.3 ? perto : 0;
    respingo.style.transform = "scale(" + (0.6 + perto) + ")";

    var sub = clamp((camY - (superficie - 0.55 * H)) / (0.4 * H), 0, 1);
    submerso.style.opacity = sub;
    body.classList.toggle("no-mar", sub > 0.5 || y > historia.offsetTop + total);
    var f = suave(faixa(p, 0.50, 0.60));
    frase.style.opacity = f;
    frase.style.transform = "translateY(" + ((1 - f) * 40 - nado * 60) + "px)";
    var h = 1 - faixa(p, 0.02, 0.07);
    hero.style.opacity = h; hero.style.visibility = h < 0.02 ? "hidden" : "visible";
  }

  // ---------- Nadador + língua que pega a mosca ----------
  function saiba(y) {
    var onda = Math.sin(y / 140);
    var ang = 72 + onda * 5;
    nadador.style.transform = "translateY(" + (onda * 18) + "px) rotate(" + ang + "deg)";
    nadador.style.setProperty("--pf", (-40 + Math.sin(y / 60) * 25) + "deg");
    nadador.style.setProperty("--pt", (40 - Math.sin(y / 60) * 25) + "deg");
    if (W < 760) return;

    if (pegouMosca) return;
    var rM = mosca.getBoundingClientRect();
    if (rM.top + rM.height / 2 < H * 0.55 && rM.bottom > 0) disparaLingua();   // passou do ponto: pega uma vez
  }

  // A língua roda uma única vez, por tempo (não acompanha o scroll). Voltar a rolar não devolve a mosca.
  var pegouMosca = false;
  function disparaLingua() {
    pegouMosca = true;
    var inicio = performance.now(), duracao = 750;
    function passo(agora) {
      var t = Math.min(1, (agora - inicio) / duracao);
      var ang = 72 + Math.sin(scrollY / 140) * 5;
      var rN = nadador.getBoundingClientRect(), rM = mosca.getBoundingClientRect();
      // Boca do Next: centro do nadador + vetor da boca girado (ponto 265,135 do desenho de 340x260)
      var k = nadador.offsetWidth / 340, a = ang * Math.PI / 180;
      var vx = 95 * k, vy = 5 * k;
      var bx = rN.left + rN.width / 2 + vx * Math.cos(a) - vy * Math.sin(a);
      var by = rN.top + rN.height / 2 + vx * Math.sin(a) + vy * Math.cos(a);
      var mx = rM.left + rM.width / 2, my = rM.top + rM.height / 2;
      var dist = Math.hypot(mx - bx, my - by);
      var estica = t < 0.45 ? suave(t / 0.45) : 1 - suave((t - 0.45) / 0.55);   // vai e volta
      var pegou = t >= 0.45;
      lingua.style.display = "block";
      lingua.style.left = bx + "px"; lingua.style.top = (by - 6) + "px";
      lingua.style.width = (dist * estica) + "px";
      lingua.style.transform = "rotate(" + Math.atan2(my - by, mx - bx) + "rad)";
      lingua.classList.toggle("pegou", pegou);
      if (pegou) mosca.style.visibility = "hidden";
      if (t < 1) requestAnimationFrame(passo); else lingua.style.display = "none";
    }
    requestAnimationFrame(passo);
  }

  function quadro() { var y = scrollY; cena(y); saiba(y); }
  var pedido = false;
  function agendar() { if (!pedido) { pedido = true; requestAnimationFrame(function () { pedido = false; quadro(); }); } }

  // Revelar blocos do "Saiba mais"
  var blocos = document.querySelectorAll(".revelar");
  if ("IntersectionObserver" in window && !reduzir) {
    var obs = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) e.target.classList.add("visivel"); }); }, { threshold: 0.25 });
    blocos.forEach(function (b) { obs.observe(b); });
  } else { blocos.forEach(function (b) { b.classList.add("visivel"); }); }

  if (reduzir) {
    document.documentElement.classList.add("estatico");
    medir();
    ator.style.transform = "translate(" + (innerWidth * 0.52 - A * 0.25) + "px," + (0.748 * innerHeight - AH * 0.79) + "px)";
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

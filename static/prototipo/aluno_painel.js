// Painel do aluno (protótipo): preferências, painéis interativos (notas, tempo, tarefas) e calendário em "zoom".
(function () {
  var b = document.body;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function ler(k) { try { return localStorage.getItem("nl-" + k); } catch (e) { return null; } }
  function gravar(k, v) { try { localStorage.setItem("nl-" + k, v); } catch (e) {} }
  function el(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; }

  // Dentro da tela de comparação (iframe), esconde o painel do desenvolvedor
  if (window.self !== window.top) { var dv = document.querySelector('.dev'); if (dv) dv.hidden = true; }

  // ---------- Preferências (só para o aluno, na hora) ----------
  var classes = { letras: "letras-espacadas", voz: "com-voz", limpo: "modo-limpo", movimento: "com-movimento" };
  $$("[data-pref]").forEach(function (bt) {
    var k = bt.dataset.pref, salvo = b.dataset.perfilDev ? null : ler(k);   // simulação do dev ignora o que ficou salvo
    var ligado = salvo === null ? bt.getAttribute("aria-pressed") === "true" : salvo === "1";
    function aplicar() { bt.setAttribute("aria-pressed", ligado ? "true" : "false"); b.classList.toggle(classes[k], ligado); }
    aplicar();
    bt.addEventListener("click", function () { ligado = !ligado; gravar(k, ligado ? "1" : "0"); aplicar(); });
  });
  if (!$("[data-pref='movimento']")) { var mv = ler("movimento"); if (mv === "1" || (mv === null && b.dataset.padraoMovimento === "1")) b.classList.add("com-movimento"); }
  function podeAnimar() { return b.classList.contains("com-movimento") && !matchMedia("(prefers-reduced-motion: reduce)").matches; }

  var msg = $("[data-humor-msg]");
  $$("[data-humor]").forEach(function (bt) {
    bt.addEventListener("click", function () {
      $$("[data-humor]").forEach(function (o) { o.setAttribute("aria-pressed", o === bt ? "true" : "false"); });
      msg.textContent = bt.dataset.humor === "dificil" ? "Obrigado por contar. Amanhã a gente vai com calma." : "Obrigado por contar!";
    });
  });

  // Fala do Next (IA no servidor, com reserva). Só o texto vem para o navegador.
  var falaEl = $("[data-fala-next]");
  if (falaEl) {
    fetch("/prototipo/aluno/fala/?perfil_dev=" + encodeURIComponent(b.dataset.perfilDev || "") + "&ambiente=" + encodeURIComponent(b.dataset.ambienteDev || ""), { credentials: "same-origin" })
      .then(function (r) { return r.json(); })
      .then(function (d) { if (d.fala) falaEl.textContent = d.fala; var o = $("[data-origem-fala]"); if (o) o.textContent = "fala: " + d.origem; })
      .catch(function () {});
  }

  // Mapa com 560 px de largura: encolhe para caber em telas menores
  function escalarMapas() {
    $$("[data-mapa]").forEach(function (caixa) {
      var m = $(".mapa", caixa); if (!m) return;
      var w = parseFloat(m.style.width), h = parseFloat(m.style.height), k = Math.min(1, caixa.clientWidth / w);
      m.style.transform = "scale(" + k + ")"; caixa.style.height = (h * k) + "px";
      m.style.marginLeft = Math.max(0, (caixa.clientWidth - w * k) / 2) + "px";
    });
  }
  escalarMapas(); addEventListener("resize", escalarMapas);
  $$("details.unidade").forEach(function (d) { d.addEventListener("toggle", escalarMapas); });

  // ---------- Botões "Ouvir" em cada bloco (modo leitura ou preferência de ouvir) ----------
  if ("speechSynthesis" in window && (b.dataset.modo === "leitura" || b.classList.contains("com-voz"))) {
    var alvos = $$(".missao-texto h1, .lado .bloco > header h2, .lado .bloco > h2");
    alvos.forEach(function (h) {
      var bt = el("button", "btn-ouvir", "🔊 Ouvir"); bt.type = "button";
      bt.setAttribute("aria-label", "Ouvir: " + h.textContent.trim());
      bt.addEventListener("click", function () {
        if (speechSynthesis.speaking) { speechSynthesis.cancel(); bt.textContent = "🔊 Ouvir"; return; }
        var bloco = h.closest(".bloco, .missao-texto");
        var texto = (bloco ? bloco.innerText : h.textContent).replace(/🔊 Ouvir|■ Parar/g, "").slice(0, 600);
        var u = new SpeechSynthesisUtterance(texto); u.lang = "pt-BR"; u.rate = .95;
        u.onend = function () { bt.textContent = "🔊 Ouvir"; };
        speechSynthesis.speak(u); bt.textContent = "■ Parar";
      });
      h.appendChild(bt);
    });
  }

  // ---------- Chat com o Next ----------
  var chatBox = $("[data-chat]"), chatBt = $("[data-chat-abrir]");
  if (chatBox) {
    var msgs = $("[data-chat-msgs]"), form = $("[data-chat-form]"), campo = $("#chat-texto");
    function abrirChat(abrir) { chatBox.hidden = !abrir; chatBt.setAttribute("aria-expanded", abrir ? "true" : "false"); if (abrir) campo.focus(); }
    chatBt.addEventListener("click", function () { abrirChat(chatBox.hidden); });
    $("[data-chat-fechar]").addEventListener("click", function () { abrirChat(false); chatBt.focus(); });
    function falar(texto, quem) { var li = el("li", "msg " + quem, texto); msgs.appendChild(li); msgs.scrollTop = msgs.scrollHeight; return li; }
    function enviar(pergunta) {
      pergunta = pergunta.trim(); if (!pergunta) return;
      falar(pergunta, "eu"); campo.value = "";
      var pensando = falar("…", "next pensando");
      var url = "/prototipo/aluno/chat/" + (b.dataset.perfilDev ? "?perfil_dev=" + encodeURIComponent(b.dataset.perfilDev) : "");
      fetch(url, { method: "POST", credentials: "same-origin",
        headers: { "Content-Type": "application/json", "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value },
        body: JSON.stringify({ pergunta: pergunta }) })
        .then(function (r) { return r.json(); })
        .then(function (d) { pensando.className = "msg next"; pensando.textContent = d.resposta; pensando.dataset.origem = d.origem; })
        .catch(function () { pensando.className = "msg next"; pensando.textContent = "Não consegui responder agora. Tente de novo daqui a pouco."; });
    }
    form.addEventListener("submit", function (e) { e.preventDefault(); enviar(campo.value); });
    $$("[data-chat-sugestoes] button").forEach(function (bt) { bt.addEventListener("click", function () { enviar(bt.textContent); }); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !chatBox.hidden) abrirChat(false); });
  }

  var fonte = $("#dados-painel");
  if (!fonte) return;
  var D = JSON.parse(fonte.textContent);
  var MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
  var SEM = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"];
  function data(iso) { var p = iso.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function iso(d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }
  function curta(isoTxt) { var d = data(isoTxt); return d.getDate() + "/" + String(d.getMonth() + 1).padStart(2, "0"); }
  function segunda(d) { var x = new Date(d); x.setDate(x.getDate() - ((x.getDay() + 6) % 7)); return x; }
  var HOJE = data(D.hoje);

  // Abas genéricas (role=tab): chama fn(botão) ao trocar
  function abas(grupo, fn) {
    if (!grupo) return;
    var bts = $$("[role=tab]", grupo);
    bts.forEach(function (bt) {
      bt.addEventListener("click", function () { bts.forEach(function (o) { o.setAttribute("aria-selected", o === bt ? "true" : "false"); }); fn(bt); });
    });
  }

  // ---------- Notas em carrossel ----------
  var car = $("[data-carrossel]");
  if (car) {
    var trilho = $("[data-car-trilho]", car), pontos = $("[data-car-pontos]", car);
    var cartoesN = $$(".nota-cartao", trilho);
    function visiveis() { return cartoesN.filter(function (c) { return !c.hidden; }); }
    function passo() { var c = visiveis()[0]; return c ? c.getBoundingClientRect().width + 12 : 200; }
    function comportamento() { return podeAnimar() ? "smooth" : "auto"; }
    function atualizaPontos() {
      var v = visiveis(), porTela = Math.max(1, Math.round(trilho.clientWidth / passo()));
      var n = Math.max(1, Math.ceil(v.length / porTela)), atual = Math.round(trilho.scrollLeft / (passo() * porTela));
      pontos.innerHTML = "";
      for (var i = 0; i < n; i++) pontos.appendChild(el("i", i === Math.min(atual, n - 1) ? "ativo" : ""));
    }
    $("[data-car-ant]", car).addEventListener("click", function () { trilho.scrollBy({ left: -passo() * 2, behavior: comportamento() }); });
    $("[data-car-prox]", car).addEventListener("click", function () { trilho.scrollBy({ left: passo() * 2, behavior: comportamento() }); });
    trilho.addEventListener("scroll", function () { requestAnimationFrame(atualizaPontos); });
    trilho.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); trilho.scrollBy({ left: passo(), behavior: comportamento() }); }
      if (e.key === "ArrowLeft") { e.preventDefault(); trilho.scrollBy({ left: -passo(), behavior: comportamento() }); }
    });
    abas($("[data-filtro-notas]"), function (bt) {
      var m = bt.dataset.materia;
      cartoesN.forEach(function (c) { c.hidden = !!m && c.dataset.materia !== m; });
      trilho.scrollLeft = 0; atualizaPontos();
    });
    addEventListener("resize", atualizaPontos);
    atualizaPontos();
  }

  // ---------- Tempo ----------
  var gTempo = $("[data-grafico-tempo]");
  function desenharTempo(periodo) {
    gTempo.innerHTML = "";
    var itens = [], limite = D.limite, escala;
    if (periodo === "semana") {
      var s = segunda(HOJE);
      for (var i = 0; i < 7; i++) { var d = new Date(s); d.setDate(s.getDate() + i); itens.push({ rot: SEM[i], min: D.minutos[iso(d)] || 0, hoje: iso(d) === D.hoje }); }
      escala = Math.max(limite, Math.max.apply(null, itens.map(function (x) { return x.min; })));
      var linha = el("span", "limite"); linha.style.bottom = (28 + 120 * limite / escala) + "px"; linha.title = "Limite diário: " + limite + " min"; gTempo.appendChild(linha);
    } else {
      var s0 = segunda(HOJE);
      for (var w = 3; w >= 0; w--) {
        var ini = new Date(s0); ini.setDate(s0.getDate() - 7 * w); var tot = 0;
        for (var j = 0; j < 7; j++) { var dd = new Date(ini); dd.setDate(ini.getDate() + j); tot += D.minutos[iso(dd)] || 0; }
        itens.push({ rot: w === 0 ? "esta" : curta(iso(ini)), min: tot, hoje: w === 0 });
      }
      escala = Math.max(1, Math.max.apply(null, itens.map(function (x) { return x.min; })));
    }
    itens.forEach(function (x) {
      var col = el("div", "barra-col" + (x.hoje ? " ativa" : ""));
      col.appendChild(el("span", "bc-valor", x.min ? x.min + " min" : "–"));
      var barra = el("span", "bc-barra"); barra.style.height = Math.max(x.min ? 6 : 2, 120 * x.min / escala) + "px"; col.appendChild(barra);
      col.appendChild(el("span", "bc-rot", x.rot));
      gTempo.appendChild(col);
    });
    gTempo.setAttribute("aria-label", "Minutos de estudo: " + itens.map(function (x) { return x.rot + " " + x.min; }).join(", "));
  }
  if (gTempo) { desenharTempo("semana"); abas($("[data-filtro-tempo]"), function (bt) { desenharTempo(bt.dataset.periodo); }); }

  // ---------- Tarefas ----------
  var listaT = $("[data-lista-tarefas]"), botaoTodas = $("[data-mostrar-todas]"), listaAtual = "pendentes", todas = false;
  function prazoTxt(isoTxt) {
    var dias = Math.round((data(isoTxt) - HOJE) / 864e5);
    return dias < 0 ? "prazo passou" : dias === 0 ? "prazo hoje" : dias === 1 ? "prazo amanhã" : "prazo em " + dias + " dias (" + curta(isoTxt) + ")";
  }
  function desenharTarefas() {
    listaT.innerHTML = "";
    var itens = D[listaAtual], foco = b.classList.contains("apoio-foco");
    var mostra = (foco && listaAtual === "pendentes" && !todas) ? itens.slice(0, 1) : itens;
    mostra.forEach(function (t, k) {
      var li = el("li"), a = el("a"); a.href = t.url;
      var txt = el("span"); txt.appendChild(el("strong", null, t.titulo)); txt.appendChild(el("span", "suave", " · " + t.materia));
      a.appendChild(txt);
      a.appendChild(el("span", "selo" + (listaAtual === "pendentes" && k === 0 ? " selo-nova" : ""), listaAtual === "pendentes" ? prazoTxt(t.prazo) : t.detalhe));
      li.appendChild(a);
      var cal = el("button", "btn-icone"); cal.type = "button";
      cal.setAttribute("aria-label", "Ver " + t.titulo + " no calendário");
      cal.innerHTML = '<svg class="ico" aria-hidden="true"><use href="#i-calendario"/></svg>';
      cal.addEventListener("click", function () { abrirCalendario(cal, listaAtual === "pendentes" ? t.prazo : t.data); });
      li.appendChild(cal);
      listaT.appendChild(li);
    });
    if (botaoTodas) botaoTodas.hidden = !(foco && listaAtual === "pendentes" && itens.length > 1 && !todas);
  }
  if (listaT) {
    desenharTarefas();
    abas($("[data-filtro-tarefas]"), function (bt) { listaAtual = bt.dataset.lista; desenharTarefas(); });
    if (botaoTodas) botaoTodas.addEventListener("click", function () { todas = true; desenharTarefas(); });
  }

  // ---------- Calendário (zoom a partir de quem abriu) ----------
  var dlg = $("[data-calendario]"), caixa = $(".cal-caixa"), grade = $("[data-cal-grade]");
  var mesVisto = new Date(HOJE.getFullYear(), HOJE.getMonth(), 1), selecionado = D.hoje, origem = null;
  var porDia = {};
  D.eventos.forEach(function (e) { (porDia[e.data] = porDia[e.data] || []).push(e); });

  function semanaComMeta(seg) {
    var n = 0;
    for (var i = 0; i < 7; i++) { var d = new Date(seg); d.setDate(seg.getDate() + i); n += (porDia[iso(d)] || []).filter(function (e) { return e.tipo === "feita"; }).length; }
    return n >= D.meta;
  }
  function desenharMes() {
    var nomeMes = MESES[mesVisto.getMonth()];
    $("[data-cal-titulo]").textContent = nomeMes.charAt(0).toUpperCase() + nomeMes.slice(1) + " de " + mesVisto.getFullYear();
    grade.innerHTML = "";
    var cab = el("div", "cal-linha cal-cab"); cab.setAttribute("role", "row");
    SEM.concat(["meta"]).forEach(function (s) { var c = el("span", "cal-cab-dia", s); c.setAttribute("role", "columnheader"); cab.appendChild(c); });
    grade.appendChild(cab);
    var d = segunda(mesVisto);
    while (d.getMonth() === mesVisto.getMonth() || d < mesVisto) {
      var linha = el("div", "cal-linha"); linha.setAttribute("role", "row");
      var seg = new Date(d);
      for (var i = 0; i < 7; i++) {
        var k = iso(d), evs = porDia[k] || [], fora = d.getMonth() !== mesVisto.getMonth();
        var bt = el("button", "cal-dia-bt" + (fora ? " fora" : "") + (k === D.hoje ? " hoje" : "") + (k === selecionado ? " sel" : ""));
        bt.type = "button"; bt.dataset.dia = k; bt.setAttribute("role", "gridcell");
        bt.appendChild(el("span", "cal-num", String(d.getDate())));
        var marcas = el("span", "cal-marcas");
        var feitas = evs.filter(function (e) { return e.tipo === "feita"; }).length, prazos = evs.filter(function (e) { return e.tipo === "prazo"; }).length;
        if (feitas) marcas.appendChild(el("span", "leg leg-feita", "✓"));
        if (prazos) marcas.appendChild(el("span", "leg leg-prazo"));
        if (D.minutos[k]) marcas.appendChild(el("span", "leg leg-estudo"));
        bt.appendChild(marcas);
        var desc = d.getDate() + " de " + MESES[d.getMonth()] + (k === D.hoje ? ", hoje" : "") +
          (feitas ? ", " + feitas + " aula feita" : "") + (prazos ? ", " + prazos + " prazo" + (prazos > 1 ? "s" : "") : "") +
          (D.minutos[k] ? ", " + D.minutos[k] + " minutos de estudo" : "");
        bt.setAttribute("aria-label", desc);
        bt.addEventListener("click", function () { selecionado = this.dataset.dia; desenharMes(); mostrarDia(); var f = grade.querySelector("[data-dia='" + selecionado + "']"); if (f) f.focus(); });
        linha.appendChild(bt);
        d.setDate(d.getDate() + 1);
      }
      var meta = el("span", "cal-meta", seg <= HOJE && semanaComMeta(seg) ? "✓" : "");
      meta.setAttribute("role", "gridcell");
      if (meta.textContent) meta.setAttribute("aria-label", "Meta da semana cumprida");
      linha.appendChild(meta);
      grade.appendChild(linha);
      if (d.getMonth() !== mesVisto.getMonth() && d > mesVisto) break;
    }
  }
  function mostrarDia() {
    var d = data(selecionado), evs = porDia[selecionado] || [];
    $("[data-cal-dia-titulo]").textContent = (selecionado === D.hoje ? "Hoje, " : "") + d.getDate() + " de " + MESES[d.getMonth()];
    var ul = $("[data-cal-eventos]"); ul.innerHTML = "";
    if (D.minutos[selecionado]) ul.appendChild(el("li", "ev-estudo", "Estudou " + D.minutos[selecionado] + " min"));
    evs.forEach(function (e) {
      var li = el("li", "ev-" + e.tipo), a = el("a"); a.href = e.url;
      a.appendChild(el("span", "ev-tipo", e.tipo === "feita" ? "✓ Aula feita" : "Prazo"));
      a.appendChild(el("strong", null, e.titulo));
      a.appendChild(el("span", "suave", e.materia + (e.tipo === "feita" ? " · " + e.detalhe : "")));
      li.appendChild(a); ul.appendChild(li);
    });
    if (!ul.children.length) ul.appendChild(el("li", "suave", "Nada marcado neste dia."));
    // Próximos prazos (a partir do dia escolhido), para o aluno se planejar
    var prox = D.eventos.filter(function (e) { return e.tipo === "prazo" && e.data >= selecionado; })
      .sort(function (a, c) { return a.data < c.data ? -1 : 1; }).slice(0, 3);
    var box = $("[data-cal-proximos]"); box.innerHTML = "";
    $("[data-cal-proximos-titulo]").hidden = !prox.length;
    prox.forEach(function (e) {
      var li = el("li"), bt = el("button", "prox-bt"); bt.type = "button";
      bt.appendChild(el("span", "prox-data", curta(e.data)));
      bt.appendChild(el("span", null, e.titulo));
      bt.addEventListener("click", function () { selecionado = e.data; var d2 = data(e.data); mesVisto = new Date(d2.getFullYear(), d2.getMonth(), 1); desenharMes(); mostrarDia(); });
      li.appendChild(bt); box.appendChild(li);
    });
  }
  function zoom(de, abrindo) {
    if (!de || !podeAnimar() || !caixa.animate) return null;
    var r0 = de.getBoundingClientRect(), r1 = caixa.getBoundingClientRect();
    var t = "translate(" + (r0.left + r0.width / 2 - (r1.left + r1.width / 2)) + "px," + (r0.top + r0.height / 2 - (r1.top + r1.height / 2)) + "px) scale(" + Math.max(0.05, r0.width / r1.width) + "," + Math.max(0.05, r0.height / r1.height) + ")";
    var quadros = [{ transform: t, opacity: 0.2 }, { transform: "none", opacity: 1 }];
    return caixa.animate(abrindo ? quadros : quadros.reverse(), { duration: 380, easing: "cubic-bezier(.2,.8,.2,1)" });
  }
  function abrirCalendario(de, dia) {
    origem = de || $("[data-dia-hoje]");
    selecionado = dia || D.hoje;
    var d = data(selecionado); mesVisto = new Date(d.getFullYear(), d.getMonth(), 1);
    desenharMes(); mostrarDia();
    dlg.showModal();
    zoom(origem, true);
    var f = grade.querySelector("[data-dia='" + selecionado + "']"); if (f) f.focus();
  }
  function fecharCalendario() {
    var anim = zoom(origem, false);
    if (anim) anim.onfinish = function () { dlg.close(); }; else dlg.close();
  }
  window.abrirCalendario = abrirCalendario;
  $$("[data-abrir-calendario]").forEach(function (bt) { bt.addEventListener("click", function () { abrirCalendario(bt); }); });
  $("[data-cal-fechar]").addEventListener("click", fecharCalendario);
  dlg.addEventListener("cancel", function (e) { e.preventDefault(); fecharCalendario(); });
  dlg.addEventListener("click", function (e) { if (e.target === dlg) fecharCalendario(); });
  $("[data-cal-anterior]").addEventListener("click", function () { mesVisto.setMonth(mesVisto.getMonth() - 1); desenharMes(); });
  $("[data-cal-proximo]").addEventListener("click", function () { mesVisto.setMonth(mesVisto.getMonth() + 1); desenharMes(); });
  grade.addEventListener("keydown", function (e) {
    var passo = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -7, ArrowDown: 7 }[e.key];
    if (!passo) return;
    e.preventDefault();
    var d = data(selecionado); d.setDate(d.getDate() + passo); selecionado = iso(d);
    if (d.getMonth() !== mesVisto.getMonth()) mesVisto = new Date(d.getFullYear(), d.getMonth(), 1);
    desenharMes(); mostrarDia(); var f = grade.querySelector("[data-dia='" + selecionado + "']"); if (f) f.focus();
  });
  if (location.hash === "#calendario") abrirCalendario(null);
})();

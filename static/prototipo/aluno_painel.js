// Painel do aluno (protótipo): preferências, painéis interativos (notas, tempo, tarefas) e calendário em "zoom".
(function () {
  var b = document.body;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function ler(k) { try { return localStorage.getItem("nl-" + k); } catch (e) { return null; } }
  function gravar(k, v) { try { localStorage.setItem("nl-" + k, v); } catch (e) {} }
  function el(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; }

  // ---------- Preferências (só para o aluno, na hora) ----------
  var classes = { letras: "letras-espacadas", voz: "com-voz", limpo: "modo-limpo", movimento: "com-movimento" };
  $$("[data-pref]").forEach(function (bt) {
    var k = bt.dataset.pref, salvo = ler(k);
    var ligado = salvo === null ? bt.getAttribute("aria-pressed") === "true" : salvo === "1";
    function aplicar() { bt.setAttribute("aria-pressed", ligado ? "true" : "false"); b.classList.toggle(classes[k], ligado); }
    aplicar();
    bt.addEventListener("click", function () { ligado = !ligado; gravar(k, ligado ? "1" : "0"); aplicar(); });
  });
  if (!$("[data-pref='movimento']") && ler("movimento") === "1") b.classList.add("com-movimento");
  function podeAnimar() { return b.classList.contains("com-movimento") && !matchMedia("(prefers-reduced-motion: reduce)").matches; }

  var msg = $("[data-humor-msg]");
  $$("[data-humor]").forEach(function (bt) {
    bt.addEventListener("click", function () {
      $$("[data-humor]").forEach(function (o) { o.setAttribute("aria-pressed", o === bt ? "true" : "false"); });
      msg.textContent = bt.dataset.humor === "dificil" ? "Obrigado por contar. Amanhã a gente vai com calma." : "Obrigado por contar!";
    });
  });

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

  // ---------- Notas ----------
  var gNotas = $("[data-grafico-notas]"), detalhe = $("[data-detalhe-nota]");
  function desenharNotas(materia) {
    var lista = D.notas.filter(function (n) { return !materia || n.materia === materia; }).slice(-8);
    gNotas.innerHTML = "";
    lista.forEach(function (n) {
      var col = el("button", "barra-col");
      col.type = "button";
      col.setAttribute("aria-label", n.assunto + ", " + n.materia + ", nota " + n.nota + " em " + curta(n.data));
      col.appendChild(el("span", "bc-valor", String(n.nota).replace(".", ",")));
      var barra = el("span", "bc-barra"); barra.style.height = Math.max(6, n.nota * 12) + "px"; col.appendChild(barra);
      col.appendChild(el("span", "bc-rot", curta(n.data)));
      col.addEventListener("click", function () {
        $$(".barra-col", gNotas).forEach(function (o) { o.classList.toggle("ativa", o === col); });
        detalhe.textContent = n.assunto + " (" + n.materia + ") · nota " + String(n.nota).replace(".", ",") + " · " + curta(n.data);
      });
      gNotas.appendChild(col);
    });
    gNotas.setAttribute("aria-label", "Notas: " + lista.map(function (n) { return n.assunto + " " + n.nota; }).join(", "));
    var todas = D.notas.filter(function (n) { return !materia || n.materia === materia; });
    var media = todas.reduce(function (s, n) { return s + n.nota; }, 0) / (todas.length || 1);
    $("[data-media-filtro]").textContent = todas.length ? media.toFixed(1).replace(".", ",") : "–";
    var dom = todas.filter(function (n) { return n.nota >= 10; }).length, rev = todas.filter(function (n) { return n.nota < 6; }).length;
    $("[data-texto-filtro]").textContent = dom + " assunto" + (dom === 1 ? "" : "s") + " dominado" + (dom === 1 ? "" : "s") + " · " + rev + " para revisar";
    detalhe.textContent = "Toque numa barra para ver a aula.";
  }
  if (gNotas) { desenharNotas(""); abas($("[data-filtro-notas]"), function (bt) { desenharNotas(bt.dataset.materia); }); }

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
      cal.innerHTML = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>';
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

// Família: gráfico interativo de notas (filtro por matéria, detalhe ao passar o mouse/tocar) e checklist do ambiente de estudo.
(function () {
  var el = document.querySelector("[data-grafico]"), fonte = document.getElementById("dados-grafico");
  if (el && fonte) {
    var dados = JSON.parse(fonte.textContent), det = document.querySelector("[data-detalhe]"), filtro = "";
    function cor(n) { return n >= 8 ? "#1E8A5A" : n >= 6 ? "#2B59C3" : n >= 4 ? "#B8860B" : "#B3412E"; }
    function desenha() {
      el.innerHTML = "";
      dados.forEach(function (d) {
        var b = document.createElement("button");
        b.type = "button"; b.className = "barra-nota" + (filtro && d.materia !== filtro ? " apagada" : "");
        b.style.setProperty("--h", Math.max(4, d.nota * 10) + "%"); b.style.setProperty("--c", cor(d.nota));
        b.setAttribute("aria-label", d.quando + ", " + d.materia + ", " + d.assunto + ": nota " + d.nota);
        b.innerHTML = '<span class="bn-val">' + d.nota + '</span><span class="bn-barra"></span><span class="bn-data">' + d.quando + "</span>";
        function mostra() { det.textContent = d.quando + " · " + d.materia + " · " + d.assunto + " — nota " + d.nota + (d.nota >= 6 ? " ✓" : " (vale revisar junto)"); }
        b.addEventListener("mouseenter", mostra); b.addEventListener("focus", mostra); b.addEventListener("click", mostra);
        el.appendChild(b);
      });
    }
    document.querySelectorAll("[data-mat]").forEach(function (bt) {
      bt.addEventListener("click", function () {
        filtro = bt.dataset.mat;
        document.querySelectorAll("[data-mat]").forEach(function (x) { x.classList.toggle("ativo", x === bt); x.setAttribute("aria-pressed", x === bt); });
        desenha();
      });
    });
    desenha();
  }
  var lista = document.querySelector("[data-checklist]");
  if (lista) {
    var chave = "chamaleon-" + lista.dataset.checklist, caixas = lista.querySelectorAll("input"), salvo = [];
    try { salvo = JSON.parse(localStorage.getItem(chave) || "[]"); } catch (e) { salvo = []; }
    function total() {
      var n = 0; caixas.forEach(function (c) { if (c.checked) n++; });
      var t = document.querySelector("[data-check-total]"); if (t) t.textContent = n + " de " + caixas.length + " já fazem parte da rotina.";
    }
    caixas.forEach(function (c, i) {
      c.checked = salvo.indexOf(i) >= 0;
      c.addEventListener("change", function () {
        var marc = []; caixas.forEach(function (x, j) { if (x.checked) marc.push(j); });
        try { localStorage.setItem(chave, JSON.stringify(marc)); } catch (e) {}
        total();
      });
    });
    total();
  }
})();

// Brilho que segue o mouse em cartões e botões. Desligado no modo agenda (TEA), no modo limpo e com "reduzir movimento".
(function () {
  var b = document.body;
  if (b.classList.contains("modo-agenda") || b.classList.contains("modo-limpo") || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var sel = ".cartao, .cartao-pg, .kpi, .numero, .nota-cartao, .treino, .btn-contorno, .btn-missao, .btn-principal, .no-bt, .dia-grande, .tarefas li > a, .abas [role=tab], .interruptor, .chat-abrir, .unidade-faixa";
  document.addEventListener("pointermove", function (e) {
    var alvo = e.target.closest && e.target.closest(sel);
    if (!alvo) return;
    var r = alvo.getBoundingClientRect();
    alvo.style.setProperty("--mx", (e.clientX - r.left) + "px");
    alvo.style.setProperty("--my", (e.clientY - r.top) + "px");
    alvo.classList.add("brilhando");
  });
  document.addEventListener("pointerout", function (e) {
    var alvo = e.target.closest && e.target.closest(sel);
    if (alvo && !alvo.contains(e.relatedTarget)) alvo.classList.remove("brilhando");
  });
})();

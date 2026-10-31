// Ao vivo (só no computador de desenvolvimento): recarrega a página quando um arquivo do protótipo muda.
// Em produção o endereço /prototipo/_versao/ não existe (404) e o script para sozinho.
(function () {
  var url = "/prototipo/_versao/", ultima = null, caiu = false;
  function checar() {
    fetch(url, { cache: "no-store" }).then(function (r) {
      if (r.status === 404) return null;            // produção: desliga
      return r.json();
    }).then(function (d) {
      if (!d) return;
      if (caiu || (ultima !== null && d.v !== ultima)) { location.reload(); return; }
      ultima = d.v; setTimeout(checar, 1200);
    }).catch(function () { caiu = true; setTimeout(checar, 1500); });   // servidor reiniciando
  }
  checar();
})();

// Barra de apoios de leitura do aluno: liga e desliga sem recarregar a página,
// para não perder respostas já marcadas. Se o JavaScript falhar, o formulário funciona sozinho.
document.querySelectorAll("form[data-preferencia]").forEach(function (form) {
  form.addEventListener("submit", function (evento) {
    evento.preventDefault();
    fetch(form.action, {
      method: "POST",
      body: new FormData(form),
      headers: { "X-Requested-With": "fetch" },
    })
      .then(function (resposta) {
        if (!resposta.ok) throw new Error("HTTP " + resposta.status);
        return resposta.json();
      })
      .then(function (dados) {
        document.body.classList.toggle(dados.campo.replace(/_/g, "-"), dados.valor);
        form.querySelector("button").setAttribute("aria-pressed", dados.valor ? "true" : "false");
        form.querySelector("input[name=valor]").value = dados.valor ? "0" : "1";
        if (dados.campo === "leitura_voz" && !dados.valor && window.speechSynthesis) {
          window.speechSynthesis.cancel();
        }
      })
      .catch(function () {
        form.submit(); // envia do jeito normal, com recarga da página
      });
  });
});

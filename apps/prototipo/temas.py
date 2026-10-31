"""Paletas por apoio (skill design_neuro). Contraste de texto verificado em scripts/contraste_paletas.py.

A paleta acompanha o APOIO ligado, nunca um diagnóstico, e nunca é mostrada como rótulo do aluno.
Ordem de prioridade quando há vários apoios: modo limpo > foco > textual > concreto > base.
"""

TEMAS = {
    "base": {
        "nome": "Base (todos)",
        "fundo": "#F7F8FA", "superficie": "#FFFFFF", "texto": "#1F2933", "texto_suave": "#52606D",
        "destaque": "#2B59C3", "destaque_suave": "#E6EDFB", "borda": "#E1E5EA",
        "por_que": "Neutra, um único destaque azul. Azul/laranja em vez de verde/vermelho (daltonismo).",
    },
    "foco": {
        "nome": "Calma (foco e previsibilidade)",
        "fundo": "#F4F6F8", "superficie": "#FFFFFF", "texto": "#1E293B", "texto_suave": "#475569",
        "destaque": "#35557F", "destaque_suave": "#E5EBF2", "borda": "#DDE3EA",
        "por_que": "Baixa saturação e um só destaque: menos estímulo competindo pela atenção. Segue o 'use cores simples, evite cores vivas contrastantes' do guia GOV.UK para usuários autistas.",
    },
    "textual": {
        "nome": "Leitura confortável (textual)",
        "fundo": "#FBF8F1", "superficie": "#FFFDF8", "texto": "#2B2B2B", "texto_suave": "#555049",
        "destaque": "#1F5A96", "destaque_suave": "#E7EEF7", "borda": "#E8E1D3",
        "por_que": "Fundo creme e texto cinza-escuro (não preto puro) reduzem o brilho para quem tem estresse visual. Guias de dislexia lembram que isso é preferência individual: o aluno pode trocar.",
    },
    "concreto": {
        "nome": "Visual (interativo e concreto)",
        "fundo": "#F7F9FB", "superficie": "#FFFFFF", "texto": "#1F2933", "texto_suave": "#52606D",
        "destaque": "#0B6BA8", "destaque_suave": "#E3F0F8", "borda": "#E1E5EA",
        "por_que": "Destaque azul e cores de apoio da paleta Okabe-Ito (seguras para daltonismo) para representações visuais, como barras de fração.",
        "dados": ["#0072B2", "#E69F00", "#009E73", "#CC79A7"],
    },
    "limpo": {
        "nome": "Modo limpo",
        "fundo": "#FFFFFF", "superficie": "#FFFFFF", "texto": "#111827", "texto_suave": "#374151",
        "destaque": "#1D4ED8", "destaque_suave": "#EEF2FF", "borda": "#D1D5DB",
        "por_que": "Sem cores de enfeite: só texto, um destaque e muito espaço. Letra maior.",
    },
}


def tema_para(mascara, modo_limpo=False):
    if modo_limpo:
        return "limpo"
    if mascara & 4:
        return "foco"
    if mascara & 2:
        return "textual"
    if mascara & 1:
        return "concreto"
    return "base"

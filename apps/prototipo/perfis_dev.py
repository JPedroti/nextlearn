"""Ferramenta do desenvolvedor (só com DEBUG): simular a área do aluno para cada perfil.

O aluno NUNCA vê estes rótulos. Na escola, o que liga a interface são os apoios escolhidos pelo professor;
aqui o rótulo serve só para o time comparar cenários. Cada perfil vira apoios (bits da máscara), preferências
de interface, um tema e a intensidade das cores do cenário.

Cores (base: docs/PERFIS_E_METRICAS.md, docs/METRICAS_ENSINO.md, docs/design_neuro.md):
- TEA (P4): hipersensibilidade sensorial é comum → cores simples e pouco saturadas, sem contraste vibrante,
  sem animação e layout sempre igual (guia GOV.UK para usuários autistas; práticas NCAEP 2020).
- TDAH (P3): memória de trabalho (Kofler et al., 2020) → poucos estímulos competindo, um destaque só por tela.
- Dislexia (P1): fundo creme/tingido e texto cinza-escuro reduzem brilho; letras espaçadas (Zorzi et al., 2012);
  cor é preferência individual (British Dyslexia Association).
- Discalculia (P5): cor como código para quantidades (Okabe-Ito, seguro para daltonismo); pode ser vivo.
- TDL (P2): linguagem simples + apoio visual; cores médias.
- DI / ritmo (P7): concreto + passos curtos; cores vivas mas com poucos elementos.
- TDC (P6): alvos maiores (WCAG 2.5.5); cores padrão.
- Altas habilidades (P8): cenário completo e vivo; mais desafio (fora da v1 no conteúdo).
Os números de intensidade são valor de produto, a calibrar com uso real.
"""

PERFIS_DEV = [
    {"id": "", "nome": "Perfil do banco (Davi)", "desc": "Usa os apoios que o professor marcou para o aluno."},
    {"id": "nenhum", "nome": "Sem adaptação", "desc": "Aula original, cenário completo.",
     "apoios": {}, "prefs": {}, "tema": "base", "int": {"saturacao": 1.0, "luz": 0.0, "densidade": 1.0}},
    {"id": "tdah", "nome": "TDAH (atenção / memória de trabalho)", "desc": "Foco: um passo por vez, um destaque, sem animação automática.",
     "apoios": {"foco": True}, "prefs": {}, "tema": "foco", "int": {"saturacao": 0.75, "luz": 0.03, "densidade": 0.6}},
    {"id": "tea", "nome": "TEA (previsibilidade / sensorial)", "desc": "Foco + textual, cores suaves, nada se mexe, layout fixo.",
     "apoios": {"foco": True, "textual": True}, "prefs": {"limpo": False}, "tema": "brisa", "int": {"saturacao": 0.45, "luz": 0.06, "densidade": 0.45}},
    {"id": "tea_tdah", "nome": "TEA + TDAH", "desc": "União dos ajustes; vale o mais restritivo.",
     "apoios": {"foco": True, "textual": True}, "prefs": {}, "tema": "brisa", "int": {"saturacao": 0.45, "luz": 0.06, "densidade": 0.4}},
    {"id": "dislexia", "nome": "Dislexia (leitura)", "desc": "Textual + ouvir + letras espaçadas, fundo creme.",
     "apoios": {"textual": True}, "prefs": {"voz": True, "letras": True}, "tema": "textual", "int": {"saturacao": 0.8, "luz": 0.04, "densidade": 0.8}},
    {"id": "discalculia", "nome": "Discalculia (matemática)", "desc": "Concreto: figuras e cor como código.",
     "apoios": {"concreto": True}, "prefs": {}, "tema": "concreto", "int": {"saturacao": 1.0, "luz": 0.0, "densidade": 0.9}},
    {"id": "tdl", "nome": "TDL (linguagem)", "desc": "Textual + concreto.",
     "apoios": {"textual": True, "concreto": True}, "prefs": {"voz": True}, "tema": "textual", "int": {"saturacao": 0.85, "luz": 0.02, "densidade": 0.8}},
    {"id": "di", "nome": "Deficiência intelectual / ritmo", "desc": "Concreto + foco, passos curtos, mais revisão.",
     "apoios": {"foco": True, "concreto": True}, "prefs": {}, "tema": "concreto", "int": {"saturacao": 0.95, "luz": 0.02, "densidade": 0.55}},
    {"id": "tdc", "nome": "TDC / dispraxia (motor)", "desc": "Alvos maiores, sem arrastar.",
     "apoios": {}, "prefs": {"alvos": True}, "tema": "base", "int": {"saturacao": 1.0, "luz": 0.0, "densidade": 0.9}},
    {"id": "ah", "nome": "Altas habilidades", "desc": "Cenário completo, mais vivo.",
     "apoios": {}, "prefs": {}, "tema": "base", "int": {"saturacao": 1.1, "luz": 0.0, "densidade": 1.0}},
    {"id": "limpo", "nome": "Modo limpo (preferência)", "desc": "Sem enfeites, letra maior.",
     "apoios": {}, "prefs": {"limpo": True}, "tema": "limpo", "int": {"saturacao": 0.3, "luz": 0.1, "densidade": 0.3}},
]
POR_ID = {p["id"]: p for p in PERFIS_DEV}

# Intensidade padrão do cenário quando o perfil vem do banco (pelos apoios)
def intensidade_por_apoios(a):
    if a.get("limpo"):
        return POR_ID["limpo"]["int"]
    if a.get("foco") and a.get("textual"):
        return POR_ID["tea"]["int"]
    if a.get("foco"):
        return POR_ID["tdah"]["int"] if not a.get("concreto") else POR_ID["di"]["int"]
    if a.get("textual"):
        return POR_ID["dislexia"]["int"]
    if a.get("concreto"):
        return POR_ID["discalculia"]["int"]
    return POR_ID["nenhum"]["int"]

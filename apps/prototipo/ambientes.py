"""Ambientes da trilha do aluno: cada "mundo" tem no máximo 10 fases (aulas); depois começa outro mundo,
mesmo que a matéria continue (Matemática I → Matemática II).

Cada ambiente define uma paleta e um conjunto de elementos de cenário. A `semente` muda a ordem, o tamanho,
o lado e um pouco o tom das cores, para cada mundo parecer novo. O perfil de apoio ajusta a intensidade das
cores (ver PERFIS_DEV / docs/design_neuro.md): menos saturação para quem é sensível a estímulos.
"""

import colorsys
import random

FASES_POR_AMBIENTE = 10

# ---------------------------------------------------------------------------
# Biblioteca de elementos (SVG numa caixa 100x100, base no meio de baixo; cores a, b, c)
# ---------------------------------------------------------------------------
ELEMENTOS = {
    # Deserto
    "piramide": '<path d="M50 18 L92 100 H8Z" fill="{a}"/><path d="M50 18 L92 100 H58Z" fill="{b}"/><path d="M30 70 h40 M22 85 h56" stroke="{c}" stroke-width="2" opacity=".5"/>',
    "oasis": '<ellipse cx="50" cy="94" rx="44" ry="8" fill="{c}"/><path d="M40 92 C42 70 44 55 50 40" stroke="#8B5A2B" stroke-width="5" fill="none"/><path d="M50 40 C38 30 26 32 18 40 M50 40 C60 28 74 28 82 36 M50 40 C48 26 54 18 62 14 M50 40 C40 38 30 48 28 58" stroke="{a}" stroke-width="7" fill="none" stroke-linecap="round"/>',
    "camelo": '<path d="M18 62 C18 46 30 40 38 48 C42 36 54 36 58 48 C62 44 70 44 72 52 L80 40 C84 34 92 36 90 44 L82 60 C80 66 74 68 68 66 L66 98 M60 66 L58 98 M30 66 L28 98 M22 64 L20 98" fill="{a}" stroke="{a}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/><circle cx="86" cy="40" r="1.8" fill="#222"/>',
    "cacto": '<path d="M50 100 V30 a8 8 0 0 1 16 0 V100Z M50 64 H38 V44 a6 6 0 0 1 12 0 M66 56 H76 V40 a6 6 0 0 1 12 0 V62 H66" fill="{a}"/><path d="M58 34 V96" stroke="{b}" stroke-width="2" opacity=".5"/>',
    "duna": '<path d="M0 100 C20 70 40 62 60 72 C76 80 88 76 100 70 V100Z" fill="{b}"/>',
    # Floresta
    "pinheiro": '<rect x="46" y="80" width="8" height="20" fill="#7A4E2D"/><path d="M50 8 L80 50 H64 L86 82 H14 L36 50 H20Z" fill="{a}"/><path d="M50 8 L80 50 H64 L86 82 H50Z" fill="{b}" opacity=".6"/>',
    "arvore": '<rect x="45" y="60" width="10" height="40" fill="#7A4E2D"/><circle cx="50" cy="42" r="28" fill="{a}"/><circle cx="34" cy="54" r="16" fill="{b}"/><circle cx="66" cy="52" r="18" fill="{b}"/>',
    "cogumelo": '<rect x="42" y="62" width="16" height="38" rx="6" fill="#F5EBDD"/><path d="M14 66 C14 34 86 34 86 66Z" fill="{c}"/><circle cx="36" cy="52" r="5" fill="#FFF"/><circle cx="60" cy="46" r="6" fill="#FFF"/>',
    "arbusto": '<circle cx="30" cy="80" r="20" fill="{a}"/><circle cx="56" cy="74" r="24" fill="{b}"/><circle cx="76" cy="84" r="16" fill="{a}"/>',
    # Fundo do mar
    "coral": '<path d="M50 100 V60 M50 74 C40 66 36 54 38 40 M50 70 C62 62 66 50 64 36 M38 52 C30 48 28 40 30 32 M64 48 C72 44 74 36 72 28" stroke="{c}" stroke-width="8" fill="none" stroke-linecap="round"/>',
    "peixe": '<path d="M20 50 C34 30 62 30 74 50 C62 70 34 70 20 50Z" fill="{a}"/><path d="M74 50 L92 38 V62Z" fill="{b}"/><circle cx="34" cy="46" r="3" fill="#1F2933"/>',
    "alga": '<path d="M40 100 C30 80 50 70 40 50 C32 36 46 26 42 12 M58 100 C66 82 50 72 60 56 C66 46 56 36 62 26" stroke="{a}" stroke-width="7" fill="none" stroke-linecap="round"/>',
    "bolhas": '<circle cx="40" cy="70" r="7" fill="none" stroke="#FFFFFF" stroke-width="3" opacity=".7"/><circle cx="56" cy="46" r="5" fill="none" stroke="#FFFFFF" stroke-width="3" opacity=".7"/><circle cx="46" cy="24" r="4" fill="none" stroke="#FFFFFF" stroke-width="3" opacity=".7"/>',
    "concha": '<path d="M20 96 C20 60 80 60 80 96Z" fill="{c}"/><path d="M50 64 V96 M34 70 L40 96 M66 70 L60 96" stroke="{b}" stroke-width="3"/>',
    # Gelo
    "iceberg": '<path d="M10 100 L30 50 L44 62 L58 30 L90 100Z" fill="#FFFFFF"/><path d="M58 30 L90 100 H60 L52 70Z" fill="{b}" opacity=".6"/>',
    "iglu": '<path d="M12 100 C12 50 88 50 88 100Z" fill="#FFFFFF"/><path d="M40 100 C40 82 60 82 60 100Z" fill="{b}"/><path d="M20 82 H80 M30 66 H70" stroke="{b}" stroke-width="2" opacity=".6"/>',
    "pinguim": '<ellipse cx="50" cy="68" rx="20" ry="30" fill="#1F2933"/><ellipse cx="50" cy="74" rx="13" ry="22" fill="#FFFFFF"/><circle cx="50" cy="38" r="13" fill="#1F2933"/><path d="M50 42 l6 3 -6 3Z" fill="#F2A541"/><circle cx="46" cy="36" r="2" fill="#FFF"/>',
    "floco": '<path d="M50 20 V80 M24 35 L76 65 M24 65 L76 35" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>',
    # Espaço
    "planeta": '<circle cx="50" cy="56" r="26" fill="{a}"/><ellipse cx="50" cy="58" rx="44" ry="10" fill="none" stroke="{c}" stroke-width="5"/><circle cx="40" cy="48" r="5" fill="{b}" opacity=".6"/>',
    "estrela": '<path d="M50 20 L58 44 L84 44 L63 59 L71 84 L50 69 L29 84 L37 59 L16 44 L42 44Z" fill="{c}"/>',
    "foguete": '<path d="M50 10 C66 26 68 56 62 80 H38 C32 56 34 26 50 10Z" fill="#FFFFFF"/><circle cx="50" cy="44" r="8" fill="{a}"/><path d="M38 64 L24 86 H38 M62 64 L76 86 H62" fill="{c}"/><path d="M42 82 L50 100 L58 82Z" fill="#F2A541"/>',
    "lua": '<circle cx="50" cy="50" r="30" fill="#F1F5F9"/><circle cx="40" cy="42" r="6" fill="#CBD5E1"/><circle cx="60" cy="60" r="8" fill="#CBD5E1"/>',
    "cometa": '<circle cx="74" cy="30" r="9" fill="{c}"/><path d="M68 36 L20 80" stroke="{c}" stroke-width="5" stroke-linecap="round" opacity=".5"/>',
    # Vulcão
    "vulcao": '<path d="M4 100 L40 34 H60 L96 100Z" fill="{a}"/><path d="M40 34 H60 L56 44 L50 40 L44 46Z" fill="{c}"/><path d="M50 30 C44 18 54 12 48 2" stroke="#9CA3AF" stroke-width="6" fill="none" stroke-linecap="round" opacity=".7"/>',
    "rocha": '<path d="M14 100 L24 70 L50 58 L78 66 L88 100Z" fill="{b}"/><path d="M50 58 L78 66 L88 100 H56Z" fill="{a}" opacity=".5"/>',
    "lava": '<ellipse cx="50" cy="94" rx="40" ry="7" fill="{c}"/><circle cx="36" cy="86" r="4" fill="{c}"/><circle cx="62" cy="82" r="3" fill="{c}"/>',
    # Savana
    "acacia": '<path d="M50 100 V56 M50 70 L32 52 M50 64 L68 50" stroke="#7A4E2D" stroke-width="6" fill="none"/><ellipse cx="50" cy="44" rx="44" ry="12" fill="{a}"/>',
    "girafa": '<path d="M30 70 H66 V98 M34 70 V98 M60 98 V70" stroke="{c}" stroke-width="6"/><path d="M62 72 L72 22" stroke="{c}" stroke-width="9" stroke-linecap="round"/><ellipse cx="76" cy="20" rx="9" ry="6" fill="{c}"/><circle cx="44" cy="66" r="3" fill="#8B5A2B"/><circle cx="56" cy="64" r="3" fill="#8B5A2B"/>',
    "capim": '<path d="M30 100 L26 70 M40 100 L42 64 M50 100 L48 72 M60 100 L64 66 M70 100 L72 74" stroke="{a}" stroke-width="4" stroke-linecap="round"/>',
    "sol": '<circle cx="50" cy="50" r="22" fill="{c}"/><circle cx="50" cy="50" r="32" fill="{c}" opacity=".25"/>',
    # Cidade
    "predio": '<rect x="24" y="20" width="52" height="80" fill="{a}"/><g fill="#FFE8A3"><rect x="32" y="30" width="10" height="10"/><rect x="58" y="30" width="10" height="10"/><rect x="32" y="50" width="10" height="10"/><rect x="58" y="50" width="10" height="10"/><rect x="32" y="70" width="10" height="10"/></g>',
    "casa": '<rect x="22" y="56" width="56" height="44" fill="{a}"/><path d="M14 58 L50 26 L86 58Z" fill="{c}"/><rect x="44" y="74" width="14" height="26" fill="{b}"/>',
    "poste": '<path d="M50 100 V30 H66" stroke="#4B5563" stroke-width="5" fill="none"/><circle cx="66" cy="36" r="7" fill="#FFE8A3"/>',
    "nuvem": '<path d="M20 70 a14 14 0 0 1 10-24 a20 20 0 0 1 38-4 a14 14 0 0 1 12 28Z" fill="#FFFFFF" opacity=".9"/>',
    # Praia
    "palmeira": '<path d="M46 100 C46 76 52 56 60 40" stroke="#8B5A2B" stroke-width="6" fill="none"/><path d="M60 40 C46 30 32 34 24 44 M60 40 C70 28 84 30 90 38 M60 40 C60 24 70 16 78 14 M60 40 C50 40 42 50 40 60" stroke="{a}" stroke-width="7" fill="none" stroke-linecap="round"/>',
    "guarda_sol": '<path d="M50 100 V40" stroke="#4B5563" stroke-width="3"/><path d="M14 46 C20 20 80 20 86 46Z" fill="{c}"/><path d="M38 46 C40 26 46 22 50 22 C54 22 60 26 62 46" fill="#FFFFFF" opacity=".7"/>',
    "farol": '<path d="M38 100 L42 34 H58 L62 100Z" fill="#FFFFFF"/><path d="M40 60 H60 M39 80 H61" stroke="{c}" stroke-width="8"/><rect x="40" y="22" width="20" height="12" fill="#FFE8A3"/><path d="M38 22 L50 10 L62 22Z" fill="{c}"/>',
    "barco": '<path d="M14 80 H86 L74 96 H26Z" fill="{b}"/><path d="M50 78 V20 L80 72Z" fill="#FFFFFF"/><path d="M48 78 V30 L24 72Z" fill="{c}"/>',
    # Caverna de cristal
    "cristal": '<path d="M50 14 L66 50 L56 100 H44 L34 50Z" fill="{a}"/><path d="M50 14 L66 50 L56 100 H50Z" fill="{b}" opacity=".7"/><path d="M24 60 L32 76 L28 100 H20 L16 76Z" fill="{c}"/>',
    "estalactite": '<path d="M20 0 L28 40 L36 0 M44 0 L52 56 L60 0 M66 0 L72 30 L78 0" fill="{b}"/>',
    "morcego": '<path d="M50 50 C44 42 30 40 18 48 C26 50 30 56 30 60 C38 54 44 56 50 60 C56 56 62 54 70 60 C70 56 74 50 82 48 C70 40 56 42 50 50Z" fill="#374151"/>',
    "gema": '<path d="M30 70 L40 56 H60 L70 70 L50 92Z" fill="{c}"/><path d="M40 56 L50 70 L60 56 M30 70 H70" stroke="#FFFFFF" stroke-width="2" opacity=".6" fill="none"/>',
    # Selva
    "folhagem": '<path d="M50 100 C30 80 14 70 10 50 C30 52 44 66 50 82 C56 60 70 44 90 40 C88 64 70 82 50 100Z" fill="{a}"/><path d="M50 100 V60" stroke="{b}" stroke-width="3"/>',
    "arara": '<ellipse cx="50" cy="56" rx="12" ry="18" fill="{c}"/><circle cx="50" cy="34" r="10" fill="{c}"/><path d="M58 34 l8 4 -8 4Z" fill="#1F2933"/><path d="M46 72 L40 98 M54 72 L58 98" stroke="{a}" stroke-width="6" stroke-linecap="round"/><path d="M38 52 C28 58 26 68 30 76" stroke="{a}" stroke-width="7" fill="none" stroke-linecap="round"/>',
    "flor": '<path d="M50 100 V60" stroke="#3F7D20" stroke-width="4"/><circle cx="50" cy="50" r="8" fill="#F2C94C"/><circle cx="50" cy="36" r="9" fill="{c}"/><circle cx="64" cy="50" r="9" fill="{c}"/><circle cx="36" cy="50" r="9" fill="{c}"/><circle cx="50" cy="64" r="9" fill="{c}"/>',
    "cipo": '<path d="M30 0 C40 30 20 50 34 80 M70 0 C60 26 78 46 66 70" stroke="{a}" stroke-width="5" fill="none"/><circle cx="34" cy="80" r="5" fill="{a}"/>',
    # Montanha / campo
    "montanha": '<path d="M0 100 L38 26 L60 60 L72 44 L100 100Z" fill="{a}"/><path d="M38 26 L48 46 L42 44 L36 50 L30 42Z" fill="#FFFFFF"/>',
    "moinho": '<path d="M40 100 L44 46 H56 L60 100Z" fill="#FFFFFF"/><path d="M50 44 L50 10 M50 44 L84 44 M50 44 L50 78 M50 44 L16 44" stroke="{c}" stroke-width="6" stroke-linecap="round"/><circle cx="50" cy="44" r="5" fill="#4B5563"/>',
    "ovelha": '<circle cx="40" cy="64" r="14" fill="#FFFFFF"/><circle cx="58" cy="62" r="16" fill="#FFFFFF"/><circle cx="74" cy="56" r="8" fill="#374151"/><path d="M42 76 V96 M62 76 V96" stroke="#374151" stroke-width="4"/>',
    "passaro": '<path d="M30 50 Q40 40 50 50 Q60 40 70 50" stroke="#374151" stroke-width="3" fill="none"/>',
}

# ---------------------------------------------------------------------------
# Ambientes: paleta (céu em cima, chão embaixo) + elementos com peso. Pelo menos 10.
# ---------------------------------------------------------------------------
AMBIENTES = [
    {"id": "deserto", "nome": "Deserto", "ceu": "#FCE9C8", "chao": "#E7BF7E", "a": "#4F9A5B", "b": "#D9A866", "c": "#5DB8CC",
     "elementos": {"piramide": 3, "oasis": 2, "camelo": 3, "cacto": 3, "duna": 2, "sol": 1}},
    {"id": "floresta", "nome": "Floresta", "ceu": "#DDF1E4", "chao": "#9BCB8A", "a": "#2F7D4F", "b": "#4FA36A", "c": "#D64545",
     "elementos": {"pinheiro": 4, "arvore": 3, "cogumelo": 2, "arbusto": 2, "passaro": 1}},
    {"id": "mar", "nome": "Fundo do mar", "ceu": "#BEE7F2", "chao": "#4FA3C7", "a": "#F2A541", "b": "#E8833A", "c": "#E86A8C",
     "elementos": {"coral": 3, "peixe": 4, "alga": 3, "bolhas": 2, "concha": 2}},
    {"id": "gelo", "nome": "Polo de gelo", "ceu": "#E6F3FB", "chao": "#B9DCEF", "a": "#7DB7DA", "b": "#8EC3E0", "c": "#F2A541",
     "elementos": {"iceberg": 3, "iglu": 2, "pinguim": 4, "floco": 2}},
    {"id": "espaco", "nome": "Espaço", "ceu": "#1E2A5A", "chao": "#3B2F6B", "a": "#E86A8C", "b": "#9B8CF5", "c": "#F2C94C",
     "elementos": {"planeta": 3, "estrela": 4, "foguete": 2, "lua": 1, "cometa": 2}},
    {"id": "vulcao", "nome": "Vulcão", "ceu": "#FBE3D6", "chao": "#B9876B", "a": "#7C4A3A", "b": "#8A6A5C", "c": "#E8590C",
     "elementos": {"vulcao": 3, "rocha": 3, "lava": 2, "passaro": 1}},
    {"id": "savana", "nome": "Savana", "ceu": "#FFF1CC", "chao": "#D8C27A", "a": "#6E8B3D", "b": "#B9A35A", "c": "#E0A100",
     "elementos": {"acacia": 4, "girafa": 3, "capim": 3, "sol": 1}},
    {"id": "cidade", "nome": "Cidade", "ceu": "#E3ECF7", "chao": "#B8C4D4", "a": "#5B6B8C", "b": "#3F4C66", "c": "#D64545",
     "elementos": {"predio": 4, "casa": 3, "poste": 2, "nuvem": 2}},
    {"id": "praia", "nome": "Praia", "ceu": "#D6F0FA", "chao": "#F3DCA8", "a": "#2F9E6E", "b": "#2E86A8", "c": "#E8590C",
     "elementos": {"palmeira": 4, "guarda_sol": 2, "farol": 1, "barco": 2, "nuvem": 1}},
    {"id": "caverna", "nome": "Caverna de cristal", "ceu": "#2B2346", "chao": "#46386E", "a": "#7DD3FC", "b": "#A78BFA", "c": "#F472B6",
     "elementos": {"cristal": 4, "estalactite": 2, "morcego": 2, "gema": 3}},
    {"id": "selva", "nome": "Selva tropical", "ceu": "#D9F2DC", "chao": "#6FB46A", "a": "#1F7A4A", "b": "#2F9E6E", "c": "#E8590C",
     "elementos": {"folhagem": 4, "arara": 2, "flor": 3, "cipo": 2}},
    {"id": "campo", "nome": "Montanhas e campos", "ceu": "#E4F0FB", "chao": "#A8D08D", "a": "#6B7FA8", "b": "#88A86B", "c": "#C2410C",
     "elementos": {"montanha": 3, "moinho": 2, "ovelha": 3, "flor": 2, "nuvem": 1}},
]
POR_ID = {a["id"]: a for a in AMBIENTES}


# ---------------------------------------------------------------------------
# Cores
# ---------------------------------------------------------------------------
def _ajustar(hexcor, saturacao=1.0, luz=0.0, matiz=0.0):
    r, g, b = (int(hexcor[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = (h + matiz / 360) % 1
    s = max(0, min(1, s * saturacao))
    l = max(0, min(1, l + luz))
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#%02X%02X%02X" % (round(r * 255), round(g * 255), round(b * 255))


def cenario(ambiente_id, semente, altura, intensidade):
    """Monta o cenário de um mundo: cores ajustadas e elementos posicionados nas laterais da trilha.
    intensidade = {"saturacao": 0.5–1.1, "luz": -0.1–0.1, "densidade": 0.5–1.0} (vem do perfil)."""
    amb = POR_ID[ambiente_id]
    rnd = random.Random(semente)
    sat, luz = intensidade["saturacao"], intensidade["luz"]
    matiz = rnd.uniform(-14, 14)                       # cada mundo puxa o tom um pouco para um lado
    cor = {k: _ajustar(amb[k], sat, luz, matiz) for k in ("ceu", "chao", "a", "b", "c")}
    tipos, pesos = zip(*amb["elementos"].items())
    n = max(3, int(altura / 95 * intensidade["densidade"]))
    elementos = []
    for i in range(n):
        tipo = rnd.choices(tipos, weights=pesos)[0]
        lado = i % 2 if rnd.random() < .8 else rnd.randint(0, 1)
        x = rnd.uniform(4, 22) if lado == 0 else rnd.uniform(74, 92)   # % da largura, longe do caminho
        y = (i + rnd.uniform(.2, .9)) / n * altura
        escala = rnd.uniform(.75, 1.35)
        trio = [cor["a"], cor["b"], cor["c"]]
        rnd.shuffle(trio) if rnd.random() < .35 else None            # às vezes troca as cores de lugar
        svg = ELEMENTOS[tipo].format(a=trio[0], b=trio[1], c=trio[2])
        elementos.append({"tipo": tipo, "x": round(x, 1), "y": round(y), "tam": round(70 * escala),
                          "espelhar": rnd.random() < .5, "svg": svg})
    return {"id": amb["id"], "nome": amb["nome"], "cor": cor, "elementos": elementos,
            "escuro": ambiente_id in ("espaco", "caverna")}

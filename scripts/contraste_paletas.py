"""Confere o contraste WCAG (mínimo 4,5:1 para texto) das paletas em apps/prototipo/temas.py.

Uso: python scripts/contraste_paletas.py
"""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("temas", Path(__file__).resolve().parent.parent / "apps/prototipo/temas.py")
temas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(temas)


def luminancia(hexcor):
    r, g, b = (int(hexcor.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contraste(a, b):
    la, lb = sorted([luminancia(a), luminancia(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


PARES = [("texto", "fundo"), ("texto", "superficie"), ("texto_suave", "fundo"), ("texto_suave", "superficie"),
         ("destaque", "superficie"), ("destaque", "destaque_suave")]

falhas = 0
for nome, t in temas.TEMAS.items():
    linhas = []
    for a, b in PARES:
        c = contraste(t[a], t[b])
        falhas += c < 4.5
        linhas.append(f"{a}/{b} {c:.1f}{'  <-- FALHA' if c < 4.5 else ''}")
    c = contraste("#FFFFFF", t["destaque"])
    falhas += c < 4.5
    linhas.append(f"branco/destaque {c:.1f}{'  <-- FALHA' if c < 4.5 else ''}")
    print(f"[{nome}] " + " | ".join(linhas))
print("Tudo passa (>= 4,5:1)" if not falhas else f"{falhas} par(es) abaixo de 4,5:1")

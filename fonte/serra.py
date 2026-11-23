"""Linhas de serra usadas no site e na imagem de compartilhamento.

Cada serra é gerada a partir de uma semente fixa, então o desenho
é sempre o mesmo a cada build.
"""
import math
import random


def pontos(semente, n=14, minimo=0.15, maximo=0.85, pico=None):
    """Lista de alturas (0 a 1, onde 0 é o topo) ao longo da largura."""
    r = random.Random(semente)
    alturas = []
    for i in range(n + 1):
        t = i / n
        onda = 0.5 + 0.22 * math.sin(t * math.pi * 2.2 + semente) + 0.12 * math.sin(t * math.pi * 5.3 + semente * 1.7)
        onda += r.uniform(-0.08, 0.08)
        alturas.append(min(maximo, max(minimo, onda)))
    if pico is not None:
        # uma elevação mais marcada, lembrando a Pedra Azul
        i = int(pico * n)
        for k, f in ((i - 1, 0.55), (i, 0.25), (i + 1, 0.5)):
            if 0 <= k <= n:
                alturas[k] = min(alturas[k], f * maximo)
    return alturas


def caminho(semente, largura=1440, altura=100, fechado=True, **kw):
    """Caminho SVG suave. Fechado = silhueta preenchida até a base."""
    ys = pontos(semente, **kw)
    n = len(ys) - 1
    pts = [(largura * i / n, altura * y) for i, y in enumerate(ys)]
    d = f"M0 {pts[0][1]:.1f}"
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]
        x1, y1 = pts[i]
        mx = (x0 + x1) / 2
        d += f" C{mx:.1f} {y0:.1f} {mx:.1f} {y1:.1f} {x1:.1f} {y1:.1f}"
    if fechado:
        d += f" L{largura} {altura} L0 {altura} Z"
    return d


def clip_topo(semente, profundidade=9, n=10):
    """clip-path polygon com o topo em forma de serra (para fotos e cartões)."""
    ys = pontos(semente, n=n, minimo=0.05, maximo=1.0)
    topo = [f"{100 * i / n:.1f}% {profundidade * y:.2f}%" for i, y in enumerate(ys)]
    return "polygon(" + ", ".join(topo + ["100% 100%", "0% 100%"]) + ")"

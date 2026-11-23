"""Gera og-image.jpg (1200x630), apple-touch-icon.png (180) e favicon-32.png.

Uso: python3 gerar_imagens.py PASTA_DE_SAIDA
Fontes usadas no servidor de build (troque se necessário):
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

import serra

AQUI = Path(__file__).parent
SAIDA = Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI / "../site"
SAIDA.mkdir(parents=True, exist_ok=True)

FONTE_NOME = "/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrechorus-mediumitalic.otf"
FONTE_TITULO = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"
FONTE_TEXTO = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
FONTE_TEXTO_B = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"

LINHO = (235, 233, 220)
NEVOA = (244, 243, 236)
SALVIA = (166, 167, 153)
SALVIA_FUNDA = (95, 99, 85)
CAFE = (32, 25, 19)
AMEIXA = (90, 71, 77)


def serra_poligono(semente, w, h, y0, amp, **kw):
    ys = serra.pontos(semente, n=24, **kw)
    n = len(ys) - 1
    pts = [(w * i / n, y0 + amp * y) for i, y in enumerate(ys)]
    return pts + [(w, h), (0, h)]


def og():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), LINHO)
    d = ImageDraw.Draw(img)

    # serras ao fundo
    d.polygon(serra_poligono(3, W, H, 430, 120, pico=0.18), fill=(214, 213, 199))
    d.polygon(serra_poligono(7, W, H, 500, 90), fill=SALVIA)
    d.polygon(serra_poligono(11, W, H, 560, 60), fill=SALVIA_FUNDA)

    # foto no centro, com topo em serra
    foto = Image.open(AQUI / "fotos/hero.jpg").convert("RGB")
    fw, fh = 400, 500
    foto = foto.resize((fw, fh), Image.LANCZOS)
    mask = Image.new("L", (fw, fh), 0)
    md = ImageDraw.Draw(mask)
    ys = serra.pontos(5, n=10, minimo=0.05, maximo=1.0)
    top = [(fw * i / 10, 40 * y) for i, y in enumerate(ys)]
    md.polygon(top + [(fw, fh), (0, fh)], fill=255)
    fx, fy = (W - fw) // 2, H - fh
    img.paste(foto, (fx, fy), mask)

    # névoa sobre a base da foto
    nev = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    nd = ImageDraw.Draw(nev)
    nd.polygon(serra_poligono(13, W, H, 575, 40), fill=LINHO + (235,))
    img.paste(nev, (0, 0), nev)

    f_nome = ImageFont.truetype(FONTE_NOME, 74)
    f_prof = ImageFont.truetype(FONTE_TEXTO_B, 20)
    f_tit = ImageFont.truetype(FONTE_TITULO, 36)
    f_txt = ImageFont.truetype(FONTE_TEXTO, 21)

    # lado esquerdo: nome e profissão
    d.text((60, 120), "Ivonete", font=f_nome, fill=CAFE)
    d.text((60, 200), "Morelo", font=f_nome, fill=CAFE)
    d.text((64, 300), "Hipnoterapeuta", font=f_prof, fill=SALVIA_FUNDA)
    d.text((64, 330), "Hipnose clínica", font=f_txt, fill=SALVIA_FUNDA)

    # lado direito: frase, cidade e selo
    x = 840
    for i, linha in enumerate(["Por que a mesma", "história insiste", "em voltar?"]):
        d.text((x, 110 + i * 46), linha, font=f_tit, fill=CAFE)
    d.text((x, 270), "Pedra Azul, ES, e online", font=f_txt, fill=SALVIA_FUNDA)
    selo = "Agende pelo WhatsApp"
    tw = d.textlength(selo, font=f_prof)
    d.rounded_rectangle((x, 315, x + tw + 44, 365), radius=25, fill=AMEIXA)
    d.text((x + 22, 328), selo, font=f_prof, fill=NEVOA)

    img.save(SAIDA / "og-image.jpg", quality=86, optimize=True, progressive=True)


def icone(tam, nome):
    img = Image.new("RGB", (tam, tam), SALVIA_FUNDA)
    d = ImageDraw.Draw(img)
    pts = serra_poligono(7, tam, tam, tam * 0.66, tam * 0.18)
    d.polygon(pts, fill=SALVIA)
    f = ImageFont.truetype(FONTE_NOME, int(tam * 0.62))
    texto = "I"
    bb = d.textbbox((0, 0), texto, font=f)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((tam - w) / 2 - bb[0], (tam * 0.92 - h) / 2 - bb[1]), texto, font=f, fill=NEVOA)
    img.save(SAIDA / nome, optimize=True)


if __name__ == "__main__":
    og()
    icone(180, "apple-touch-icon.png")
    icone(32, "favicon-32.png")
    print("Imagens geradas em", SAIDA.resolve())

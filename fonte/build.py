"""Gera o site da Ivonete Morelo.

Uso:
    python3 build.py

Edite os dados abaixo, rode o script e envie o conteúdo da pasta ../site
para a hospedagem. As fotos ficam em fonte/fotos/.
"""
import base64
import json
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

import serra

# ------------------------------------------------------------------
# DADOS DA PROFISSIONAL (edite aqui)
# ------------------------------------------------------------------
NOME = "Ivonete Morelo"
PRIMEIRO_NOME = "Ivonete"
PROFISSAO = "Hipnoterapeuta"
SUBTITULO = "Especialista em Ansiedade & Depressão"   # aparece abaixo do nome no cabeçalho
WHATSAPP = "5528981145808"          # só números, com DDI e DDD
INSTAGRAM = "https://www.instagram.com/ivonete_hipnoterapeuta/"
INSTAGRAM_USUARIO = "@ivonete_hipnoterapeuta"

# Link do perfil no Google Meu Negócio. Enquanto estiver vazio,
# o ícone abre uma busca no Google Maps pelo nome e endereço.
GOOGLE_NEGOCIO = ""

RUA = "R. Canal, 206"
BAIRRO = "Vila de Pedra Azul"
CIDADE = "Domingos Martins"
UF = "ES"
CEP = "29260-000"

# Endereço definitivo do site (troque quando o domínio for registrado)
DOMINIO = "https://ivonetemorelohipnoterapeuta.vercel.app"

# Fotos (dentro de fonte/fotos). Deixe FOTO_CONSULTORIO vazio para
# mostrar o espaço reservado sem foto.
FOTO_HERO = "hero.jpg"
FOTO_SOBRE = "sobre.jpg"
FOTO_CONSULTORIO = ""

# Depoimentos reais e autorizados. Lista vazia = seção escondida.
# Formato: {"nome": "...", "tema": "...", "texto": "..."}
DEPOIMENTOS = []
# ------------------------------------------------------------------

AQUI = Path(__file__).parent
SAIDA = AQUI.parent / "site"


def b64(caminho):
    dados = (AQUI / "fotos" / caminho).read_bytes()
    return "data:image/jpeg;base64," + base64.b64encode(dados).decode()


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def main():
    SAIDA.mkdir(exist_ok=True)
    subprocess.run([sys.executable, str(AQUI / "gerar_imagens.py"), str(SAIDA)], check=True)

    endereco_linha = f"{RUA}, {BAIRRO}, {CIDADE}, {UF}, {CEP}"
    busca_maps = "https://www.google.com/maps/search/?api=1&query=" + quote(f"{NOME}, {endereco_linha}")
    msg_agendar = f"Olá, {PRIMEIRO_NOME}! Vim pelo site e gostaria de agendar uma consulta de avaliação."
    msg_duvida = f"Olá, {PRIMEIRO_NOME}! Vim pelo site e tenho uma dúvida antes de agendar."

    jsonld = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": f"{NOME} | {PROFISSAO}",
        "description": "Hipnose clínica para ansiedade, depressão e padrões que se repetem. Atendimento presencial em Pedra Azul, Domingos Martins (ES), e online.",
        "url": DOMINIO + "/",
        "image": DOMINIO + "/og-image.jpg?v=1",
        "telephone": "+" + WHATSAPP,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": f"{RUA}, {BAIRRO}",
            "addressLocality": CIDADE,
            "addressRegion": UF,
            "postalCode": CEP,
            "addressCountry": "BR",
        },
        "areaServed": ["Domingos Martins", "Espírito Santo", "Brasil"],
        "sameAs": [INSTAGRAM] + ([GOOGLE_NEGOCIO] if GOOGLE_NEGOCIO else []),
    }

    if FOTO_CONSULTORIO:
        consultorio = f'<img src="{b64(FOTO_CONSULTORIO)}" alt="Consultório de {NOME} em Pedra Azul" loading="lazy" width="800" height="1000">'
    else:
        consultorio = ""

    if DEPOIMENTOS:
        itens = "".join(
            f'<li class="depo" data-r="cartao" style="--i:{i}"><span class="avatar" aria-hidden="true">{esc(d["nome"][0])}</span>'
            f'<p>{esc(d["texto"])}</p><p class="depo-nome">{esc(d["nome"])}<span>{esc(d["tema"])}</span></p></li>'
            for i, d in enumerate(DEPOIMENTOS)
        )
        depoimentos = (
            '<section class="secao depoimentos" aria-labelledby="t-depo"><div class="caixa">'
            '<div class="sec-cab"><h2 id="t-depo" data-split>Quem já passou por aqui</h2></div>'
            f'<ul class="depo-lista n{len(DEPOIMENTOS)}">{itens}</ul></div></section>'
        )
    else:
        depoimentos = ""

    valores = {
        "NOME": NOME,
        "PRIMEIRO_NOME": PRIMEIRO_NOME,
        "PROFISSAO": PROFISSAO,
        "SUBTITULO": esc(SUBTITULO),
        "WHATSAPP": WHATSAPP,
        "WA_AGENDAR": f"https://wa.me/{WHATSAPP}?text=" + quote(msg_agendar),
        "WA_DUVIDA": f"https://wa.me/{WHATSAPP}?text=" + quote(msg_duvida),
        "INSTAGRAM": INSTAGRAM,
        "INSTAGRAM_USUARIO": INSTAGRAM_USUARIO,
        "GOOGLE": GOOGLE_NEGOCIO or busca_maps,
        "MAPA": busca_maps,
        "RUA": RUA,
        "BAIRRO": BAIRRO,
        "CIDADE": CIDADE,
        "UF": UF,
        "CEP": CEP,
        "DOMINIO": DOMINIO,
        "IMG_HERO": b64(FOTO_HERO),
        "IMG_SOBRE": b64(FOTO_SOBRE),
        "CONSULTORIO": consultorio,
        "CONSULTORIO_CLASSE": "com-foto" if FOTO_CONSULTORIO else "sem-foto",
        "DEPOIMENTOS": depoimentos,
        "JSONLD": json.dumps(jsonld, ensure_ascii=False),
        "CLIP_HERO": serra.clip_topo(5, profundidade=8),
        "CLIP_SOBRE": serra.clip_topo(21, profundidade=7),
        "CLIP_LOCAL": serra.clip_topo(17, profundidade=8),
        "CLIP_C1": serra.clip_topo(31, profundidade=14, n=8),
        "CLIP_C2": serra.clip_topo(37, profundidade=14, n=8),
        "CLIP_C3": serra.clip_topo(41, profundidade=14, n=8),
    }
    # silhuetas preenchidas (bordas superiores das faixas)
    for i in range(1, 15):
        valores[f"S{i}"] = serra.caminho(i * 3 + 1, largura=1440, altura=100, pico=0.7 if i % 4 == 1 else None)
    valores["S1"] = serra.caminho(5, largura=1440, altura=100, minimo=0.25, maximo=0.75)
    valores["S2"] = serra.caminho(9, largura=1440, altura=100, minimo=0.2, maximo=0.6)
    # linhas finas (divisórias), mais largas que a tela para poder deslizar
    for i in range(1, 7):
        valores[f"L{i}"] = serra.caminho(i * 7 + 2, largura=2000, altura=120, fechado=False, n=22,
                                         minimo=0.1 + 0.08 * (i % 3), maximo=0.6 + 0.12 * (i % 3))

    html = (AQUI / "template.html").read_text(encoding="utf-8")
    for chave, valor in valores.items():
        html = html.replace("{{" + chave + "}}", valor)
    if "{{" in html:
        faltando = sorted(set(p.split("}}")[0] for p in html.split("{{")[1:]))
        raise SystemExit(f"Chaves sem valor no template: {faltando}")
    (SAIDA / "index.html").write_text(html, encoding="utf-8")
    print("Site gerado em", (SAIDA / "index.html").resolve(), f"({len(html)//1024} KB)")


if __name__ == "__main__":
    main()

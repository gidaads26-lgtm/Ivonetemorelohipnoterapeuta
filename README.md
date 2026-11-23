# Site de Ivonete Morelo, hipnoterapeuta

Site de uma página, com tudo num único `index.html` (estilos, código e fotos embutidos).

## Pastas

- `site/`: o que vai para a hospedagem. Envie todos os arquivos desta pasta para a raiz do domínio.
  - `index.html`, o site;
  - `og-image.jpg`, a imagem que aparece ao compartilhar o link no WhatsApp e nas redes;
  - `favicon-32.png` e `apple-touch-icon.png`, os ícones da aba e da tela inicial do celular.
- `fonte/`: os arquivos para editar o site.
  - `build.py`, com os dados da profissional no topo (nome, WhatsApp, Instagram, endereço, domínio, fotos e depoimentos);
  - `template.html`, com o texto e o visual do site;
  - `fotos/`, com as fotos usadas;
  - `serra.py`, que desenha as linhas de serra;
  - `gerar_imagens.py`, que gera a imagem de compartilhamento e os ícones.

## Como atualizar

1. Edite os dados no topo de `fonte/build.py`. Os mais comuns são:
   - `DOMINIO`, quando o domínio for registrado;
   - `GOOGLE_NEGOCIO`, com o link do perfil no Google;
   - `FOTO_CONSULTORIO`, com o nome do arquivo da foto colocada em `fonte/fotos/`;
   - `DEPOIMENTOS`, só com depoimentos reais e autorizados.
2. Para trocar textos, edite `fonte/template.html`. Os trechos entre `{{ }}` são preenchidos pelo `build.py`.
3. Rode o comando abaixo, de dentro da pasta `fonte`:

   ```
   python3 build.py
   ```

   Ele precisa de Python 3 com a biblioteca Pillow (`pip install pillow`). Se as fontes indicadas no topo de `gerar_imagens.py` não existirem no seu computador, troque os caminhos por fontes que você tenha.
4. Envie de novo o conteúdo da pasta `site/`.

Ao trocar a imagem de compartilhamento, mude `?v=1` para `?v=2` no `template.html` para o WhatsApp buscar a versão nova.

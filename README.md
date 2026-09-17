# Clippy Videos — Arquivos estáticos

Este diretório contém os arquivos estáticos utilizados pelo servidor do Clippy Videos, incluindo:

- Imagens;
- Scripts;
- Banners;
- Vídeos; e
- Outros recursos públicos.

## Como executar o servidor

### Pré-requisitos

Tenha o [Python](https://www.python.org/) instalado em sua máquina. Em seguida, instale o Flask:

```bash
pip install flask
```

> Recomenda-se utilizar um ambiente virtual para manter as dependências do projeto isoladas.

### Inicialização

Na raiz deste diretório, execute:

```bash
python static.py
```

O servidor será iniciado e os arquivos poderão ser acessados conforme as rotas definidas em `static.py`.

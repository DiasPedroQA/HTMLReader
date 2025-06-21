# HTMLReader

O HTMLReader é uma aplicação modular para leitura, análise e processamento de arquivos HTML e outros formatos de texto, com suporte a interface gráfica (Tkinter), linha de comando (CLI) e API (FastAPI). O projeto foi pensado para ser didático, organizado e fácil de evoluir, tanto para uso quanto para contribuições.

## Estrutura do Projeto

A estrutura do HTMLReader foi desenhada para separar claramente responsabilidades e facilitar testes, manutenção e extensibilidade:

- **src/core**: Lógica central do sistema, incluindo modelos (schemas Pydantic), serviços de processamento e utilitários.
  - **models**: Schemas e validações para arquivos, pastas e operações.
  - **services**: Funções de processamento, leitura, listagem e prévia de arquivos.
- **src/interfaces**: Pontos de entrada para interação do usuário.
  - **gui**: Interface gráfica baseada em Tkinter.
  - **cli**: Interface de linha de comando para uso via terminal.
  - **api**: Interface de API REST com FastAPI, incluindo rotas para operações de visor e processamento.
- **tests**: Testes automatizados para todos os módulos principais, garantindo robustez e exemplos de uso.
- **Makefile**: Comandos para facilitar instalação, testes, lint, formatação e execução.
- **requirements.txt / requirements-dev.txt**: Dependências de produção e desenvolvimento.

## Como rodar os testes

```bash
make test
```

ou diretamente:

```bash
pytest tests
```

## Como usar o HTMLReader

O HTMLReader pode ser utilizado de três formas principais:

- **GUI (Tkinter)**: Execute `make run` ou rode o módulo principal para abrir a interface gráfica, onde é possível selecionar pastas, visualizar arquivos e obter prévias de conteúdo.
- **CLI**: Use `python -m htmlreader.interfaces.cli.main_cli visor <caminho>` para visualizar arquivos/pastas ou `processar <arquivos>` para processar arquivos em lote.
- **API**: Suba a API com FastAPI (`uvicorn htmlreader.interfaces.api.main_api:app`) e acesse os endpoints REST para integração com outros sistemas ou automações.

### Recomendações

- Sempre utilize ambientes virtuais para instalar dependências.
- Consulte os testes automatizados para exemplos práticos de uso dos módulos.
- Leia os docstrings dos módulos para entender as funções e modelos disponíveis.
- Para contribuir, siga o padrão de organização e documentação do projeto.

---

O HTMLReader é um projeto pensado para ser acessível, modular e didático, servindo tanto para aprendizado quanto para aplicações reais de manipulação e análise de arquivos.

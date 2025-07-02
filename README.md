# HTMLReader

[![Build](https://github.com/DiasPedroQA/htmlreader/actions/workflows/tdd.yml/badge.svg)](https://github.com/DiasPedroQA/htmlreader/actions/workflows/tdd.yml)
[![Coverage](https://codecov.io/gh/DiasPedroQA/htmlreader/branch/main/graph/badge.svg)](https://codecov.io/gh/DiasPedroQA/htmlreader)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-linux--windows--macos-lightgrey)

![Docker Ready](https://img.shields.io/badge/docker-ready-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-orange)

**HTMLReader** é uma aplicação modular para leitura, análise e processamento de arquivos HTML e texto (como `.txt`, `.md`, etc.). Ele oferece suporte a três formas de interação:

- Interface Gráfica (GUI) com **Tkinter**
- Interface de Linha de Comando (CLI)
- Interface de API REST com **FastAPI**

O projeto é didático, extensível e fácil de manter — ideal para aprendizado e aplicações reais.

---

## 🧱 Estrutura do Projeto

A arquitetura segue boas práticas de camadas e separação de responsabilidades:

```text
HTMLReader/
├── src/
│   ├── core/               # Lógica central da aplicação
│   │   ├── models/         # Schemas Pydantic e modelos de dados
│   │   └── services/       # Regras de negócio, análise e utilitários
│   └── interfaces/         # Interfaces de interação com o usuário
│       ├── api/            # API REST com FastAPI
│       ├── cli/            # Interface de linha de comando
│       └── gui/            # Interface gráfica (Tkinter)
├── tests/                  # Testes automatizados com Pytest
├── Makefile                # Tarefas automatizadas
├── pyproject.toml          # Configurações de build, lint e testes
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação do projeto
````

---

## ▶️ Como Usar

### GUI (Interface Gráfica)

```bash
make run
# ou
python -m src.interfaces.gui.main_gui
```

---

### CLI (Linha de Comando)

```bash
python -m src.interfaces.cli.main_cli visor <CAMINHO>
python -m src.interfaces.cli.main_cli processar <ARQUIVOS>
```

---

### API REST (FastAPI)

```bash
uvicorn src.interfaces.api.main_api:src --reload
```

Acesse: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## ✅ Executando os Testes

```bash
make test
# ou
pytest tests
```

---

## 🧪 Boas Práticas para Desenvolvimento

```bash
python -m venv .venv && source .venv/bin/activate
```

```bash
make install
```

```bash
make lint
make format
```

---

## 🤝 Contribuindo

Pull requests são bem-vindos!

1. Faça um fork do repositório
2. Crie uma branch (`git checkout -b feature/nome`)
3. Execute `make test` e confirme que tudo está funcionando
4. Envie um pull request com descrição clara e objetiva

---

## 📝 Licença

Este projeto está licenciado sob os termos da licença [MIT](LICENSE).

---

> Projeto desenvolvido com foco didático e modular por [Pedro PM Dias](https://github.com/DiasPedroQA/HTMLReader).

## ✅ Estrutura sugerida para os badges

```markdown
# HTMLReader

<!-- Status Geral -->
[![Build](https://github.com/DiasPedroQA/htmlreader/actions/workflows/tdd.yml/badge.svg)](https://github.com/DiasPedroQA/htmlreader/actions/workflows/tdd.yml)
[![Coverage](https://codecov.io/gh/DiasPedroQA/htmlreader/branch/main/graph/badge.svg)](https://codecov.io/gh/DiasPedroQA/htmlreader)

<!-- Ambiente e Plataforma -->
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-linux--windows--macos-lightgrey)
![Docker Ready](https://img.shields.io/badge/docker-ready-blue)

<!-- Manutenção e Licença -->
![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-orange)
```

---

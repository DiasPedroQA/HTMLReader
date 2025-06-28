# HTMLReader

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

O **HTMLReader** é uma aplicação modular para leitura, análise e processamento de arquivos HTML e texto (como `.txt`, `.md`, etc.). Ele oferece suporte a três formas de interação:

- Interface Gráfica (GUI) com **Tkinter**
- Interface de Linha de Comando (CLI)
- Interface de API REST com **FastAPI**

O projeto foi pensado para ser didático, extensível e fácil de manter — ideal para aprendizado e aplicações reais.

---

## 🧱 Estrutura do Projeto

A organização do HTMLReader segue boas práticas de arquitetura em camadas e separação de responsabilidades:

```plain

HTMLReader/
├── src/
│   ├── core/               # Lógica central da aplicação
│   │   ├── models/         # Schemas Pydantic e modelos de dados
│   │   └── services/       # Regras de negócio, análise e utilitários
│   └── interfaces/         # Interfaces de interação com o usuário
│       ├── api/            # API REST com FastAPI
│       ├── cli/            # Interface de linha de comando
│       └── gui/            # Interface gráfica (Tkinter)
├── tests/                  # Testes automatizados com pytest
├── Makefile                # Tarefas automatizadas
├── pyproject.toml          # Configurações de build, lint e testes
├── requirements.txt        # Dependências de produção (pip-tools/Poetry)
└── README.md               # Documentação do projeto

```

---

## ▶️ Como Usar

### GUI (Interface Gráfica)

Abra a interface gráfica com:

```bash
make run
````

Ou diretamente:

```bash
python -m src.interfaces.gui.main_gui
```

---

### CLI (Linha de Comando)

Use os comandos disponíveis para executar operações diretamente via terminal:

```bash
python -m src.interfaces.cli.main_cli visor <CAMINHO>
python -m src.interfaces.cli.main_cli processar <ARQUIVOS>
```

---

### API REST (FastAPI)

Inicie o servidor com:

```bash
uvicorn src.interfaces.api.main_api:app --reload
```

Acesse a documentação automática em:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## ✅ Executando os Testes

Via Makefile:

```bash
make test
```

Ou diretamente com Pytest:

```bash
pytest tests
```

---

## 🧪 Recomendações para Desenvolvimento

- Use ambientes virtuais: `python -m venv .venv && source .venv/bin/activate`
- Execute `make install` para instalar dependências.
- Utilize `make lint` e `make format` para manter o código limpo.
- Consulte os testes automatizados como exemplos de uso.
- Leia o `docstring` e *type hints* para compreender os modelos e fluxos.

---

## 🤝 Contribuindo

Pull requests são bem-vindos! Para contribuir:

- Faça um fork do repositório
- Crie uma branch para sua feature ou correção
- Confirme se os testes passam com `make test`
- Envie um *pull request* com uma descrição clara

---

## 📝 Licença

Este projeto está licenciado sob os termos da licença [MIT](LICENSE).

---

> Projeto desenvolvido com foco didático e modular por [Pedro PM Dias](https://github.com/DiasPedroQA/HTMLReader).

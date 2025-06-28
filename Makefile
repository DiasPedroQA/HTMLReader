.PHONY: help venv install compile lint format test coverage coverage-html run-cli run-gui run-api clean all pre setup post

VENV = .venv/bin

help:
	@echo "Comandos disponíveis:"
	@echo "  make venv          - Cria ambiente virtual .venv"
	@echo "  make install       - Instala dependências (produção e dev)"
	@echo "  make compile       - Gera requirements.txt via pip-tools"
	@echo "  make lint          - Roda pylint e flake8"
	@echo "  make format        - Roda black e isort"
	@echo "  make test          - Executa testes com pytest"
	@echo "  make coverage      - Mostra cobertura de testes no terminal"
	@echo "  make coverage-html - Gera cobertura de testes em HTML"
	@echo "  make run-cli       - Executa a interface de linha de comando"
	@echo "  make run-gui       - Executa a interface gráfica"
	@echo "  make run-api       - Executa a API FastAPI"
	@echo "  make clean         - Remove arquivos temporários"
	@echo "  make all           - Executa pipeline completa"
	@echo "  make pre           - Executa pré-configuração (scripts/pre_setup.py)"
	@echo "  make setup         - Executa configuração principal (scripts/setup.py)"
	@echo "  make post          - Executa pós-configuração (scripts/post_setup.py)"

venv:
	python3 -m venv .venv

install: venv
	$(VENV)/pip install --upgrade pip
	@if [ -f requirements.txt ]; then \
		$(VENV)/pip install -r requirements.txt; \
	fi
	@if [ -f requirements-dev.txt ]; then \
		$(VENV)/pip install -r requirements-dev.txt; \
	fi

compile:
	$(VENV)/pip-compile requirements.in -o requirements.txt

lint:
	$(VENV)/pylint src/ tests || true
	$(VENV)/flake8 src/ tests || true

format:
	$(VENV)/black src/ tests/
	$(VENV)/isort src/ tests/

test:
	PYTHONPATH=src $(VENV)/pytest tests --maxfail=1 --disable-warnings -v

coverage:
	PYTHONPATH=src $(VENV)/pytest --cov=src tests --cov-report=term-missing

coverage-html:
	PYTHONPATH=src $(VENV)/pytest --cov=src tests --cov-report=html

run-cli:
	PYTHONPATH=src $(VENV)/python src/interfaces/cli/main_cli.py

run-gui:
	PYTHONPATH=src $(VENV)/python src/interfaces/gui/main_gui.py

run-api:
	PYTHONPATH=src $(VENV)/python src/interfaces/api/main_api.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov __pycache__ */__pycache__

# Pipeline completa: executa todas as etapas principais
all: clean venv install lint format test coverage-html
	@echo "✅ Pipeline completa executada com sucesso!"

# Scripts de configuração (pré, setup, pós)
pre:
	@echo "🔧 Executando pré-configuração..."
	@python3 scripts/pre_setup.py

setup: pre
	@echo "⚙️  Executando configuração principal..."
	@python3 scripts/setup.py

post: setup
	@echo "✅ Executando pós-configuração..."
	@python3 scripts/post_setup.py

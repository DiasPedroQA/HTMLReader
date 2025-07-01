.PHONY: help venv install compile lint format test coverage coverage-html tdd run-cli run-gui run-api clean all pre setup post

PYTHON := python3
VENV := .venv/bin
SRC := app
TESTS := tests

# ====================================
# AJUDA
# ====================================
help:
	@echo "Comandos disponíveis:"
	@echo "  make venv             - Cria ambiente virtual .venv"
	@echo "  make install          - Instala dependências (produção e dev)"
	@echo "  make compile          - Gera requirements.txt via pip-tools"
	@echo "  make lint             - Executa linters (ruff, mypy, isort)"
	@echo "  make format           - Aplica formatação (black, isort)"
	@echo "  make test             - Executa testes com pytest"
	@echo "  make coverage         - Mostra cobertura no terminal e gera XML"
	@echo "  make coverage-html    - Gera cobertura de testes em HTML"
	@echo "  make tdd              - Executa lint, testes e cobertura (modo TDD)"
	@echo "  make run-cli          - Executa interface de linha de comando"
	@echo "  make run-gui          - Executa interface gráfica (Tkinter)"
	@echo "  make run-api          - Executa API FastAPI"
	@echo "  make clean            - Remove arquivos temporários"
	@echo "  make all              - Executa pipeline completa"
	@echo "  make pre/setup/post   - Executa scripts de configuração modular"

# ====================================
# AMBIENTE VIRTUAL E DEPENDÊNCIAS
# ====================================
venv:
	$(PYTHON) -m venv .venv

install: venv
	$(VENV)/pip install --upgrade pip
	@if [ -f requirements.txt ]; then $(VENV)/pip install -r requirements.txt; fi
	@if [ -f requirements-dev.txt ]; then $(VENV)/pip install -r requirements-dev.txt; fi

compile:
	$(VENV)/pip-compile requirements.in -o requirements.txt

# ====================================
# LINT E FORMATAÇÃO
# ====================================
lint:
	$(VENV)/ruff . --output-format=github
	$(VENV)/mypy $(SRC)
	$(VENV)/isort . --check-only --profile black

format:
	$(VENV)/black .
	$(VENV)/isort . --profile black

# ====================================
# TESTES E COBERTURA
# ====================================
test:
	PYTHONPATH=$(SRC) $(VENV)/pytest $(TESTS) --maxfail=1 --disable-warnings -v

coverage:
	PYTHONPATH=$(SRC) $(VENV)/pytest --cov=$(SRC) $(TESTS) --cov-report=term-missing --cov-report=xml

coverage-html:
	PYTHONPATH=$(SRC) $(VENV)/pytest --cov=$(SRC) $(TESTS) --cov-report=html

tdd: lint test coverage

# ====================================
# EXECUÇÃO DAS INTERFACES
# ====================================
run-cli:
	PYTHONPATH=$(SRC) $(VENV)/python $(SRC)/interfaces/cli/main_cli.py

run-gui:
	PYTHONPATH=$(SRC) $(VENV)/python $(SRC)/interfaces/gui/main_gui.py

run-api:
	PYTHONPATH=$(SRC) $(VENV)/python $(SRC)/interfaces/api/main_api.py

# ====================================
# LIMPEZA
# ====================================
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov coverage.xml __pycache__ */__pycache__

# ====================================
# PIPELINE COMPLETA
# ====================================
all: clean venv install format lint test coverage-html
	@echo "✅ Pipeline completa executada com sucesso!"

# ====================================
# SCRIPTS DE CONFIGURAÇÃO MODULAR
# ====================================
pre:
	@echo "🔧 Executando pré-configuração..."
	@$(PYTHON) scripts/pre_setup.py

setup: pre
	@echo "⚙️  Executando configuração principal..."
	@$(PYTHON) scripts/setup.py

post: setup
	@echo "✅ Executando pós-configuração..."
	@$(PYTHON) scripts/post_setup.py

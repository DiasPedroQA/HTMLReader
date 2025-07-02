.PHONY: help venv install compile lint format test coverage coverage-html tdd run-cli run-gui run-api clean all pre setup post

# Variáveis principais
VENV_PATH := app-tkinter-venv
PYTHON := $(VENV_PATH)/bin/python
PIP := $(VENV_PATH)/bin/pip
PIP_COMPILE := $(VENV_PATH)/bin/pip-compile
PYTEST := $(VENV_PATH)/bin/pytest
RUFF := $(VENV_PATH)/bin/ruff
# MYPY := $(VENV_PATH)/bin/mypy
ISORT := $(VENV_PATH)/bin/isort
BLACK := $(VENV_PATH)/bin/black
SRC := src
TESTS := tests


# ====================================
# AJUDA
# ====================================
help:
	@echo "Comandos disponíveis:"
	@echo "  make venv             - Cria ambiente virtual (app-tkinter-venv)"
	@echo "  make install          - Instala dependências"
	@echo "  make compile          - Gera requirements*.txt via pip-tools"
	@echo "  make lint             - Executa ruff, mypy e isort"
	@echo "  make format           - Formata com black e isort"
	@echo "  make test             - Executa testes com pytest"
	@echo "  make coverage         - Gera cobertura (terminal + XML)"
	@echo "  make coverage-html    - Gera relatório de cobertura em HTML"
	@echo "  make tdd              - Executa TDD completo"
	@echo "  make run-cli          - Executa CLI"
	@echo "  make run-gui          - Executa GUI"
	@echo "  make run-api          - Executa API"
	@echo "  make clean            - Remove arquivos temporários"
	@echo "  make all              - Pipeline completa"
	@echo "  make pre/setup/post   - Scripts de configuração modular"

# ====================================
# AMBIENTE VIRTUAL E DEPENDÊNCIAS
# ====================================
venv:
	@python3 -m venv $(VENV_PATH)
	@echo "Ambiente virtual criado em $(VENV_PATH)"

install:
	@echo "Usando pip: $(PIP)"
	@$(PIP) install --upgrade pip --break-system-packages
	@if [ -f requirements.txt ]; then $(PIP) install -r requirements.txt --break-system-packages; fi
	@if [ -f requirements-dev.txt ]; then $(PIP) install -r requirements-dev.txt --break-system-packages; fi

compile:
	@$(PIP) install pip-tools --break-system-packages
	@$(PIP_COMPILE) requirements.in --output-file=requirements.txt
	@$(PIP_COMPILE) requirements-dev.in --output-file=requirements-dev.txt

# ====================================
# LINT E FORMATAÇÃO
# ====================================
lint:
	$(RUFF) check .
	# PYTHONPATH=src $(MYPY) src/core
	$(ISORT) . --check-only --profile black

format:
	$(BLACK) .
	$(ISORT) . --profile black

# ====================================
# TESTES E COBERTURA
# ====================================
test:
	PYTHONPATH=$(SRC) $(PYTEST) $(TESTS) --maxfail=1 --disable-warnings -v

coverage:
	PYTHONPATH=$(SRC) $(PYTEST) --cov=$(SRC) $(TESTS) --cov-report=term-missing --cov-report=xml

coverage-html:
	PYTHONPATH=$(SRC) $(PYTEST) --cov=$(SRC) $(TESTS) --cov-report=html

tdd: lint test coverage

# ====================================
# EXECUÇÃO DAS INTERFACES
# ====================================
run-cli:
	PYTHONPATH=$(SRC) $(PYTHON) $(SRC)/interfaces/cli/main_cli.py

run-gui:
	PYTHONPATH=$(SRC) $(PYTHON) $(SRC)/interfaces/gui/main_gui.py

run-api:
	PYTHONPATH=$(SRC) $(PYTHON) $(SRC)/interfaces/api/main_api.py

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
all: clean venv install compile format lint test coverage coverage-html tdd help
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

.PHONY: help venv install install compile lint format test coverage coverage-html clean run run-cli run-gui run-api all

VENV = .venv/bin

help:
	@echo "Comandos disponíveis:"
	@echo "  make venv          - Cria ambiente virtual .venv"
	@echo "  make install       - Instala dependências (produção e dev)"
	@echo "  make compile       - Gera requirements.txt e requirements.txt via pip-tools"
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

venv:
	python3 -m venv .venv


install:
	$(VENV)/pip install -r requirements.txt

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
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov

all: clean venv install lint format test coverage-html
	@echo "✅ Pipeline completa executada com sucesso!"

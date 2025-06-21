.PHONY: help venv install lint format test clean

help:
	@echo "Comandos disponíveis:"
	@echo "  make venv      - Cria ambiente virtual .venv"
	@echo "  make install   - Instala dependências no .venv"
	@echo "  make lint      - Roda pylint e flake8"
	@echo "  make format    - Roda black e isort"
	@echo "  make test      - Executa todos os testes com pytest"
	@echo "  make clean     - Remove arquivos temporários e __pycache__"
	@echo "  make run       - Roda a aplicação principal"

venv:
	python3 -m venv .venv

install: venv
	.venv/bin/pip install --upgrade pip
	@if [ -f requirements.txt ]; then \
		.venv/bin/pip install -r requirements.txt; \
	fi
	@if [ -f requirements-dev.txt ]; then \
		.venv/bin/pip install -r requirements-dev.txt; \
	fi

lint:
	.venv/bin/pylint src/ tests || true
	.venv/bin/flake8 src/ tests || true

format:
	.venv/bin/black src/ tests/
	.venv/bin/isort src/ tests/

test:
	PYTHONPATH=src .venv/bin/pytest tests --maxfail=1 --disable-warnings -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov

run:
	PYTHONPATH=src .venv/bin/python -m src

coverage-html:
	PYTHONPATH=src .venv/bin/pytest --cov=src tests --cov-report=html

all: clean venv install lint format test coverage-html
	@echo "Pipeline completa executada com sucesso!"

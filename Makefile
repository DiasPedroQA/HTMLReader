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
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install -r requirements-dev.txt || true

lint:
	.venv/bin/pylint src/htmlreader src/tests || true
	.venv/bin/flake8 src/htmlreader src/tests || true

format:
	.venv/bin/black src/ src/tests/
	.venv/bin/isort src/ src/tests/

test:
	PYTHONPATH=src .venv/bin/pytest src/tests --maxfail=1 --disable-warnings -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov

run:
	.venv/bin/python -m htmlreader

coverage-html:
	PYTHONPATH=src .venv/bin/pytest --cov=htmlreader src/tests --cov-report=html

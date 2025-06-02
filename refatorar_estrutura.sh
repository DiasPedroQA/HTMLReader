#!/bin/bash

set -e

echo "🔄 Navegando para o diretório do projeto..."
cd "$(dirname "$0")"

echo "📁 Criando diretórios das interfaces (CLI e GUI)..."
mkdir -p src/htmlreader/interfaces/{cli,gui,api}

echo "📁 Movendo arquivos existentes, se houver..."
[ -f src/htmlreader/backend/cli.py ] && mv src/htmlreader/backend/cli.py src/htmlreader/interfaces/cli/
[ -f src/htmlreader/frontend/gui.py ] && mv src/htmlreader/frontend/gui.py src/htmlreader/interfaces/gui/

echo "🧹 Limpando diretórios antigos se estiverem vazios..."
[ -d src/htmlreader/backend ] && rmdir --ignore-fail-on-non-empty src/htmlreader/backend
[ -d src/htmlreader/frontend ] && rmdir --ignore-fail-on-non-empty src/htmlreader/frontend

echo "📁 Criando estrutura de core e interfaces, se necessário..."
mkdir -p src/htmlreader/core/{models,services,utils}
mkdir -p src/htmlreader/interfaces/{cli,gui,api}
mkdir -p src/tests/core/{models,services,utils}
mkdir -p src/tests/interfaces/{cli,gui,api}

echo "📄 Criando arquivos __init__.py..."
touch src/htmlreader/__init__.py
touch src/htmlreader/core/__init__.py
touch src/htmlreader/core/models/__init__.py
touch src/htmlreader/core/services/__init__.py
touch src/htmlreader/core/utils/__init__.py
touch src/htmlreader/interfaces/__init__.py
touch src/htmlreader/interfaces/cli/__init__.py
touch src/htmlreader/interfaces/gui/__init__.py
touch src/htmlreader/interfaces/api/__init__.py
touch src/tests/__init__.py
touch src/tests/core/__init__.py
touch src/tests/core/models/__init__.py
touch src/tests/core/services/__init__.py
touch src/tests/core/utils/__init__.py
touch src/tests/interfaces/__init__.py
touch src/tests/interfaces/cli/__init__.py
touch src/tests/interfaces/gui/__init__.py
touch src/tests/interfaces/api/__init__.py

echo "✅ Estrutura reorganizada com sucesso."

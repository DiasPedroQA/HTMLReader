#!/bin/bash

# Script para refatorar e organizar a estrutura do projeto HTMLReader

set -e

echo "🔧 Criando estrutura de diretórios..."

# Diretórios principais
mkdir -p src/core/{models,services,controllers}
mkdir -p src/interfaces/{api/routes,cli,gui/widgets}
mkdir -p tests/core/{models,services,controllers}
mkdir -p tests/interfaces/{api/routes,cli,gui}

echo "📂 Estrutura de diretórios criada com sucesso."

echo "🚚 Movendo arquivos para a nova estrutura (se existirem)..."

# Mover arquivos de models
mv -v src/core/models/{exceptions.py,processador_models.py,visor_models.py} src/core/models/ 2>/dev/null || true

# Mover arquivos de services
mv -v src/core/services/{processador_service.py,visor_service.py,system_services.py} src/core/services/ 2>/dev/null || true

# Mover arquivos da API
mv -v src/interfaces/api/{main_api.py,__init__.py} src/interfaces/api/ 2>/dev/null || true
mv -v src/interfaces/api/routes/{processador_routes.py,visor_routes.py,__init__.py} src/interfaces/api/routes/ 2>/dev/null || true

# Mover arquivos da CLI
mv -v src/interfaces/cli/{main_cli.py,__init__.py} src/interfaces/cli/ 2>/dev/null || true

# Mover arquivos da GUI
mv -v src/interfaces/gui/{main_gui.py,__init__.py} src/interfaces/gui/ 2>/dev/null || true

# Mover arquivos de testes
mv -v tests/core/models/{test_directory_model.py,test_file_model.py} tests/core/models/ 2>/dev/null || true
mv -v tests/core/services/test_*.py tests/core/services/ 2>/dev/null || true

echo "✅ Refatoração e organização concluídas com sucesso!"

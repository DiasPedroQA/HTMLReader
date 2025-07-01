#!/bin/bash

# Script para refatorar e organizar a estrutura do projeto HTMLReader

set -e

echo "🔧 Criando estrutura de diretórios..."

# Diretórios principais
mkdir -p app/core/{models,services,controllers}
mkdir -p app/interfaces/{api/routes,cli,gui/widgets}
mkdir -p tests/core/{models,services,controllers}
mkdir -p tests/interfaces/{api/routes,cli,gui}

echo "📂 Estrutura de diretórios criada com sucesso."

echo "🚚 Movendo arquivos para a nova estrutura (se existirem)..."

# Mover arquivos de models
mv -v app/core/models/{exceptions.py,processador_models.py,visor_models.py} app/core/models/ 2>/dev/null || true

# Mover arquivos de services
mv -v app/core/services/{processador_service.py,visor_service.py,system_services.py} app/core/services/ 2>/dev/null || true

# Mover arquivos da API
mv -v app/interfaces/api/{main_api.py,__init__.py} app/interfaces/api/ 2>/dev/null || true
mv -v app/interfaces/api/routes/{processador_routes.py,visor_routes.py,__init__.py} app/interfaces/api/routes/ 2>/dev/null || true

# Mover arquivos da CLI
mv -v app/interfaces/cli/{main_cli.py,__init__.py} app/interfaces/cli/ 2>/dev/null || true

# Mover arquivos da GUI
mv -v app/interfaces/gui/{main_gui.py,__init__.py} app/interfaces/gui/ 2>/dev/null || true

# Mover arquivos de testes
mv -v tests/core/models/{test_directory_model.py,test_file_model.py} tests/core/models/ 2>/dev/null || true
mv -v tests/core/services/test_*.py tests/core/services/ 2>/dev/null || true

echo "✅ Refatoração e organização concluídas com sucesso!"

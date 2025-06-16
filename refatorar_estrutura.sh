#!/bin/bash

# Script para refatorar e organizar a estrutura do projeto HTMLReader

set -e

echo "Criando estrutura de diretórios..."

mkdir -p src/core/models
mkdir -p src/core/services
mkdir -p src/core/utils
mkdir -p src/interfaces/api/routes
mkdir -p src/interfaces/cli
mkdir -p src/interfaces/gui
mkdir -p src/tests/core/models
mkdir -p src/tests/core/services
mkdir -p src/tests/core/utils

echo "Movendo arquivos para a nova estrutura..."

# Core models
mv src/core/models/__init__.py src/core/models/__init__.py 2>/dev/null || true
mv src/core/models/exceptions.py src/core/models/exceptions.py 2>/dev/null || true
mv src/core/models/processador_models.py src/core/models/processador_models.py 2>/dev/null || true
mv src/core/models/visor_models.py src/core/models/visor_models.py 2>/dev/null || true

# Core services
mv src/core/services/__init__.py src/core/services/__init__.py 2>/dev/null || true
mv src/core/services/processador_service.py src/core/services/processador_service.py 2>/dev/null || true
mv src/core/services/visor_service.py src/core/services/visor_service.py 2>/dev/null || true

# Core utils
mv src/core/utils/__init__.py src/core/utils/__init__.py 2>/dev/null || true
mv src/core/utils/system_utils.py src/core/utils/system_utils.py 2>/dev/null || true

# Interfaces API
mv src/interfaces/api/__init__.py src/interfaces/api/__init__.py 2>/dev/null || true
mv src/interfaces/api/main_api.py src/interfaces/api/main_api.py 2>/dev/null || true
mv src/interfaces/api/routes/__init__.py src/interfaces/api/routes/__init__.py 2>/dev/null || true
mv src/interfaces/api/routes/processador_routes.py src/interfaces/api/routes/processador_routes.py 2>/dev/null || true
mv src/interfaces/api/routes/visor_routes.py src/interfaces/api/routes/visor_routes.py 2>/dev/null || true

# Interfaces CLI
mv src/interfaces/cli/__init__.py src/interfaces/cli/__init__.py 2>/dev/null || true
mv src/interfaces/cli/main_cli.py src/interfaces/cli/main_cli.py 2>/dev/null || true

# Interfaces GUI
mv src/interfaces/gui/__init__.py src/interfaces/gui/__init__.py 2>/dev/null || true
mv src/interfaces/gui/main_gui.py src/interfaces/gui/main_gui.py 2>/dev/null || true

# Testes
mv src/tests/core/models/test_directory_model.py src/tests/core/models/test_directory_model.py 2>/dev/null || true
mv src/tests/core/models/test_file_model.py src/tests/core/models/test_file_model.py 2>/dev/null || true
mv src/tests/core/services/test_text_analysis_service.py src/tests/core/services/test_text_analysis_service.py 2>/dev/null || true
mv src/tests/core/services/test_text_file_service.py src/tests/core/services/test_text_file_service.py 2>/dev/null || true
mv src/tests/core/utils/test_encoding_utils.py src/tests/core/utils/test_encoding_utils.py 2>/dev/null || true
mv src/tests/core/utils/test_file_utils.py src/tests/core/utils/test_file_utils.py 2>/dev/null || true
mv src/tests/core/utils/test_path_utils.py src/tests/core/utils/test_path_utils.py 2>/dev/null || true
mv src/tests/core/utils/test_system_utils.py src/tests/core/utils/test_system_utils.py 2>/dev/null || true

echo "Estrutura refatorada com sucesso!"


#!/bin/bash

# Script para refatorar e organizar a estrutura do projeto HTMLReader

set -e

echo "Criando estrutura de diretórios..."

mkdir -p src/htmlreader/core/models
mkdir -p src/htmlreader/core/services
mkdir -p src/htmlreader/core/utils
mkdir -p src/htmlreader/interfaces/api/routes
mkdir -p src/htmlreader/interfaces/cli
mkdir -p src/htmlreader/interfaces/gui
mkdir -p src/tests/core/models
mkdir -p src/tests/core/services
mkdir -p src/tests/core/utils

echo "Movendo arquivos para a nova estrutura..."

# Core models
mv src/htmlreader/core/models/__init__.py src/htmlreader/core/models/__init__.py 2>/dev/null || true
mv src/htmlreader/core/models/exceptions.py src/htmlreader/core/models/exceptions.py 2>/dev/null || true
mv src/htmlreader/core/models/processador_models.py src/htmlreader/core/models/processador_models.py 2>/dev/null || true
mv src/htmlreader/core/models/visor_models.py src/htmlreader/core/models/visor_models.py 2>/dev/null || true

# Core services
mv src/htmlreader/core/services/__init__.py src/htmlreader/core/services/__init__.py 2>/dev/null || true
mv src/htmlreader/core/services/processador_service.py src/htmlreader/core/services/processador_service.py 2>/dev/null || true
mv src/htmlreader/core/services/visor_service.py src/htmlreader/core/services/visor_service.py 2>/dev/null || true

# Core utils
mv src/htmlreader/core/utils/__init__.py src/htmlreader/core/utils/__init__.py 2>/dev/null || true
mv src/htmlreader/core/utils/system_utils.py src/htmlreader/core/utils/system_utils.py 2>/dev/null || true

# Interfaces API
mv src/htmlreader/interfaces/api/__init__.py src/htmlreader/interfaces/api/__init__.py 2>/dev/null || true
mv src/htmlreader/interfaces/api/main_api.py src/htmlreader/interfaces/api/main_api.py 2>/dev/null || true
mv src/htmlreader/interfaces/api/routes/__init__.py src/htmlreader/interfaces/api/routes/__init__.py 2>/dev/null || true
mv src/htmlreader/interfaces/api/routes/processador_routes.py src/htmlreader/interfaces/api/routes/processador_routes.py 2>/dev/null || true
mv src/htmlreader/interfaces/api/routes/visor_routes.py src/htmlreader/interfaces/api/routes/visor_routes.py 2>/dev/null || true

# Interfaces CLI
mv src/htmlreader/interfaces/cli/__init__.py src/htmlreader/interfaces/cli/__init__.py 2>/dev/null || true
mv src/htmlreader/interfaces/cli/main_cli.py src/htmlreader/interfaces/cli/main_cli.py 2>/dev/null || true

# Interfaces GUI
mv src/htmlreader/interfaces/gui/__init__.py src/htmlreader/interfaces/gui/__init__.py 2>/dev/null || true
mv src/htmlreader/interfaces/gui/main_gui.py src/htmlreader/interfaces/gui/main_gui.py 2>/dev/null || true

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


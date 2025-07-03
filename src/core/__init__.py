"""
Pacote core - Funcionalidades centrais do sistema.

Exporta:
    - models: Todos os modelos de dados
    - utils: Utilitários do sistema
    - constants: Constantes globais
"""

# Configuração inicial
import logging

from src.core.controllers import arquivos_controller
from src.core.controllers import info_sistema_controller
from src.core.controllers import pastas_controller
from src.core.controllers import sistema_controller
from src.core.models.arquivo import arquivo_model
from src.core.models.arquivo import tipos_model
from src.core.models.pasta import pasta_model
from src.core.models.sistema import sistema_info_model
from src.core.models.sistema import sistema_operacional_model
from src.core.models.sistema import tipos_comuns_model
from src.core.utils.exceptions import file_exceptions
from src.core.utils.filesystem.detectores import sistema_operacional
from src.core.utils.filesystem.metadados import coletor_permissoes
from src.core.utils.filesystem.metadados import coletor_tempos
from src.core.utils.filesystem.metadados import gerador_metadados


__all__ = [
    "arquivos_controller",
    "info_sistema_controller",
    "pastas_controller",
    "sistema_controller",
    "arquivo_model",
    "tipos_model",
    "pasta_model",
    "sistema_info_model",
    "sistema_operacional_model",
    "tipos_comuns_model",
    "file_exceptions",
    "sistema_operacional",
    "coletor_permissoes",
    "coletor_tempos",
    "gerador_metadados",
]

logging.basicConfig(level=logging.INFO)

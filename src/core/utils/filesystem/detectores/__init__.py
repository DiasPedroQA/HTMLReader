"""
Módulo de detecção de ambiente do sistema operacional.

Exporta:
    - DetectorSO: Classe principal com métodos estáticos para detecção
    - SistemaOperacionalDetectado: Estrutura de dados contendo os dados detectados
    - Constantes úteis para identificação rápida do SO
"""

from .sistema_operacional import DetectorSO, SistemaOperacionalDetectado

__all__ = [
    "DetectorSO",
    "SistemaOperacionalDetectado",
]

SISTEMA_LINUX = "linux"
SISTEMA_WINDOWS = "windows"
SISTEMA_MAC = "darwin"

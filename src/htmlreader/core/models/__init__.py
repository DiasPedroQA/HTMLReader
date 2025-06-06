"""
Pacote de modelos (schemas) do HTMLReader.

Importa e expõe os principais modelos para facilitar o acesso em outros módulos.
"""

from src.htmlreader.core.models.objects_models import (
    Arquivo,
    CaminhoBruto,
    CaminhoInvalido,
    CaminhoValido,
    Pasta
)

__all__: list[str] = [
    "CaminhoBruto",
    "CaminhoValido",
    "CaminhoInvalido",
    "Arquivo",
    "Pasta",
]

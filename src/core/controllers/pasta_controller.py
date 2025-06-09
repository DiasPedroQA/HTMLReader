from core.models.pasta_models import Pasta
from core.services.pasta_service import PastaService


class PastaController:
    @staticmethod
    def carregar_pasta(caminho: str) -> Pasta:
        """Controla a criação da estrutura da pasta a partir de um caminho."""
        construtor = PastaService()
        return construtor.construir_estrutura_pasta(caminho=caminho)

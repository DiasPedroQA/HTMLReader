# from core.services.conversor_html import ConversorHTMLService
from core.models.pasta_models import Pasta
from core.services.pasta_service import PastaService


class ProcessadorService:
    @staticmethod
    def processar_pasta(caminho_pasta: str) -> Pasta:
        pasta = PastaService.listar_pasta(caminho_pasta)
        # Aqui poderia chamar o conversor para arquivos HTML encontrados, por exemplo.
        return pasta

from core.services.conversor_html import ConversorHTMLService
from core.models.conversao_models import ResultadoConversao
from core.utils.file_utils import ler_arquivo_html


class ConversaoController:
    @staticmethod
    def converter_html_para_json(caminho_html: str) -> ResultadoConversao:
        """Controla o fluxo de conversão de um arquivo HTML para JSON."""
        conteudo = ler_arquivo_html(caminho_html)
        conversor = ConversorHTMLService()
        resultado = conversor.converter_arquivo_html(conteudo, caminho_html)
        return resultado

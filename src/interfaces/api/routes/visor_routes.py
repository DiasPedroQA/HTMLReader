from fastapi import APIRouter
from core.controllers.file_path_controller import listar_arquivos_html

visor_router = APIRouter()


@visor_router.get("/conteudo-arquivo")
def obter_conteudo_arquivo(caminho: str) -> list[str]:
    """
    Retorna o conteúdo completo de um arquivo.
    """
    result = listar_arquivos_html(caminho)
    if not isinstance(result, list) or not all(isinstance(item, str) for item in result):
        raise TypeError("Expected a list of strings as return value")
    return result

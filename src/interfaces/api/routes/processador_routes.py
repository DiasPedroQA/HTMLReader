from fastapi import APIRouter
from core.controllers.file_path_controller import listar_arquivos_html

processador_router = APIRouter()


@processador_router.get("/listar-arquivos")
def listar_arquivos_em_pasta(caminho: str) -> list[str]:
    """
    Lista arquivos com determinada extensão em uma pasta.
    """
    result = listar_arquivos_html(caminho)
    if not isinstance(result, list) or not all(isinstance(item, str) for item in result):
        raise TypeError("Expected a list of strings as return value")
    return result

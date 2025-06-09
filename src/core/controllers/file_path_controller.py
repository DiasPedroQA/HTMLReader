import os
from core.utils.system_utils import eh_diretorio_valido, eh_arquivo_html


def listar_arquivos_html(diretorio: str) -> list[str]:
    """Retorna todos os arquivos HTML válidos no diretório fornecido."""
    if not eh_diretorio_valido(diretorio):
        raise ValueError(f"Diretório inválido: {diretorio}")

    arquivos = []
    for nome_arquivo in os.listdir(diretorio):
        caminho = os.path.join(diretorio, nome_arquivo)
        if os.path.isfile(caminho) and eh_arquivo_html(caminho):
            arquivos.append(caminho)
    return arquivos

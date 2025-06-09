import os


def listar_arquivos(diretorio: str, extensoes: list[str] | None = None) -> list[str]:
    """
    Lista arquivos em um diretório, filtrando por extensões se fornecidas.

    Args:
        diretorio (str): Caminho do diretório.
        extensoes (list[str], optional): Extensões dos arquivos, ex: ['.html', '.txt'].

    Returns:
        list[str]: Lista de caminhos completos dos arquivos encontrados.
    """
    arquivos: list[str] = []
    for root, _, files in os.walk(diretorio):
        for file in files:
            if extensoes is None or any(
                file.lower().endswith(ext.lower()) for ext in extensoes
            ):
                arquivos.append(os.path.join(root, file))
    return arquivos


def criar_diretorio_se_nao_existir(caminho: str) -> None:
    """
    Cria um diretório se ele não existir.

    Args:
        caminho (str): Caminho do diretório.
    """
    os.makedirs(caminho, exist_ok=True)


def ler_arquivo_html(caminho: str, encoding: str = "utf-8") -> str:
    """
    Lê e retorna o conteúdo de um arquivo de texto.

    Args:
        caminho (str): Caminho completo do arquivo.
        encoding (str, optional): Codificação do arquivo. Padrão: 'utf-8'.

    Returns:
        str: Conteúdo do arquivo como string.
    """
    with open(caminho, "r", encoding=encoding) as f:
        return f.read()

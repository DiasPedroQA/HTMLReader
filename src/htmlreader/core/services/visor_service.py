"""
Serviços para o visor de arquivos e pastas do HTMLReader.

Inclui funções para listar o conteúdo de diretórios e obter prévias de arquivos.
"""

from pathlib import Path

from src.htmlreader.core.models.visor_models import (
    FiltroVisor,
    ItemDePasta,
    ListaDeItens,
    PreviaArquivo,
)


def listar_conteudo(
    caminho: Path, filtros: FiltroVisor = FiltroVisor()
) -> ListaDeItens:
    """
    Lista o conteúdo de um diretório, aplicando filtros de tipo e extensão.

    Args:
        caminho (Path): Caminho do diretório a ser listado.
        filtros (FiltroVisor, opcional): Filtros para tipo e extensões.

    Returns:
        ListaDeItens: Lista dos itens encontrados no diretório.
    """
    itens = []
    for item in caminho.iterdir():
        if filtros.tipo and filtros.tipo == "arquivo" and item.is_dir():
            continue
        if filtros.tipo and filtros.tipo == "pasta" and item.is_file():
            continue
        if filtros.extensoes and item.suffix not in filtros.extensoes:
            continue
        itens.append(
            ItemDePasta(
                nome=item.name, path=item, tipo="arquivo" if item.is_file() else "pasta"
            )
        )
    return ListaDeItens(itens=itens)


def obter_previa(caminho: Path) -> PreviaArquivo:
    """
    Obtém uma prévia de um arquivo, incluindo nome, extensão, tamanho,
    data de modificação e primeiras linhas.

    Args:
        caminho (Path): Caminho do arquivo.

    Returns:
        PreviaArquivo: Dados resumidos e linhas iniciais do arquivo.
    """
    with open(caminho, "r", encoding="utf-8") as f:
        linhas = [next(f).rstrip() for _ in range(50)]
    stat = caminho.stat()
    return PreviaArquivo(
        nome=caminho.name,
        extensao=caminho.suffix,
        tamanho_bytes=stat.st_size,
        modificado_em=str(stat.st_mtime),
        linhas=linhas,
    )

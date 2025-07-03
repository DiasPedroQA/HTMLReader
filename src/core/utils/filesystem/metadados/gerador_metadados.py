"""
Gerador principal para coleta completa de metadados de arquivos e diretórios.

Integra informações básicas, permissões, timestamps e dados específicos do tipo.
"""

from pathlib import Path
from typing import Union, Dict, Any

from src.core.utils.exceptions.file_exceptions import FileAccessError
from src.core.models.sistema.tipos_comuns_model import MetadadosArquivo
from .coletor_permissoes import coletar_permissoes
from .coletor_tempos import coletar_tempos


def coletar_info_basica(caminho: Path) -> Dict[str, Any]:
    """
    Coleta metadados básicos comuns a arquivos e diretórios.

    Args:
        caminho (Path): Caminho a ser analisado.

    Returns:
        Dict[str, Any]: Dicionário com metadados básicos.
    """
    stats = caminho.stat()
    return {
        "nome": caminho.name,
        "caminho_absoluto": str(caminho.absolute()),
        "caminho_pai": str(caminho.parent),
        "tamanho_bytes": stats.st_size,
        "eh_oculto": caminho.name.startswith("."),
        "dispositivo": stats.st_dev,
        "proprietario": {"uid": stats.st_uid, "gid": stats.st_gid},
    }


def gerar_dados_item(caminho: Union[str, Path]) -> MetadadosArquivo:
    """
    Gera metadados completos para um arquivo ou diretório.

    Args:
        caminho (Union[str, Path]): Caminho do item a ser analisado.

    Returns:
        MetadadosArquivo: Metadados completos do item.

    Raises:
        FileAccessError: Se o item não existir ou não puder ser acessado.
    """
    try:
        path = Path(caminho)
        if not path.exists():
            raise FileAccessError("Item não encontrado", str(caminho))

        base = coletar_info_basica(path)
        base.update(coletar_tempos(path))
        base["permissoes"] = coletar_permissoes(path)

        if path.is_file():
            base["tipo"] = "arquivo"
            base["extensao"] = path.suffix.lower()
            base["extensao_legivel"] = path.suffix[1:].upper() if path.suffix else ""
        elif path.is_dir():
            base["tipo"] = "pasta"

        return base
    except Exception as e:
        raise FileAccessError("Falha ao gerar metadados", str(caminho), e) from e

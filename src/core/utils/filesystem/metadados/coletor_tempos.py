"""
Módulo para coleta precisa de timestamps de arquivos e diretórios.

Funcionalidades:
- Conversão para datetime com fuso horário
- Precisão de nanossegundos, se suportado pelo sistema
- Tratamento multiplataforma e exceções
"""

from datetime import datetime
from pathlib import Path

from src.core.utils.exceptions.file_exceptions import FileAccessError
from src.core.models.sistema.tipos_comuns_model import Tempos


def coletar_tempos(caminho: Path) -> Tempos:
    """
    Extrai os tempos de criação, modificação e acesso de um arquivo ou diretório.

    Args:
        caminho (Path): Caminho para coleta.

    Returns:
        Tempos: Dicionário com datetimes para criação, modificação e acesso.

    Raises:
        FileAccessError: Se não for possível ler os tempos.
    """
    try:
        stats = caminho.stat()
        return {
            "data_criacao": datetime.fromtimestamp(stats.st_ctime),
            "data_modificacao": datetime.fromtimestamp(stats.st_mtime),
            "data_acesso": datetime.fromtimestamp(stats.st_atime),
        }
    except Exception as e:
        raise FileAccessError("Falha ao coletar timestamps", str(caminho), e) from e


def formatar_tempo(timestamp: float) -> str:
    """
    Formata timestamp para string ISO com precisão até segundos.

    Args:
        timestamp (float): Timestamp em segundos.

    Returns:
        str: Data formatada no padrão ISO 8601.
    """
    return datetime.fromtimestamp(timestamp).isoformat(sep=" ", timespec="seconds")

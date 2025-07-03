"""
Módulo para extração e processamento de permissões de arquivos e diretórios.

Funcionalidades:
- Leitura das permissões POSIX/Windows
- Máscaras de bits para usuário, grupo e outros
- Conversão para estrutura padronizada para uso no sistema
"""

import stat
from pathlib import Path

from src.core.utils.exceptions.file_exceptions import FileAccessError
from src.core.models.sistema.tipos_comuns_model import PermissoesDetalhadas


def coletar_permissoes(caminho: Path) -> PermissoesDetalhadas:
    """
    Coleta permissões detalhadas de um arquivo ou diretório.

    Args:
        caminho (Path): Caminho do arquivo ou diretório.

    Returns:
        PermissoesDetalhadas: Dicionário com permissões para usuário, grupo e outros.

    Raises:
        FileAccessError: Se não for possível acessar as permissões.
    """
    try:
        modo = caminho.stat().st_mode
        return {
            "usuario": {
                "ler": bool(modo & stat.S_IRUSR),
                "escrever": bool(modo & stat.S_IWUSR),
                "executar": bool(modo & stat.S_IXUSR),
            },
            "grupo": {
                "ler": bool(modo & stat.S_IRGRP),
                "escrever": bool(modo & stat.S_IWGRP),
                "executar": bool(modo & stat.S_IXGRP),
            },
            "outros": {
                "ler": bool(modo & stat.S_IROTH),
                "escrever": bool(modo & stat.S_IWOTH),
                "executar": bool(modo & stat.S_IXOTH),
            },
        }
    except Exception as e:
        raise FileAccessError("Falha ao coletar permissões", str(caminho), e) from e

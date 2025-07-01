"""
Utilitários para extração e formatação de metadados de arquivos e diretórios.

Este módulo oferece:
- Tipos nomeados com `TypedDict` para estruturação precisa de metadados;
- Funções para validar caminhos, extrair permissões e tempos;
- Geração unificada de dados com `gerar_dados_item`;
- Conversão de tamanhos legíveis com `converter_tamanho`;
- Tratamento seguro de erros com `ErroAcessoArquivo`.

Compatível com Python 3.12 e tipagem moderna.
"""

from __future__ import annotations

import logging
import stat
from datetime import datetime
from os import stat_result
from pathlib import Path
from typing import Literal, TypedDict

logger: logging.Logger = logging.getLogger(__name__)

# -------------------------------------
# Tipos nomeados para metadados
# -------------------------------------


class Permissoes(TypedDict):
    """Permissões básicas de leitura, escrita e execução para uma categoria de usuário."""

    ler: bool
    escrever: bool
    executar: bool


class PermissoesDetalhadas(TypedDict):
    """Permissões divididas por tipo de usuário: usuário, grupo e outros."""

    usuario: Permissoes
    grupo: Permissoes
    outros: Permissoes


class Proprietario(TypedDict):
    """Identificadores de propriedade do sistema: UID e GID."""

    uid: int
    gid: int


class Tempos(TypedDict):
    """Datas relevantes de um item: criação, modificação e último acesso."""

    data_criacao: datetime
    data_modificacao: datetime
    data_acesso: datetime


class MetadadosArquivo(TypedDict, total=False):
    """Estrutura completa de metadados extraídos de um arquivo ou diretório."""

    nome: str
    caminho_absoluto: str
    caminho_pai: str
    tamanho_bytes: int
    eh_oculto: bool
    dispositivo: int
    proprietario: Proprietario
    tipo: Literal["arquivo", "pasta"]
    extensao: str
    extensao_legivel: str
    permissoes: PermissoesDetalhadas
    data_criacao: datetime
    data_modificacao: datetime
    data_acesso: datetime


# -------------------------------------
# Exceção personalizada
# -------------------------------------


class ErroAcessoArquivo(Exception):
    """Exceção para falhas ao acessar um caminho no sistema de arquivos."""

    def __init__(
        self,
        mensagem: str,
        caminho: str | Path | None = None,
        original: Exception | None = None,
    ) -> None:
        self.caminho = str(caminho) if caminho else None
        self.mensagem = mensagem
        self.original = original
        super().__init__(self.__str__())

    def __str__(self) -> str:
        msg = f"ErroAcessoArquivo: {self.mensagem}"
        if self.caminho:
            msg += f" | Caminho: {self.caminho}"
        if self.original:
            msg += f" | Original: {self.original}"
        return msg


# -------------------------------------
# Funções principais
# -------------------------------------


def validar_caminho(caminho: str | Path) -> Path:
    """
    Verifica se o caminho é válido e acessível.

    Raises:
        TypeError: Se o tipo for inválido.
        ErroAcessoArquivo: Se o caminho não puder ser acessado.
    """
    if not isinstance(caminho, (str, Path)):
        raise TypeError(f"Tipo inválido para caminho: {type(caminho)}")
    path = Path(caminho)
    try:
        _ = path.exists()
    except Exception as e:
        raise ErroAcessoArquivo("Erro ao acessar caminho", caminho, e) from e
    return path


def coletar_permissoes(stats: stat_result) -> PermissoesDetalhadas:
    """Extrai permissões de leitura, escrita e execução para cada tipo de usuário."""
    return {
        "usuario": {
            "ler": bool(stats.st_mode & stat.S_IRUSR),
            "escrever": bool(stats.st_mode & stat.S_IWUSR),
            "executar": bool(stats.st_mode & stat.S_IXUSR),
        },
        "grupo": {
            "ler": bool(stats.st_mode & stat.S_IRGRP),
            "escrever": bool(stats.st_mode & stat.S_IWGRP),
            "executar": bool(stats.st_mode & stat.S_IXGRP),
        },
        "outros": {
            "ler": bool(stats.st_mode & stat.S_IROTH),
            "escrever": bool(stats.st_mode & stat.S_IWOTH),
            "executar": bool(stats.st_mode & stat.S_IXOTH),
        },
    }


def coletar_tempos(stats: stat_result) -> Tempos:
    """Converte os tempos brutos do sistema para objetos `datetime`."""
    return {
        "data_criacao": datetime.fromtimestamp(stats.st_ctime),
        "data_modificacao": datetime.fromtimestamp(stats.st_mtime),
        "data_acesso": datetime.fromtimestamp(stats.st_atime),
    }


def coletar_info_basica(path: Path, stats: stat_result) -> MetadadosArquivo:
    """Coleta metadados básicos e detalhados de um caminho."""
    resultado: MetadadosArquivo = {
        "nome": path.name,
        "caminho_absoluto": str(path.absolute()),
        "caminho_pai": str(path.parent),
        "tamanho_bytes": stats.st_size,
        "eh_oculto": path.name.startswith("."),
        "dispositivo": stats.st_dev,
        "proprietario": {"uid": stats.st_uid, "gid": stats.st_gid},
        **coletar_tempos(stats),
        "permissoes": coletar_permissoes(stats),
    }

    if path.is_file():
        resultado["tipo"] = "arquivo"
        resultado["extensao"] = path.suffix.lower()
        resultado["extensao_legivel"] = (
            path.suffix[1:].upper() if path.suffix else "Sem extensão"
        )
    elif path.is_dir():
        resultado["tipo"] = "pasta"

    return resultado


def gerar_dados_item(caminho: str | Path) -> MetadadosArquivo:
    """
    Agrega todas as informações relevantes de um arquivo ou diretório.

    Raises:
        ErroAcessoArquivo: Em caso de erro de leitura ou permissão.
    """
    caminho_path = validar_caminho(caminho)
    try:
        stats = caminho_path.stat()
        return coletar_info_basica(caminho_path, stats)
    except PermissionError as e:
        logger.error(msg=f"Permissão negada: {caminho_path}")
        raise ErroAcessoArquivo("Permissão negada", caminho_path, e) from e
    except FileNotFoundError as e:
        logger.error(msg=f"Erro inesperado ao processar {caminho_path}: {e}", exc_info=True)
        raise ErroAcessoArquivo("Erro inesperado", caminho_path, e) from e


def converter_tamanho(tamanho_bytes: int | float, precisao: int = 2) -> str:
    """
    Converte tamanho bruto (bytes) em string com unidade legível.

    Raises:
        ValueError: Para valores negativos ou tipos inválidos.
    """
    if not isinstance(tamanho_bytes, (int, float)) or tamanho_bytes < 0:
        raise ValueError("Tamanho deve ser um número positivo")

    unidades = ["B", "KB", "MB", "GB", "TB", "PB"]
    idx = 0
    while tamanho_bytes >= 1024 and idx < len(unidades) - 1:
        tamanho_bytes /= 1024
        idx += 1
    return f"{tamanho_bytes:.{precisao}f} {unidades[idx]}"

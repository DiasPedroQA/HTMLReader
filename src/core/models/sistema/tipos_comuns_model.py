"""
Tipos compartilhados para modelos do sistema.

Define estruturas de dados fundamentais usadas em múltiplos módulos.
"""

from typing import TypedDict, Literal
from datetime import datetime


class Permissoes(TypedDict):
    """Permissões básicas de acesso."""

    ler: bool
    escrever: bool
    executar: bool


class PermissoesDetalhadas(TypedDict):
    """Permissões por categoria de usuário."""

    usuario: Permissoes
    grupo: Permissoes
    outros: Permissoes


class Tempos(TypedDict):
    """Datas relevantes de arquivos/pastas."""

    data_criacao: datetime
    data_modificacao: datetime
    data_acesso: datetime


class MetadadosArquivo(TypedDict, total=False):
    """Estrutura completa de metadados para itens do sistema de arquivos."""

    nome: str
    caminho_absoluto: str
    tipo: Literal["arquivo", "pasta"]
    tamanho_bytes: int
    permissoes: PermissoesDetalhadas
    # ... (outros campos conforme necessário)

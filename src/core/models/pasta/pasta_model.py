"""
Modelo de representação segura de diretórios no sistema de arquivos.

Classes:
    Pasta: Encapsula operações e metadados de pastas com validação integrada.
"""

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

from src.core.models.sistema.tipos_comuns_model import MetadadosArquivo
from src.core.models.arquivo.arquivo_model import Arquivo
from src.core.utils.filesystem.metadados.gerador_metadados import gerar_dados_item

logger = logging.getLogger(__name__)


@dataclass
class Pasta:
    """
    Representa um diretório no sistema de arquivos com operações seguras.

    Atributos:
        caminho (str | Path): Localização da pasta
        _dados (MetadadosArquivo): Metadados carregados automaticamente
    """

    caminho: str | Path
    _dados: MetadadosArquivo = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Valida o caminho e carrega metadados."""
        self.caminho = Path(self.caminho)
        if not self.caminho.is_dir():
            raise NotADirectoryError(f"Caminho inválido: {self.caminho}")
        self._carregar_metadados()

    def _carregar_metadados(self) -> None:
        """Carrega metadados usando o utilitário padrão."""
        self._dados = gerar_dados_item(self.caminho)

    # Propriedades básicas (acesso direto aos metadados)
    @property
    def nome(self) -> str:
        return self._dados["nome"]

    @property
    def caminho_absoluto(self) -> str:
        return self._dados["caminho_absoluto"]

    @property
    def tamanho_bytes(self) -> int:
        """Calcula tamanho total (com cache implícito nos metadados)."""
        return self._dados.get("tamanho_bytes", 0)

    # Iteradores
    @property
    def arquivos(self) -> Iterator[Arquivo]:
        """Gera arquivos imediatos (não recursivo)."""
        for item in self.caminho.iterdir():
            if item.is_file():
                yield Arquivo(item)

    @property
    def subpastas(self) -> Iterator["Pasta"]:
        """Gera subpastas imediatas (não recursivo)."""
        for item in self.caminho.iterdir():
            if item.is_dir():
                yield Pasta(item)

    # Serialização
    def to_dict(self) -> dict[str, Any]:
        """Versão simplificada para serialização."""
        return {**self._dados, "subpastas": [p.to_dict() for p in self.subpastas], "arquivos": [a.to_dict() for a in self.arquivos]}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    def __repr__(self) -> str:
        return f"Pasta(nome='{self.nome}', caminho='{self.caminho}')"

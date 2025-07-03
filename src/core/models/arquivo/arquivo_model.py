"""
Modelo de representação segura de arquivos no sistema.

Classes:
    Arquivo: Encapsula operações, metadados e conteúdo de arquivos com validação integrada.
"""

import hashlib
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Union

from src.core.models.sistema import MetadadosArquivo, PermissoesDetalhadas
from src.core.utils.filesystem import validar_caminho
from src.core.utils.filesystem.metadados.gerador_metadados import gerar_dados_item
from .tipos_model import ErroAcessoArquivo


logger = logging.getLogger(__name__)


@dataclass
class Arquivo:
    """
    Representação segura de um arquivo no sistema de arquivos.

    Atributos:
        caminho_arquivo (Union[str, Path]): Localização do arquivo
        dados_arquivo (MetadadosArquivo): Metadados carregados automaticamente
        _cache_checksum (Optional[str]): Cache do hash MD5 do conteúdo
    """

    caminho_arquivo: Union[str, Path]
    dados_arquivo: MetadadosArquivo = field(init=False, repr=False)
    _cache_checksum: Optional[str] = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """Valida o caminho e carrega metadados."""

        self.caminho_arquivo = validar_caminho(self.caminho_arquivo)
        if not self.caminho_arquivo.is_file():
            raise ErroAcessoArquivo("Caminho não é um arquivo", self.caminho_arquivo)
        self._carregar_metadados()

    def _carregar_metadados(self) -> None:
        """Carrega metadados usando o utilitário padrão."""

        self.dados_arquivo = gerar_dados_item(self.caminho_arquivo)

    # Propriedades básicas
    @property
    def nome(self) -> str:
        return self.dados_arquivo["nome"]

    @property
    def extensao(self) -> str:
        return self.dados_arquivo.get("extensao", "")

    @property
    def permissoes(self) -> PermissoesDetalhadas:
        return self.dados_arquivo["permissoes"]

    # Operações de conteúdo
    def calcular_checksum(self) -> str:
        """Calcula hash MD5 do conteúdo (com cache)."""
        if self._cache_checksum:
            return self._cache_checksum

        hash_md5 = hashlib.md5(usedforsecurity=False)
        try:
            with self.caminho_arquivo.open("rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            self._cache_checksum = hash_md5.hexdigest()
            return self._cache_checksum
        except Exception as e:
            logger.error(str(f"Falha ao calcular checksum: {e}"))
            raise ErroAcessoArquivo("Erro na leitura do arquivo", self.caminho_arquivo, e) from e

    # Serialização
    def to_dict(self) -> dict:
        """Versão simplificada para serialização."""
        return {**self.dados_arquivo, "checksum": self.calcular_checksum()}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    def __repr__(self) -> str:
        return f"Arquivo(nome='{self.nome}', extensao='{self.extensao}')"

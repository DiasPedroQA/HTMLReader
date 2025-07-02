"""
Módulo de representação e manipulação segura de pastas (Python 3.12+)

Este módulo define a classe `Pasta`, encapsulando operações comuns sobre diretórios:
- Validação de estrutura
- Acesso a metadados (nome, permissões, datas)
- Listagem de arquivos e subpastas
- Serialização e cálculo de tamanho total
"""

import json
import logging
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from src.core.models.model_arquivo import Arquivo
from src.core.utils.formatadores import (
    converter_tamanho,
    gerar_dados_item,
)

logger: logging.Logger = logging.getLogger(name=__name__)


@dataclass
class Pasta:
    """
    Representa uma pasta no sistema de arquivos com operações seguras e metadados.

    Esta classe encapsula:
    - Validação e leitura de estrutura
    - Geração de metadados completos via `gerar_dados_item`
    - Navegação e serialização recursiva
    """

    caminho: str | Path
    _dados: Any = field(init=False, repr=False)
    # _dados: dict = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Valida o caminho e carrega os metadados da pasta."""
        try:
            self.caminho = Path(self.caminho)
            if not self.caminho.is_dir():
                raise NotADirectoryError(
                    f"Caminho não é uma pasta válida: {self.caminho}"
                )
            self._carregar_metadados()
        except Exception as e:
            logger.error(msg=f"Falha ao inicializar Pasta: {e}")
            raise

    def _carregar_metadados(self) -> None:
        """Carrega os metadados da pasta utilizando o utilitário `gerar_dados_item`."""
        try:
            self._dados = gerar_dados_item(caminho=self.caminho)
        except Exception as e:
            logger.error(msg=f"Erro ao carregar metadados: {e}")
            raise

    def atualizar_metadados(self) -> None:
        """Recarrega os metadados da pasta."""
        self._carregar_metadados()

    @property
    def nome(self) -> str:
        """Retorna o nome da pasta."""
        return self._dados["nome"]

    @property
    def caminho_absoluto(self) -> str:
        """Retorna o caminho absoluto da pasta."""
        return self._dados["caminho_absoluto"]

    @property
    def criado_em(self) -> datetime:
        """Retorna a data de criação da pasta."""
        return self._dados["data_criacao"]

    @property
    def modificado_em(self) -> datetime:
        """Retorna a data de modificação da pasta."""
        return self._dados["data_modificacao"]

    @property
    def eh_oculto(self) -> bool:
        """Indica se a pasta é oculta (nome iniciado por ponto)."""
        return self._dados.get("eh_oculto", False)

    @property
    def tamanho_bytes(self) -> int:
        """Retorna o tamanho da pasta em bytes (soma aproximada)."""
        total = 0
        self.caminho = Path(self.caminho)
        for f in self.caminho.rglob(pattern="*"):
            if f.is_file():
                total += f.stat().st_size
        return total

    @property
    def tamanho_legivel(self) -> str:
        """Retorna o tamanho total da pasta em formato legível."""
        return converter_tamanho(tamanho_bytes=self.tamanho_bytes)

    @property
    def arquivos(self) -> Iterator[Arquivo]:
        """Itera sobre todos os arquivos na pasta (não recursivo)."""
        self.caminho = Path(self.caminho)
        for f in self.caminho.iterdir():
            if f.is_file():
                yield Arquivo(f)

    @property
    def subpastas(self) -> Iterator["Pasta"]:
        """Itera sobre todas as subpastas imediatas (não recursivo)."""
        self.caminho = Path(self.caminho)
        for d in self.caminho.iterdir():
            if d.is_dir():
                yield Pasta(caminho=d)

    def to_dict(
        self,
    ) -> dict[str, str | int | bool | list[dict[str, str | int | bool]]]:
        """
        Serializa a pasta em dicionário.

        Args:
            incluir_conteudo: Se True, inclui arquivos e subpastas (não recursivo)

        Returns:
            Dicionário com metadados e opcionalmente o conteúdo da pasta.
        """
        # Lista de arquivos como dicionários
        sub_arquivos: list[dict[str, object]] = [
            sub_arquivos.to_dict() for sub_arquivos in self.arquivos
        ]

        # Lista de subpastas como dicionários
        sub_pastas: list[
            dict[str, str | int | bool | list[dict[str, str | int | bool]]]
        ] = [sub_pastas.to_dict() for sub_pastas in self.subpastas]

        # Base do dicionário com metadados principais
        base: dict[str, str | int | bool | list[dict]] = {
            "nome_pasta": self.nome,
            "caminho_absoluto": self.caminho_absoluto,
            "arquivo_criado_em": self.criado_em.isoformat(),
            "arquivo_modificado_em": self.modificado_em.isoformat(),
            "tamanho": self.tamanho_bytes,
            "tamanho_legivel": self.tamanho_legivel,
            "arquivo_eh_oculto": self.eh_oculto,
            "permissoes": self._dados["permissoes"],
            "sub_arquivos": sub_arquivos,
            "sub_pastas": sub_pastas,
        }

        return base

    def to_json(self) -> str:
        """
        Serializa a pasta em formato JSON.

        Args:
            incluir_conteudo: Se True, inclui arquivos e subpastas (não recursivo)

        Returns:
            String JSON representando a pasta.
        """
        return json.dumps(
            self.to_dict(),
            ensure_ascii=False,
            indent=4,
        )

    def __repr__(self) -> str:
        """Retorna uma representação resumida da pasta."""
        return f"Pasta(nome='{self.nome}', caminho='{self.caminho}')"


# Exemplo de uso
if __name__ == "__main__":
    pasta = Pasta(caminho=Path.home() / "Downloads/Firefox")
    print(pasta.to_json())

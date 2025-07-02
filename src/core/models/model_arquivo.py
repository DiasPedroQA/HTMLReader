"""
Módulo de representação e manipulação segura de arquivos (Python 3.12+)

Este módulo define a classe `Arquivo`, encapsulando operações comuns sobre arquivos:
- Verificações de existência e propriedades
- Acesso a metadados (nome, extensão, tamanho, datas)
- Leitura e escrita com segurança
- Suporte a operadores e navegação
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from src.core.utils.formatadores import (  # ErroAcessoArquivo,; Tempos,
    MetadadosArquivo,
    Permissoes,
    PermissoesDetalhadas,
    converter_tamanho,
    gerar_dados_item,
    validar_caminho,
)

logger = logging.getLogger(__name__)


@dataclass
class Arquivo:
    """
    Representa um arquivo com acesso seguro a metadados e conteúdo.
    """

    caminho_arquivo: str | Path
    dados_arquivo: MetadadosArquivo = field(init=False, repr=False)
    _cache_checksum: str | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        self.caminho_arquivo = validar_caminho(caminho=self.caminho_arquivo)
        if not self.caminho_arquivo.is_file():
            raise FileNotFoundError(f"Caminho não é um arquivo: {self.caminho_arquivo}")
        self._carregar_metadados()

    def _carregar_metadados(self) -> None:
        try:
            self.dados_arquivo = gerar_dados_item(self.caminho_arquivo)
        except Exception as e:
            logger.error(msg=f"Erro ao carregar metadados: {e}")
            raise

    def atualizar_metadados(self) -> None:
        """Atualiza os metadados e limpa o cache do checksum."""
        self._carregar_metadados()
        self._cache_checksum = None

    @property
    def checksum(self) -> str:
        """Calcula o checksum MD5 com cache."""
        caminho_interpretado = Path(self.caminho_arquivo)
        if self._cache_checksum:
            return self._cache_checksum

        try:
            hash_md5 = hashlib.md5(usedforsecurity=False)
            with caminho_interpretado.open("rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            self._cache_checksum = hash_md5.hexdigest()
            return self._cache_checksum
        except Exception as e:
            logger.error(msg=f"Erro ao calcular checksum: {e}")
            raise RuntimeError(f"Erro ao ler arquivo: {self.nome}") from e

    def ler(self, encoding: str = "utf-8", tamanho_max: int = 10_000_000) -> str:
        """Lê o conteúdo do arquivo como texto."""
        try:
            caminho_interpretado = Path(self.caminho_arquivo)
            tamanho: int = caminho_interpretado.stat().st_size
            if tamanho > tamanho_max:
                raise RuntimeError(
                    f"Arquivo excede o tamanho permitido: {tamanho} bytes"
                )
            return caminho_interpretado.read_text(encoding=encoding)
        except UnicodeDecodeError:
            logger.warning(msg=f"Falha ao decodificar {self.nome}")
            return ""
        except Exception as e:
            logger.error(msg=f"Erro na leitura: {e}")
            raise RuntimeError(f"Falha ao ler {self.nome}") from e

    def to_dict(self) -> dict[str, object]:
        """Serializa o objeto como dicionário."""
        return {
            "nome": self.nome,
            "caminho": str(self.caminho_arquivo),
            "tamanho": self.tamanho_bytes,
            "tamanho_legivel": self.tamanho_legivel,
            "criado_em": self.criado_em.isoformat(),
            "modificado_em": self.modificado_em.isoformat(),
            "acessado_em": self.acessado_em.isoformat(),
            "extensao": self.extensao,
            "eh_oculto": self.eh_oculto,
            "permissoes": self.permissoes_detalhadas,
            "checksum": self.checksum,
        }

    def to_json(self) -> str:
        """Serializa como JSON formatado."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)

    # ----------------------------
    # Propriedades derivadas
    # ----------------------------

    @property
    def nome(self) -> str:
        return self.dados_arquivo["nome"]

    @property
    def extensao(self) -> str:
        return self.dados_arquivo.get("extensao", "")

    @property
    def tamanho_bytes(self) -> int:
        return int(self.dados_arquivo.get("tamanho_bytes", 0))

    @property
    def tamanho_legivel(self) -> str:
        return converter_tamanho(tamanho_bytes=self.tamanho_bytes)

    @property
    def criado_em(self) -> datetime:
        return self.dados_arquivo.get("data_criacao", datetime.fromtimestamp(0))

    @property
    def modificado_em(self) -> datetime:
        return self.dados_arquivo.get("data_modificacao", datetime.fromtimestamp(0))

    @property
    def acessado_em(self) -> datetime:
        return self.dados_arquivo.get("data_acesso", datetime.fromtimestamp(0))

    @property
    def eh_oculto(self) -> bool:
        return self.dados_arquivo.get("eh_oculto", False)

    @property
    def permissoes_detalhadas(self) -> PermissoesDetalhadas:
        return self.dados_arquivo["permissoes"]

    @property
    def permissoes_usuario(self) -> Permissoes:
        return self.permissoes_detalhadas["usuario"]

    # ----------------------------
    # Métodos utilitários
    # ----------------------------

    def tem_leitura(self) -> bool:
        """Verifica se o usuário tem permissão de leitura."""
        return self.permissoes_usuario.get("ler", False)

    def tem_escrita(self) -> bool:
        """Verifica se o usuário tem permissão de escrita."""
        return self.permissoes_usuario.get("escrever", False)

    def tem_execucao(self) -> bool:
        """Verifica se o usuário tem permissão de execução."""
        return self.permissoes_usuario.get("executar", False)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Arquivo) and self.checksum == other.checksum

    def __repr__(self) -> str:
        return f"Arquivo(nome='{self.nome}', caminho='{self.caminho_arquivo}')"


def exemplo_uso_arquivo(caminho: str | Path) -> None:
    """Demonstração de uso da classe Arquivo."""
    try:
        arquivo = Arquivo(caminho_arquivo=caminho)
        print(f"\n📁 Metadados:\n{arquivo.to_json()}")
        conteudo_x: str = arquivo.ler()
        if conteudo_x:
            print(f"\n📄 Conteúdo (parcial):\n{conteudo_x[:300]}...")
    except ValueError as e:
        logger.error(msg=f"Erro ao processar arquivo: {e}")


# Exemplo de uso
if __name__ == "__main__":
    try:
        arquivo_atual = Arquivo(
            caminho_arquivo=Path.home() / "Downloads/Firefox/bookmarks.html"
        )
        arquivo_visual: str = arquivo_atual.to_json()
        print(f"\nDados do arquivo:\n{arquivo_visual}\n")
        conteudo: str | None = arquivo_atual.ler()
        if conteudo:
            print(f"Conteúdo do arquivo: {conteudo[:500]}...")
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        logger.error(msg=f"Erro ao processar arquivo: {e}")

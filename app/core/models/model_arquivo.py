"""
Módulo de representação e manipulação segura de arquivos (Python 3.12+)

Este módulo define a classe `Arquivo`, encapsulando operações comuns sobre arquivos:
- Verificações de existência e propriedades
- Acesso a metadados (nome, extensão, tamanho, datas)
- Leitura e escrita com segurança
- Suporte a operadores e navegação
"""

import hashlib
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from core.utils.formatadores import (
    # ErroAcessoArquivo,
    # MetadadosArquivo,
    # Permissoes,
    # PermissoesDetalhadas,
    # Proprietario,
    # Tempos,
    # coletar_info_basica,
    # coletar_permissoes,
    # coletar_tempos,
    converter_tamanho,
    gerar_dados_item,
    # validar_caminho,
)

logger: logging.Logger = logging.getLogger(name=__name__)


@dataclass
class Arquivo:
    """
    Representa um arquivo no sistema de arquivos com operações seguras e metadados.

    Esta classe encapsula:
    - Validação e leitura de arquivos
    - Geração de metadados completos via `gerar_dados_item`
    - Cálculo de checksum MD5 com cache
    - Serialização e leitura segura do conteúdo
    """

    caminho_arquivo: str | Path
    dados_arquivo: dict[
        str,
        str | int | datetime | bool | dict[str, dict[str, bool]] | dict[str, int],
    ] = field(init=False, repr=False)
    _cache_checksum: str | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        self.caminho_arquivo = Path(self.caminho_arquivo)
        if not self.caminho_arquivo.is_file():
            raise FileNotFoundError(f"Caminho não é um arquivo: {self.caminho_arquivo}")
        self._carregar_metadados()

    def _carregar_metadados(self) -> None:
        """Carrega os metadados do arquivo utilizando o utilitário `gerar_dados_item`."""
        try:
            self.dados_arquivo = gerar_dados_item(caminho=self.caminho_arquivo)
        except ValueError as e:
            logger.error(msg=f"Erro ao carregar metadados: {e}")
            raise

    def atualizar_metadados(self) -> None:
        """Atualiza os metadados e invalida o cache do checksum."""
        self._carregar_metadados()
        self._cache_checksum = None

    @property
    def checksum(self) -> str:
        """Calcula o checksum MD5 com cache para otimização."""
        if self._cache_checksum is not None:
            return self._cache_checksum

        try:
            self.caminho_arquivo = Path(self.caminho_arquivo)
            # Removido tipo inválido 'hashlib.HASH'
            hash_md5 = hashlib.md5(usedforsecurity=False)
            with self.caminho_arquivo.open("rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            self._cache_checksum = hash_md5.hexdigest()
            return self._cache_checksum
        except Exception as e:
            logger.error(msg=f"Erro ao calcular checksum: {e}")
            raise RuntimeError(
                f"Falha ao ler arquivo para checksum: {self.nome}"
            ) from e

    def ler(self, encoding: str = "utf-8", tamanho_max: int = 10_000_000) -> str:
        """
        Lê o conteúdo do arquivo como texto.

        Args:
            encoding: Codificação do arquivo. Padrão é 'utf-8'.
            tamanho_max: Tamanho máximo permitido para leitura, em bytes.

        Returns:
            Conteúdo do arquivo como string.

        Raises:
            RuntimeError: Se ocorrer erro na leitura ou o tamanho exceder o limite.
        """
        try:
            self.caminho_arquivo = Path(self.caminho_arquivo)
            tamanho: int = self.caminho_arquivo.stat().st_size
            if tamanho > tamanho_max:
                raise RuntimeError(
                    f"Arquivo muito grande ({tamanho} bytes). Limite: {tamanho_max}"
                )
            return self.caminho_arquivo.read_text(encoding=encoding)
        except UnicodeDecodeError:
            logger.warning(msg=f"Falha ao decodificar {self.nome} como {encoding}")
            return ""
        except Exception as e:
            logger.error(msg=f"Erro na leitura: {e}")
            raise RuntimeError(f"Falha ao ler {self.nome}") from e

    def to_dict(self) -> dict[str, object]:
        """
        Serializa o objeto Arquivo em um dicionário com os dados principais e opcionais.

        Returns:
            Dicionário representando os dados do arquivo.
        """
        base: dict[str, object] = {
            "nome_arquivo": str(self.nome),
            "caminho_arquivo": str(self.caminho_arquivo),
            "tamanho": int(self.tamanho_bytes),
            "tamanho_legivel": str(self.tamanho_legivel),
            "arquivo_criado_em": self.criado_em.isoformat(),
            "arquivo_modificado_em": self.modificado_em.isoformat(),
            "extensao_arquivo": str(self.extensao),
            "arquivo_eh_oculto": bool(self.eh_oculto),
            "permissoes": self.dados_arquivo["permissoes"],
            "id_arquivo": str(self.checksum),
        }

        return base

    @property
    def nome(self) -> str:
        """Retorna o nome do arquivo."""
        return str(self.dados_arquivo["nome"])

    @property
    def extensao(self) -> str:
        """Retorna a extensão do arquivo, se houver."""
        return str(self.dados_arquivo.get("extensao", ""))

    @property
    def tamanho_bytes(self) -> int:
        """Retorna o tamanho do arquivo em bytes."""
        valor: (
            str | int | datetime | bool | dict[str, dict[str, bool]] | dict[str, int]
        ) = self.dados_arquivo.get("tamanho_bytes", 0)
        # Garante que só converte para int se for int, float ou str numérico
        if isinstance(valor, int):
            return valor
        if isinstance(valor, float):
            return int(valor)
        if isinstance(valor, str):
            try:
                return int(valor)
            except ValueError:
                return 0
        # Se for qualquer outro tipo (dict, bool, etc), retorna 0
        return 0

    @property
    def tamanho_legivel(self) -> str:
        """Retorna o tamanho do arquivo em formato legível (ex: KB, MB)."""
        return str(converter_tamanho(tamanho_bytes=self.tamanho_bytes))

    @property
    def modificado_em(self) -> datetime:
        """Retorna a data e hora da última modificação do arquivo."""
        valor: (
            str
            | int
            | datetime
            | bool
            | dict[str, dict[str, bool]]
            | dict[str, int]
            | None
        ) = self.dados_arquivo.get("data_modificacao")
        return (
            valor
            if isinstance(valor, datetime)
            else datetime.fromtimestamp(timestamp=0)
        )

    @property
    def criado_em(self) -> datetime:
        """Retorna a data e hora da criação do arquivo."""
        valor: (
            str
            | int
            | datetime
            | bool
            | dict[str, dict[str, bool]]
            | dict[str, int]
            | None
        ) = self.dados_arquivo.get("data_criacao")
        return (
            valor
            if isinstance(valor, datetime)
            else datetime.fromtimestamp(timestamp=0)
        )

    @property
    def eh_oculto(self) -> bool:
        """Indica se o arquivo é oculto (nome iniciado por ponto)."""
        valor: (
            str | int | datetime | bool | dict[str, dict[str, bool]] | dict[str, int]
        ) = self.dados_arquivo.get("eh_oculto", False)
        return bool(valor)

    def __eq__(self, outro: object) -> bool:
        """Compara dois arquivos com base em seus checksums."""
        return isinstance(outro, Arquivo) and self.checksum == outro.checksum

    def __repr__(self) -> str:
        """Retorna representação resumida do objeto."""
        return f"Arquivo(nome='{self.nome}', caminho='{self.caminho_arquivo}')"

    def to_json(self) -> str:
        """
        Serializa o objeto Arquivo em JSON.

        Returns:
            String JSON representando os dados do arquivo.
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)


def exemplo_uso_arquivo(caminho: str | Path) -> None:
    """
    Exemplo de uso moderno com correspondência manual
    ao invés de `match` direto em propriedades.

    Args:
        caminho: Caminho para o arquivo a ser processado.
    """
    arquivo = Arquivo(caminho_arquivo=caminho)

    match arquivo:
        case _ if arquivo.nome.endswith(".html"):
            print(f"Arquivo de texto encontrado: {arquivo.nome}")
        case _ if arquivo.extensao == ".py":
            print("Arquivo Python encontrado")
        case _:
            print("Outro tipo de arquivo")


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

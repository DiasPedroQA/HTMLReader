"""
Módulo de representação e manipulação segura de arquivos (Python 3.12+).

Este módulo define a classe `Arquivo`, que encapsula operações robustas
para lidar com arquivos do sistema.
Inclui validação de caminho, leitura de conteúdo, acesso a metadados,
cálculo de checksum e verificação de permissões,
com suporte a cache e serialização.

Principais recursos:
- Verificação segura de existência e tipo do caminho
- Extração de metadados (nome, tamanho, datas, permissões)
- Leitura textual com controle de tamanho
- Cálculo de checksum com cache (MD5)
- Serialização em dicionário e JSON formatado
- Verificações de permissões de leitura, escrita e execução
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from src.core.utils.formatadores import (
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
    Representa um arquivo no sistema com acesso seguro ao conteúdo e metadados.

    A classe realiza validações automáticas no caminho informado, extrai e armazena
    metadados relevantes, e oferece métodos utilitários como leitura textual,
    cálculo de checksum e serialização em formatos estruturados.

    Atributos:
        caminho_arquivo (str | Path): Caminho absoluto ou relativo do arquivo.
        dados_arquivo (MetadadosArquivo): Metadados coletados automaticamente após a validação.
        _cache_checksum (str | None): Valor em cache do checksum MD5, calculado sob demanda.

    Exceções:
        FileNotFoundError: Se o caminho não corresponder a um arquivo existente.
        RuntimeError: Para erros na leitura de conteúdo ou cálculo de hash.
    """

    caminho_arquivo: str | Path
    dados_arquivo: MetadadosArquivo = field(init=False, repr=False)
    _cache_checksum: str | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """Valida o caminho e carrega os metadados ao instanciar o objeto."""
        self.caminho_arquivo = validar_caminho(caminho=self.caminho_arquivo)
        if not self.caminho_arquivo.is_file():
            raise FileNotFoundError(f"Caminho não é um arquivo: {self.caminho_arquivo}")
        self._carregar_metadados()

    def _carregar_metadados(self) -> None:
        """Coleta os metadados do arquivo e armazena internamente."""
        try:
            self.dados_arquivo = gerar_dados_item(self.caminho_arquivo)
        except Exception as e:
            logger.error(msg=f"Erro ao carregar metadados: {e}")
            raise

    def atualizar_metadados(self) -> None:
        """
        Recarrega os metadados do arquivo e limpa o cache do checksum.

        Deve ser utilizado após modificações no sistema de arquivos que
        possam alterar propriedades como tamanho, datas ou permissões.
        """
        self._carregar_metadados()
        self._cache_checksum = None

    @property
    def checksum(self) -> str:
        """
        Retorna o checksum MD5 do arquivo (com cache).

        O valor é calculado apenas uma vez e armazenado em cache para uso posterior,
        a menos que os metadados sejam atualizados.

        Retorna:
            str: Hash MD5 do conteúdo do arquivo.

        Exceções:
            RuntimeError: Em caso de falha ao acessar ou ler o conteúdo do arquivo.
        """
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
        """
        Lê o conteúdo do arquivo como texto.

        Argumentos:
            encoding (str): Codificação a ser usada para leitura (padrão: 'utf-8').
            tamanho_max (int): Tamanho máximo permitido em bytes (padrão: 10 MB).

        Retorna:
            str: Conteúdo textual do arquivo.

        Exceções:
            RuntimeError: Se o tamanho do arquivo for excedido ou ocorrer erro na leitura.
            UnicodeDecodeError: Se a decodificação falhar (retorna string vazia e emite aviso).
        """
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
        """
        Serializa os metadados e propriedades do arquivo em um dicionário.

        Retorna:
            dict[str, object]: Representação estruturada com informações como nome, tamanho,
            datas de acesso/modificação/criação, permissões e checksum.
        """
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
        """
        Serializa os metadados do arquivo como uma string JSON formatada.

        Retorna:
            str: JSON com identação e suporte a caracteres UTF-8.
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)

    @property
    def nome(self) -> str:
        """Retorna o nome do arquivo."""
        return self.dados_arquivo.get("nome", "")

    @property
    def extensao(self) -> str:
        """Retorna a extensão do arquivo."""
        return self.dados_arquivo.get("extensao", "")

    @property
    def tamanho_bytes(self) -> int:
        """Retorna o tamanho do arquivo em bytes."""
        return int(self.dados_arquivo.get("tamanho_bytes", 0))

    @property
    def tamanho_legivel(self) -> str:
        """Retorna o tamanho do arquivo em formato legível (ex: KB, MB)."""
        return converter_tamanho(tamanho_bytes=self.tamanho_bytes)

    @property
    def criado_em(self) -> datetime:
        """Retorna a data de criação do arquivo."""
        return self.dados_arquivo.get("data_criacao", datetime.fromtimestamp(0))

    @property
    def modificado_em(self) -> datetime:
        """Retorna a data de modificação do arquivo."""
        return self.dados_arquivo.get("data_modificacao", datetime.fromtimestamp(0))

    @property
    def acessado_em(self) -> datetime:
        """Retorna a data de último acesso ao arquivo."""
        return self.dados_arquivo.get("data_acesso", datetime.fromtimestamp(0))

    @property
    def eh_oculto(self) -> bool:
        """Indica se o arquivo é oculto."""
        return self.dados_arquivo.get("eh_oculto", False)

    @property
    def permissoes_detalhadas(self) -> PermissoesDetalhadas:
        """Retorna as permissões detalhadas do arquivo."""
        permissoes: PermissoesDetalhadas | None = self.dados_arquivo.get("permissoes")
        if permissoes is None:
            return PermissoesDetalhadas()  # type: ignore
        return permissoes

    @property
    def permissoes_usuario(self) -> Permissoes:
        """Retorna as permissões do usuário atual sobre o arquivo."""
        return self.permissoes_detalhadas.get("usuario", {})

    def tem_leitura(self) -> bool:
        """
        Verifica se o usuário atual possui permissão de leitura.

        Retorna:
            bool: True se houver permissão de leitura, False caso contrário.
        """
        return self.permissoes_usuario.get("ler", False)

    def tem_escrita(self) -> bool:
        """
        Verifica se o usuário atual possui permissão de escrita.

        Retorna:
            bool: True se houver permissão de escrita, False caso contrário.
        """
        return self.permissoes_usuario.get("escrever", False)

    def tem_execucao(self) -> bool:
        """
        Verifica se o usuário atual possui permissão de execução.

        Retorna:
            bool: True se houver permissão de execução, False caso contrário.
        """
        return self.permissoes_usuario.get("executar", False)

    def __eq__(self, other: object) -> bool:
        """Compara dois objetos Arquivo com base no checksum do conteúdo."""
        return isinstance(other, Arquivo) and self.checksum == other.checksum

    def __repr__(self) -> str:
        """Retorna uma representação resumida e informativa do objeto Arquivo."""
        return f"Arquivo(nome='{self.nome}', caminho='{self.caminho_arquivo}')"


def exemplo_uso_arquivo(caminho: str | Path) -> None:
    """
    Demonstra o uso básico da classe `Arquivo`.

    Tenta instanciar a classe com o caminho fornecido, imprime os metadados em JSON
    e, se possível, exibe um trecho do conteúdo textual do arquivo.

    Argumentos:
        caminho (str | Path): Caminho absoluto ou relativo para o arquivo a ser analisado.
    """
    try:
        arquivo = Arquivo(caminho_arquivo=caminho)
        print(f"\n📁 Metadados:\n{arquivo.to_json()}")
        conteudo_x: str = arquivo.ler()
        if conteudo_x:
            print(f"\n📄 Conteúdo (parcial):\n{conteudo_x[:300]}...")
    except ValueError as e:
        logger.error(msg=f"Erro ao processar arquivo: {e}")


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

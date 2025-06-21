"""
Módulo de representação e manipulação de arquivos no sistema de arquivos.

Este módulo define a classe `Arquivo`, que herda de `CaminhoBase` e encapsula
operações comuns relacionadas a arquivos, como criação, leitura, escrita e
acesso a metadados.

A classe fornece acesso a propriedades úteis como extensão, nome, diretório pai,
tamanho legível e data de modificação formatada. Pode ser utilizada em sistemas
que requerem abstração sobre o sistema de arquivos, com suporte a inspeção e
operações seguras.

Classes:
    Arquivo: Representa um arquivo do sistema, com métodos utilitários e propriedades
             derivadas de seu estado físico no disco.
"""

from pathlib import Path

from core.models.model_caminho_base import CaminhoBase
from core.services.formatadores import (
    converter_bytes_em_tamanho_legivel,
    formatar_data_para_string,
    obter_extensao_legivel,
    formatar_nome_arquivo,
)


class Arquivo(CaminhoBase):
    """Representa um arquivo com propriedades e operações comuns."""

    @property
    def nome_sem_extensao(self) -> str:
        """
        Retorna o nome do arquivo sem a extensão.

        Returns:
            str: Nome do arquivo (sem extensão).
        """
        return formatar_nome_arquivo(nome=self._path.stem)

    @property
    def extensao(self) -> str:
        """
        Retorna a extensão do arquivo (incluindo o ponto).

        Returns:
            str: Extensão do arquivo (ex: '.txt').
        """
        return self._path.suffix

    @property
    def extensao_legivel(self) -> str:
        """
        Retorna uma descrição legível da extensão do arquivo.

        Returns:
            str: Descrição legível da extensão (ex: 'Texto', 'Imagem PNG').
        """
        return obter_extensao_legivel(formato_padrao_extensao=self._path.suffix)

    @property
    def tamanho_legivel(self) -> str:
        """
        Retorna o tamanho do arquivo em formato legível.

        Returns:
            str: Tamanho legível (ex: '1.23 MB').
        """
        if self.tamanho_em_bytes is None:
            return "0 B"
        return converter_bytes_em_tamanho_legivel(tamanho_bytes=self.tamanho_em_bytes)

    @property
    def data_modificacao_legivel(self) -> str | None:
        """
        Retorna a data da última modificação do arquivo em formato legível.

        Returns:
            str | None: Data formatada, ou None se indisponível.
        """
        if self.data_modificacao:
            return formatar_data_para_string(data_e_hora=self.data_modificacao)
        return None

    @property
    def data_criacao_legivel(self) -> str | None:
        """
        Retorna a data da criação do arquivo em formato legível.

        Returns:
            str | None: Data formatada, ou None se indisponível.
        """
        if self.data_criacao:
            return formatar_data_para_string(data_e_hora=self.data_criacao)
        return None

    @property
    def eh_arquivo_oculto(self) -> bool:
        """
        Verifica se o arquivo é oculto (nome inicia com ponto).

        Returns:
            bool: True se for oculto, False caso contrário.
        """
        return self._path.name.startswith(".")

    @property
    def diretorio_pai(self) -> Path:
        """
        Retorna o diretório pai onde o arquivo está localizado.

        Returns:
            Path: Caminho para o diretório pai.
        """
        return self._path.parent

    def criar_arquivo_se_nao_existir(self) -> bool:
        """
        Cria o arquivo se ele não existir, criando também os diretórios necessários.

        Returns:
            bool: True se o arquivo foi criado, False se já existia ou falhou.
        """
        if self.caminho_existe:
            return False
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.touch()
            self._atualizar_estado()
            return True
        except OSError:
            return False

    def escrever_conteudo(
        self, conteudo_arquivo: str, sobrescrever: bool = False
    ) -> bool:
        """
        Escreve conteúdo no arquivo, com controle de sobrescrita.

        Args:
            conteudo_arquivo (str): Conteúdo a ser escrito no arquivo.
            sobrescrever (bool): Se True, sobrescreve arquivo existente.

        Returns:
            bool: True se a escrita foi realizada, False caso contrário.
        """
        if self.caminho_existe and not sobrescrever:
            return False
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._path.open(mode="w", encoding="utf-8") as f:
                f.write(conteudo_arquivo)
            self._atualizar_estado()
            return True
        except OSError:
            return False

    def ler_conteudo(self) -> str | None:
        """
        Lê e retorna o conteúdo textual do arquivo.

        Returns:
            str | None: Conteúdo do arquivo, ou None em caso de erro.
        """
        if not self.caminho_existe:
            return None
        try:
            return self._path.read_text(encoding="utf-8")
        except OSError:
            return None

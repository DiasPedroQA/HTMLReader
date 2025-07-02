"""
Módulo principal de modelos e utilitários do sistema.

Este módulo centraliza os modelos de dados e utilitários para extração e
formatação de informações do sistema operacional, arquivos e diretórios.

Inclui:
- Modelo `SistemaInfo` para representação do estado do sistema operacional;
- Modelos para metadados de arquivos e diretórios com tipagem precisa;
- Exceção personalizada para erros de acesso a caminhos no sistema de arquivos;
- Funções auxiliares para validação de caminhos, coleta de permissões, tempos e
  geração unificada de metadados;
- Conversão de tamanhos de arquivos para formatos legíveis.

Compatível com Python 3.12+ e tipagem moderna.
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Literal, TypedDict

from pydantic import BaseModel

logger: logging.Logger = logging.getLogger(name=__name__)


# ------------------------------
# Modelos do sistema operacional
# ------------------------------


class SistemaInfo(BaseModel):
    """
    Modelo que representa o estado atual do sistema operacional.

    Atributos:
        sistema_operacional: Nome do sistema operacional (ex: 'Linux', 'Windows', 'Darwin').
        versao: Versão do sistema operacional.
        arquitetura: Arquitetura da máquina (ex: 'x86_64', 'arm64').
        nome_maquina: Nome do host ou máquina atual.
        separador_diretorio: Caractere separador de diretório (ex: '/', '\\').
        diretorio_atual: Caminho absoluto do diretório onde o processo está sendo executado.
        raiz_sistema_arquivos: Diretório raiz do sistema de arquivos (ex: '/', 'C:\\').
        codificacao_padrao: Codificação padrão do sistema (ex: 'utf-8').
        tempo_desde_boot: Tempo de atividade da máquina desde o último boot, em formato legível.
        versao_api: Versão da API que está retornando os dados.
        diretorio_usuario: Caminho absoluto para o diretório inicial do usuário
            (ex: '/home/usuario', 'C:\\Users\\usuario').
    """

    sistema_operacional: str
    versao: str
    arquitetura: str
    nome_maquina: str
    separador_diretorio: str
    diretorio_atual: str
    raiz_sistema_arquivos: str
    codificacao_padrao: str
    tempo_desde_boot: str
    versao_api: str
    diretorio_usuario: str


# -----------------------------
# Modelos para metadados de arquivos
# -----------------------------


class Permissoes(TypedDict):
    """
    Permissões básicas de leitura, escrita e execução para uma categoria de usuário.
    """

    ler: bool
    escrever: bool
    executar: bool


class PermissoesDetalhadas(TypedDict):
    """
    Permissões detalhadas divididas por tipo de usuário: usuário, grupo e outros.
    """

    usuario: Permissoes
    grupo: Permissoes
    outros: Permissoes


class Proprietario(TypedDict):
    """
    Identificadores de propriedade do sistema: UID e GID.
    """

    uid: int
    gid: int


class Tempos(TypedDict):
    """
    Datas relevantes de um item no sistema de arquivos: criação, modificação e último acesso.
    """

    data_criacao: datetime
    data_modificacao: datetime
    data_acesso: datetime


class MetadadosArquivo(TypedDict, total=False):
    """
    Estrutura completa de metadados extraídos de um arquivo ou diretório.

    Campos:
        nome: Nome do arquivo ou diretório.
        caminho_absoluto: Caminho absoluto completo.
        caminho_pai: Diretório pai.
        tamanho_bytes: Tamanho em bytes (aplicável a arquivos).
        eh_oculto: Indicador se o item é oculto (nome iniciando com '.').
        dispositivo: ID do dispositivo de armazenamento.
        proprietario: Dados do proprietário (UID e GID).
        tipo: Tipo do item ('arquivo' ou 'pasta').
        extensao: Extensão do arquivo (ex: '.txt').
        extensao_legivel: Extensão formatada para leitura (ex: 'TXT').
        permissoes: Permissões detalhadas.
        data_criacao: Data e hora da criação.
        data_modificacao: Data e hora da última modificação.
        data_acesso: Data e hora do último acesso.
    """

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


# -----------------------------
# Exceção personalizada
# -----------------------------


class ErroAcessoArquivo(Exception):
    """
    Exceção para falhas ao acessar um caminho no sistema de arquivos.

    Args:
        mensagem: Descrição do erro.
        caminho: Caminho que causou o erro.
        original: Exceção original capturada (se houver).
    """

    def __init__(
        self,
        mensagem: str,
        caminho: str | Path | None = None,
        original: Exception | None = None,
    ) -> None:
        self.caminho: str | None = str(caminho) if caminho else None
        self.mensagem: str = mensagem
        self.original: Exception | None = original
        super().__init__(self.__str__())

    def __str__(self) -> str:
        msg: str = f"ErroAcessoArquivo: {self.mensagem}"
        if self.caminho:
            msg += f" | Caminho: {self.caminho}"
        if self.original:
            msg += f" | Original: {self.original}"
        return msg

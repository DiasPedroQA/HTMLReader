"""
Controlador responsável por obter informações detalhadas do sistema operacional
atual, com base nas bibliotecas padrão e utilitários do sistema.

Este controlador pode ser utilizado para exibir diagnósticos ou configurar
comportamentos específicos conforme o ambiente em que a aplicação está rodando.
"""

import os
import platform
import sys
from datetime import datetime

import psutil

from app.core.models.sistema_info import SistemaInfo


class SistemaController:
    """
    Classe controladora que coleta informações do sistema operacional atual.

    Atributos:
        _versao_api: Versão atual da API, injetada na construção.
        _boot_time: Momento em que o sistema foi iniciado (timestamp).
    """

    def __init__(self, versao_api: str) -> None:
        self._versao_api: str = versao_api
        self._boot_time: datetime = datetime.fromtimestamp(timestamp=psutil.boot_time())

    def obter_info(self) -> SistemaInfo:
        """
        Coleta e retorna os dados do sistema encapsulados em um modelo `SistemaInfo`.

        Retorna:
            SistemaInfo: Objeto contendo dados estruturados do ambiente operacional.
        """
        return SistemaInfo(
            sistema_operacional=platform.system(),
            versao=platform.version(),
            arquitetura=platform.machine(),
            nome_maquina=platform.node(),
            separador_diretorio=os.sep,
            diretorio_atual=os.getcwd(),
            raiz_sistema_arquivos=os.path.abspath(path=os.sep),
            codificacao_padrao=sys.getdefaultencoding(),
            tempo_desde_boot=str(datetime.now() - self._boot_time),
            versao_api=self._versao_api,
            diretorio_usuario=os.path.expanduser(path="~"),
        )

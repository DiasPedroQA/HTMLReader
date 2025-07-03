"""
Módulo avançado para detecção do ambiente do sistema operacional.

Funcionalidades:
- Identificação precisa do SO e versão
- Detecção de ambiente virtualizado
- Verificação de arquitetura e recursos
- Interface unificada para diferentes sistemas
"""

import os
import platform
import sys
from typing import Literal, NamedTuple


class SistemaOperacionalDetectado(NamedTuple):
    """
    Estrutura imutável com os dados detectados do sistema operacional.

    Attributes:
        nome (Literal["linux", "windows", "darwin", "outro"]): Nome do SO padronizado.
        versao (str): Versão detalhada do SO.
        arquitetura (str): Arquitetura da máquina (ex: x86_64).
        virtualizado (bool): Indica se o ambiente é virtualizado.
        bits (Literal[32, 64]): Arquitetura de bits.
        caminho_home (str): Diretório home do usuário.
    """

    nome: Literal["linux", "windows", "darwin", "outro"]
    versao: str
    arquitetura: str
    virtualizado: bool
    bits: Literal[32, 64]
    caminho_home: str

    @property
    def resumo(self) -> str:
        """
        Retorna uma representação resumida para logs e depuração.

        Returns:
            str: Texto descritivo resumido do sistema operacional detectado.
        """
        return (
            f"{self.nome.capitalize()} {self.versao} ({self.arquitetura}, "
            f"{self.bits} bits) {'[VIRT]' if self.virtualizado else ''}"
        )


class DetectorSO:
    """
    Classe principal com métodos estáticos para detecção avançada do sistema operacional.
    """

    @staticmethod
    def detectar() -> SistemaOperacionalDetectado:
        """
        Executa todas as verificações e retorna estrutura consolidada do SO.

        Returns:
            SistemaOperacionalDetectado: Dados completos do ambiente detectado.
        """
        nome, versao = DetectorSO._identificar_so()
        return SistemaOperacionalDetectado(
            nome=nome,
            versao=versao,
            arquitetura=platform.machine(),
            virtualizado=DetectorSO._verificar_virtualizacao(),
            bits=64 if sys.maxsize > 2**32 else 32,
            caminho_home=os.path.expanduser("~"),
        )

    @staticmethod
    def _identificar_so() -> tuple[Literal["linux", "windows", "darwin", "outro"], str]:
        """
        Identifica o sistema operacional e obtém sua versão detalhada.

        Returns:
            tuple: Nome padronizado do SO e versão detalhada.
        """
        sistema = platform.system().lower()
        versao = platform.release()

        if sistema == "linux":
            try:
                with open("/etc/os-release", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("PRETTY_NAME="):
                            versao = line.split("=")[1].strip().strip('"')
                            break
            except FileNotFoundError:
                pass

        nome_so = sistema if sistema in ("linux", "windows", "darwin") else "outro"
        return nome_so, versao

    @staticmethod
    def _verificar_virtualizacao() -> bool:
        """
        Detecta se o ambiente está rodando em uma máquina virtual.

        Returns:
            bool: True se virtualizado, False caso contrário.
        """
        if platform.system().lower() == "linux":
            try:
                with open("/proc/cpuinfo", encoding="utf-8") as f:
                    return any("hypervisor" in line.lower() for line in f)
            except FileNotFoundError:
                return False
        return False

    @staticmethod
    def criar_ambiente_testes() -> SistemaOperacionalDetectado:
        """
        Gera dados simulados para ambientes de teste automatizados.

        Returns:
            SistemaOperacionalDetectado: Dados simulados.
        """
        return SistemaOperacionalDetectado(
            nome="linux",
            versao="5.15.0-76-generic",
            arquitetura="x86_64",
            virtualizado=True,
            bits=64,
            caminho_home="/home/teste",
        )

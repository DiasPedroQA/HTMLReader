"""
Controlador para informações do sistema operacional e estrutura de diretórios do usuário.

Responsável por:
- Detecção do sistema operacional
- Acesso ao diretório raiz do usuário
- Coleta de arquivos e pastas do usuário logado

Fornece estruturas padronizadas para consumo por outros componentes.
"""

from functools import cached_property
from pathlib import Path

from core.models.model_arquivo import Arquivo
from core.models.model_caminho_base import CaminhoBase
from core.models.model_pasta import Pasta
from core.utils.sistema_operacional import SistemaOperacional


class ControladorSistema:
    """
    Controlador central para informações do sistema operacional
    e caminhos do sistema de arquivos do usuário.
    """

    def __init__(self, sistema: str | None = None) -> None:
        """
        Inicializa o controlador, detectando ou sobrescrevendo o sistema operacional.

        Args:
            sistema: Nome opcional para simulação do sistema operacional.
        """
        self._sistema: SistemaOperacional = SistemaOperacional.detectar(sistema_simulado=sistema)

    @cached_property
    def raiz_usuario(self) -> Path:
        """Retorna o caminho da pasta raiz do usuário."""
        return SistemaOperacional.obter_raiz_usuario(str(self._sistema))

    @property
    def info_sistema(self) -> dict[str, SistemaOperacional | Path]:
        """
        Retorna informações básicas do sistema e diretório do usuário.

        Returns:
            dict: Contendo sistema operacional e caminho raiz.
        """
        return {
            "sistema": self._sistema,
            "user_root": self.raiz_usuario,
        }

    def listar_itens_usuario(self) -> list[CaminhoBase]:
        """
        Lista arquivos e pastas imediatos do diretório do usuário logado.

        Returns:
            list[CaminhoBase]: Instâncias de `Arquivo` ou `Pasta`.
        """
        pasta_usuario = Pasta(caminho=self.raiz_usuario)
        itens: list[CaminhoBase] = []

        for item in pasta_usuario.itens_diretos:
            match item.retornar_o_tipo:
                case "Arquivo":
                    itens.append(Arquivo(caminho=item.caminho_absoluto))
                case "Pasta":
                    itens.append(Pasta(caminho=item.caminho_absoluto))

        return itens

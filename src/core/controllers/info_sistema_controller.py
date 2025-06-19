"""
Controlador responsável por orquestrar a coleta de informações do sistema
operacional, retornando estruturas padronizadas de dados.
"""

from pathlib import Path

from core.models.model_caminho_base import CaminhoBase, Pasta
from core.services.system_services import SistemaOperacional


class ControladorSistema:
    """Controlador responsável por ler caminhos baseados no sistema operacional."""

    def __init__(self, sistema_atual: str | None = None) -> None:
        """Inicializa o controlador, detectando o sistema e sua pasta raiz."""
        self._sistema: SistemaOperacional = SistemaOperacional.detectar(
            sistema_simulado=sistema_atual
        )
        self._raiz_usuario: Path = SistemaOperacional.obter_raiz_usuario(
            sistema_desejado=sistema_atual
        )
        self._pasta_usuario: Pasta = Pasta(caminho=self._raiz_usuario)

    @property
    def sistema_e_caminho_pasta_usuario(self) -> dict[str, SistemaOperacional | Path]:
        """
        Retorna o sistema operacional detectado ou simulado,
        e o caminho raiz da pasta do usuário.
        """
        return {
            "sistema": self._sistema,
            "user_root": self._raiz_usuario,
        }

    def listar_pasta_usuario(
        self, tipo_item: str | None = "todos"
    ) -> list[CaminhoBase]:
        """Lista o conteúdo da pasta do usuário com filtro opcional."""
        itens: list[CaminhoBase] = self._pasta_usuario.listar_conteudo()

        if tipo_item == "arquivos":
            return [
                i
                for i in itens
                if isinstance(i, CaminhoBase) and i.caminho_absoluto.is_file()
            ]
        if tipo_item == "pastas":
            return [
                i
                for i in itens
                if isinstance(i, CaminhoBase) and i.caminho_absoluto.is_dir()
            ]
        if tipo_item == "todos" or not tipo_item:
            return itens
        return itens

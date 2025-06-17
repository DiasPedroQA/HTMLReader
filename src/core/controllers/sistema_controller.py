"""
Controlador responsável por orquestrar a coleta de informações do sistema
operacional, retornando estruturas padronizadas de dados.
"""

from pathlib import Path
from core.models.pasta_model import ModelPasta
from core.models.base_item import ModelCaminho
from core.services.system_services import obter_info_sistema, obter_diretorio_usuario


class ControladorSistema:
    """
    Controlador para operações relacionadas ao sistema operacional
    e à descoberta de caminhos do usuário.
    """

    _pasta_usuario: ModelPasta

    @staticmethod
    def _registrar_log(operacao: str, mensagem: str) -> None:
        """Registra uma operação no log padrão."""
        print(f"[ControladorSistema] {operacao}: {mensagem}")

    @classmethod
    def identificar_sistema(cls, tipo_sistema: str) -> str:
        """
        Identifica o nome do sistema operacional.

        Args:
            tipo_sistema: Nome base do sistema operacional.

        Returns:
            Nome padronizado do sistema.
        """
        nome_sistema: str = obter_info_sistema(nome_forcado=tipo_sistema)
        cls._registrar_log(
            operacao="Identificação do Sistema",
            mensagem=f"Sistema confirmado: {nome_sistema}",
        )
        return nome_sistema

    @classmethod
    def caminho_usuario_logado(cls, tipo_sistema: str) -> ModelPasta | None:
        """
        Obtém a pasta base do usuário encapsulada como objeto `ModelPasta`.

        Args:
            tipo_sistema: Nome do sistema operacional.

        Returns:
            Representação da pasta do usuário.
        """
        try:
            nome_so: str = cls.identificar_sistema(tipo_sistema=tipo_sistema)
            caminho: Path | None = obter_diretorio_usuario(nome_sistema=nome_so)

            if not caminho or not caminho.exists():
                cls._registrar_log(
                    operacao="Caminho", mensagem="Nenhum caminho válido encontrado."
                )
                # return ModelPasta(path=None)

            # cls._pasta_usuario = ModelPasta(path=caminho)
            cls._registrar_log(
                operacao="Caminho", mensagem=f"Pasta do usuário: {caminho}"
            )
            return cls._pasta_usuario

        except OSError as e:
            cls._registrar_log(
                operacao="Erro", mensagem=f"Falha ao obter caminho do usuário: {e}"
            )
            # return ModelPasta(path=None)

    @classmethod
    def listar_itens_usuario_logado(cls) -> list[ModelCaminho] | None:
        """
        Lista os itens diretos da pasta do usuário logado como objetos de modelo.

        Returns:
            Lista de instâncias de arquivos e pastas.
        """
        if not cls._pasta_usuario:
            cls._registrar_log(
                operacao="Listagem", mensagem="Pasta do usuário ainda não foi definida."
            )
            return None

        try:
            subitens: list[ModelCaminho] = cls._pasta_usuario.listar_subitens()
            cls._registrar_log(
                operacao="Listagem", mensagem=f"{len(subitens)} itens encontrados."
            )
            return subitens
        except OSError as e:
            cls._registrar_log(
                operacao="Erro", mensagem=f"Falha ao listar subitens: {e}"
            )
            return None


if __name__ == "__main__":
    controlador = ControladorSistema()
    sistemas: tuple[str, str, str] = ("windows", "darwin", "linux")

    for sistema in sistemas:
        print(f"\n--- Verificando: {sistema.upper()} ---")
        item: ModelPasta | None = controlador.caminho_usuario_logado(
            tipo_sistema=sistema
        )

        if item is not None:
            print(f"  • Caminho {item} não encontrado ou erro.")
        # else:
            # controlador.listar_itens_usuario_logado(item)

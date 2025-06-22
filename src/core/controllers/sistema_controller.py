"""
Controlador para coleta e organização de informações do sistema operacional.

Responsável por:
- Coordenar a detecção do sistema operacional
- Gerenciar caminhos padrão do usuário
- Fornecer acesso estruturado aos dados do sistema
- Ler conteúdos do diretório do usuário

Retorna sempre estruturas de dados padronizadas para consumo uniforme
por outros componentes do sistema.
"""

from pathlib import Path
from functools import cached_property

from core.models.model_arquivo import Arquivo
from core.models.model_caminho_base import CaminhoBase
from core.models.model_pasta import Pasta
from core.utils.sistema_operacional import SistemaOperacional


class ControladorSistema:
    """
    Controlador central para operações relacionadas ao sistema operacional e
    caminhos do sistema de arquivos.

    Responsável por fornecer abstrações orientadas a objetos para acesso à
    estrutura de diretórios e arquivos do usuário, com suporte à filtragem.
    """

    def __init__(self, sistema_atual: str | None = None) -> None:
        """Inicializa o controlador, detectando ou sobrescrevendo o sistema operacional."""
        self._nome_sistema_operacional: SistemaOperacional = (
            SistemaOperacional.detectar(sistema_simulado=sistema_atual)
        )

    @cached_property
    def _caminho_pasta_raiz_usuario(self) -> Path:
        """Retorna o diretório raiz do usuário (ex: `/home/user`)."""
        return SistemaOperacional.obter_raiz_usuario(
            sistema_desejado=str(self._nome_sistema_operacional)
        )

    @property
    def sistema_e_caminho_pasta_usuario(self) -> dict[str, SistemaOperacional | Path]:
        """Retorna informações básicas do sistema e o caminho do diretório do usuário."""
        return {
            "sistema": self._nome_sistema_operacional,
            "user_root": self._caminho_pasta_raiz_usuario,
        }

    def coletar_itens_da_pasta_usuario_logado(self) -> list[CaminhoBase]:
        """
        Obtém os itens do diretório do usuário logado como instâncias de Arquivo ou Pasta.

        Returns:
            list[CaminhoBase]: Lista de objetos representando arquivos ou pastas.
        """
        pasta_usuario_logado = Pasta(caminho=self._caminho_pasta_raiz_usuario)

        instancias: list[CaminhoBase] = []
        for item in pasta_usuario_logado.conteudo_listado:
            if item.retornar_o_tipo.value == "Arquivo":
                instancias.append(Arquivo(caminho=item.caminho_absoluto))
            elif item.retornar_o_tipo.value == "Pasta":
                instancias.append(Pasta(caminho=item.caminho_absoluto))

        return instancias

"""
Controlador para coleta e organização de informações do sistema operacional.

Responsável por:
- Coordenar a detecção do sistema operacional
- Gerenciar caminhos padrão do usuário
- Fornecer acesso estruturado aos dados do sistema
- Listar conteúdos do diretório do usuário

Retorna sempre estruturas de dados padronizadas para consumo uniforme
por outros componentes do sistema.
"""

from pathlib import Path
from functools import cached_property

from core.models.model_arquivo import Arquivo
from core.models.model_caminho_base import CaminhoBase
from core.models.model_pasta import Pasta
from core.services.system_services import SistemaOperacional


class ControladorSistema:
    """
    Controlador central para operações relacionadas ao sistema operacional e
    caminhos do sistema de arquivos.

    Responsável por fornecer abstrações orientadas a objetos para acesso à
    estrutura de diretórios e arquivos do usuário, com suporte à filtragem.
    """

    def __init__(self, sistema_atual: str | None = None) -> None:
        """Inicializa o controlador, detectando ou sobrescrevendo o sistema operacional."""
        self._sistema: SistemaOperacional = SistemaOperacional.detectar(
            sistema_simulado=sistema_atual
        )

    @cached_property
    def _caminho_pasta_raiz_usuario(self) -> Path:
        """Retorna o diretório raiz do usuário (ex: `/home/user`)."""
        return SistemaOperacional.obter_raiz_usuario(
            sistema_desejado=str(self._sistema)
        )

    @property
    def sistema_e_caminho_pasta_usuario(self) -> dict[str, SistemaOperacional | Path]:
        """Retorna informações básicas do sistema e o caminho do diretório do usuário."""
        return {
            "sistema": self._sistema,
            "user_root": self._caminho_pasta_raiz_usuario,
        }

    def listar_itens_da_pasta_usuario_logado(self) -> list[CaminhoBase]:
        """Lista os itens do diretório do usuário como instâncias de Arquivo ou Pasta."""
        pasta_usuario = Pasta(caminho=self._caminho_pasta_raiz_usuario)
        return self._instanciar_itens(caminhos=pasta_usuario.conteudo_listado)

    def listar_subpastas_de_uma_pasta(self, caminho_da_pasta: Path) -> list[Pasta]:
        """Retorna todas as subpastas imediatas de uma pasta fornecida."""
        pasta = Pasta(caminho=caminho_da_pasta)
        return [Pasta(caminho=p) for p in pasta.conteudo_listado if p.is_dir()]

    def listar_subarquivos_de_uma_pasta(
        self, caminho_da_pasta: Path, extensao_buscada: str | None = None
    ) -> list[Arquivo]:
        """Retorna arquivos da pasta fornecida, com filtro opcional por extensão."""
        pasta = Pasta(caminho=caminho_da_pasta)
        arquivos: list[Arquivo] = [
            Arquivo(caminho=p) for p in pasta.conteudo_listado if p.is_file()
        ]
        if extensao_buscada:
            return [a for a in arquivos if a.extensao == extensao_buscada]
        return arquivos

    def _instanciar_itens(self, caminhos: list[Path]) -> list[CaminhoBase]:
        """Converte uma lista de Paths em instâncias de Arquivo ou Pasta."""
        instancias: list[CaminhoBase] = []
        for caminho in caminhos:
            if caminho.is_file():
                instancias.append(Arquivo(caminho=caminho))
            elif caminho.is_dir():
                instancias.append(Pasta(caminho=caminho))
        return instancias

"""
Módulo de controle para operações com diretórios no sistema de arquivos.

Este módulo define a classe `PastasController`, responsável por mediar a criação
e leitura de pastas, utilizando a model `Pasta` como base de dados e operações.

Funcionalidades disponíveis:
- Criação condicional de diretórios
- Listagem de conteúdo imediato
- Identificação de arquivos e pastas ocultos
- Listagem recursiva completa

Classes:
    PastasController: Controlador de alto nível para interação com pastas.
"""

from pathlib import Path

# from core.models.model_pasta import Pasta
from core.models.model_pasta import Pasta


class PastasController:
    """
    Controlador de operações de criação e leitura de pastas.

    Responsável por coordenar o uso da classe `Pasta` para:
    - Criar diretórios de forma segura
    - Listar conteúdo direto e oculto
    - Realizar buscas recursivas
    """

    def ler_conteudo_da_pasta(self, caminho: str | Path) -> list[str]:
        """
        Retorna os nomes dos arquivos e subpastas contidos diretamente na pasta.

        Args:
            caminho (str | Path): Caminho da pasta a ser lida.

        Returns:
            list[str]: Lista de nomes de arquivos e subpastas.
        """
        pasta = Pasta(caminho=caminho)
        return [p.name for p in pasta.conteudo_listado]

    def listar_ocultos(self, caminho: str | Path) -> list[str]:
        """
        Retorna os nomes dos arquivos e pastas ocultos (nome iniciado com ponto).

        Args:
            caminho (str | Path): Caminho da pasta a ser inspecionada.

        Returns:
            list[str]: Lista de nomes de arquivos e pastas ocultos.
        """
        pasta = Pasta(caminho=caminho)
        return pasta.listar_ocultos()

    def listar_recursivamente(self, caminho: str | Path) -> list[Path]:
        """
        Lista recursivamente todos os arquivos e subpastas contidos na pasta.

        Args:
            caminho (str | Path): Caminho base da varredura.

        Returns:
            list[Path]: Lista completa dos caminhos internos encontrados.
        """
        pasta = Pasta(caminho=caminho)
        return pasta.listar_recursivo() if pasta.caminho_existe else []

    def criar_se_nao_existir(self, caminho_novo: Path) -> bool:
        """
        Cria a pasta se ela ainda não existir.

        Returns:
            bool: True se criada com sucesso, False se já existia.
        """
        pasta = Pasta(caminho=caminho_novo)
        if not pasta.caminho_existe:
            pasta.caminho_absoluto.mkdir(parents=True, exist_ok=True)
            return True
        return False

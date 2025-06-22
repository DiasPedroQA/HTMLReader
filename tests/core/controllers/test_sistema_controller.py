# pylint: disable=W0212, W0621

"""
Testes para o módulo ControladorSistema,
que gerencia a detecção do sistema operacional
e acesso aos diretórios do usuário,
com abstrações para arquivos e pastas.
"""

from pathlib import Path
import pytest

from core.controllers.sistema_controller import ControladorSistema
from core.models.model_arquivo import Arquivo
from core.models.model_pasta import Pasta
from core.models.model_caminho_base import CaminhoBase
from core.utils.sistema_operacional import SistemaOperacional


@pytest.fixture
def controlador_sistema() -> ControladorSistema:
    """Cria e retorna uma instância do controlador do sistema para os testes."""
    return ControladorSistema()


class TestControladorSistema:
    """Testa as funcionalidades da classe ControladorSistema."""

    def test_inicializacao_default(
        self, controlador_sistema: ControladorSistema
    ) -> None:
        """Deve inicializar com o sistema detectado automaticamente."""
        info: dict[str, SistemaOperacional | Path] = (
            controlador_sistema.sistema_e_caminho_pasta_usuario
        )
        assert isinstance(info, dict)
        assert "sistema" in info
        assert isinstance(info["sistema"], SistemaOperacional)
        assert "user_root" in info
        assert isinstance(info["user_root"], Path)

    def test_caminho_pasta_raiz_usuario_cached_property(
        self, controlador_sistema: ControladorSistema
    ) -> None:
        """Deve retornar sempre o mesmo Path para o diretório raiz do usuário."""
        p1: Path = controlador_sistema._caminho_pasta_raiz_usuario
        p2: Path = controlador_sistema._caminho_pasta_raiz_usuario
        assert p1 == p2
        assert isinstance(p1, Path)

    def test_coletar_itens_da_pasta_usuario_logado(
        self,
        tmp_path: Path,
        controlador_sistema: ControladorSistema,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Deve coletar instâncias de Arquivo e Pasta do diretório do usuário simulado."""

        # Criar estrutura simulada
        (tmp_path / "arquivo.txt").write_text(data="conteudo")
        (tmp_path / "pasta").mkdir()

        # Forçar _caminho_pasta_raiz_usuario para tmp_path via monkeypatch
        monkeypatch.setattr(
            target=controlador_sistema,
            name="_caminho_pasta_raiz_usuario",
            value=tmp_path,
        )

        itens: list[CaminhoBase] = (
            controlador_sistema.coletar_itens_da_pasta_usuario_logado()
        )
        nomes: set[str] = {item.nome_caminho for item in itens}

        assert "arquivo.txt" in nomes
        assert "pasta" in nomes

        # Verificar tipos das instâncias
        tipos: set[type[CaminhoBase]] = {type(item) for item in itens}
        assert Arquivo in tipos
        assert Pasta in tipos
        assert all(isinstance(item, (Arquivo, Pasta)) for item in itens)

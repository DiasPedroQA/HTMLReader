# """
# Fixtures globais para testes do projeto HTMLReader.

# Contém definições reutilizáveis de objetos comuns para testes.
# """

# from pathlib import Path

# import pytest

# from src.core.controllers.pastas_controller import PastasController


# @pytest.fixture
# def controller() -> PastasController:
#     """Retorna uma instância de PastasController para uso nos testes."""
#     return PastasController()


# @pytest.fixture
# def temporary_folder(tmp_path: Path) -> Path:
#     """Fornece um diretório temporário exclusivo para testes."""
#     return tmp_path

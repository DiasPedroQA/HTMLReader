"""
Testes unitários para o modelo `Pasta`.

Este módulo cobre:
- Carregamento e análise de conteúdo
- Filtros por extensão
- Subpastas e arquivos ocultos
- Cálculo de tamanho total e contagem de extensões
"""

from pathlib import Path
from typing import NoReturn

import pytest

from core.models.model_arquivo import Arquivo
from core.models.model_pasta import Pasta


class TestPasta:
    """Classe de testes para o modelo `Pasta`."""

    def test_pasta_carregamento_basico(self, tmp_path: Path) -> None:
        """
        Testa o carregamento básico do conteúdo da pasta.

        Verifica se arquivos e subpastas diretos são corretamente detectados
        e acessíveis via propriedades `arquivos` e `subpastas`.
        """
        pasta_raiz: Path = tmp_path
        (pasta_raiz / "arquivo.txt").write_text("abc")
        (pasta_raiz / "subdir").mkdir()

        pasta = Pasta(caminho=pasta_raiz)

        assert pasta.caminho.exists()
        arquivos: list[Arquivo] = list(pasta.arquivos)
        subpastas: list[Pasta] = list(pasta.subpastas)
        assert len(arquivos) == 1
        assert len(subpastas) == 1

    def test_filtro_por_extensao(self, tmp_path: Path) -> None:
        """
        Testa o método de busca com filtro por extensão.

        Garante que arquivos com extensões específicas (independente do case)
        sejam corretamente encontrados pelo método `buscar`.
        """
        (tmp_path / "a.py").write_text("print('a')")
        (tmp_path / "b.txt").write_text("txt")
        (tmp_path / "c.PY").write_text("maiúsculo")

        pasta = Pasta(caminho=tmp_path)
        encontrados: list[Arquivo] = list(pasta.buscar(extensao=".py"))

        assert len(encontrados) == 2
        assert all(arq.extensao == "py" for arq in encontrados)

    def test_extensoes_e_tamanho(self, tmp_path: Path) -> None:
        """
        Testa a contagem de extensões e o cálculo do tamanho total da pasta.

        Verifica se o método `contar_extensoes` retorna o número correto
        de arquivos por extensão, e se `calcular_tamanho_total` computa
        corretamente o tamanho cumulativo dos arquivos.
        """
        (tmp_path / "a.txt").write_text("1234")
        (tmp_path / "b.txt").write_text("5678")
        (tmp_path / "c.log").write_text("logfile")

        pasta = Pasta(caminho=tmp_path)
        extensoes: dict[str, int] = pasta.contar_extensoes()

        assert extensoes.get(".txt") == 2
        assert extensoes.get(".log") == 1

        tamanho_total: int = pasta.calcular_tamanho_total()
        assert tamanho_total > 0

    def test_validar_lanca_erro_quando_nao_pasta(self, tmp_path: Path) -> None:
        """
        Testa o método `validar` para garantir que lança `NotADirectoryError`
        quando o caminho não for um diretório válido (ex.: arquivo).
        """
        arquivo: Path = tmp_path / "arquivo.txt"
        arquivo.write_text("conteúdo")
        pasta = Pasta(caminho=arquivo)

        with pytest.raises(NotADirectoryError):
            pasta.validar()

    def test_propriedades_arquivos_subpastas(self, tmp_path: Path) -> None:
        """
        Testa as propriedades `arquivos` e `subpastas`.

        Confirma que os iteradores retornam objetos do tipo esperado,
        e que os arquivos e subpastas são corretamente listados.
        """
        (tmp_path / "arquivo1.txt").write_text("1")
        (tmp_path / "arquivo2.log").write_text("2")
        subpasta: Path = tmp_path / "subpasta"
        subpasta.mkdir()

        pasta = Pasta(caminho=tmp_path)
        arquivos: list[Arquivo] = list(pasta.arquivos)
        subpastas: list[Pasta] = list(pasta.subpastas)

        assert all(isinstance(a, Arquivo) for a in arquivos)
        assert len(arquivos) == 2
        assert len(subpastas) == 1
        assert subpastas[0].caminho == subpasta

    def test_buscar_com_filtros(self, tmp_path: Path) -> None:
        """
        Testa o método `buscar` com diferentes filtros: nome, extensão e função.

        Verifica se a busca retorna arquivos corretos segundo cada critério aplicado.
        """
        (tmp_path / "a.py").write_text("a")
        (tmp_path / "b.txt").write_text("b")
        (tmp_path / "c.py").write_text("c")

        pasta = Pasta(caminho=tmp_path)

        resultados_nome: list[Arquivo] = list(pasta.buscar(nome="A"))
        resultados_ext: list[Arquivo] = list(pasta.buscar(extensao=".py"))
        resultados_filtro: list[Arquivo] = list(
            pasta.buscar(filtro=lambda arq: arq.nome.endswith("b.txt"))
        )

        assert len(resultados_nome) == 1
        assert all(arq.extensao == "py" for arq in resultados_ext)
        assert len(resultados_filtro) == 1
        assert resultados_filtro[0].nome == "b.txt"

    def test_calcular_tamanho_total_com_erro(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """
        Testa o método `calcular_tamanho_total` simulando erro de acesso a arquivos.

        Usa monkeypatch para simular `OSError` na obtenção do tamanho,
        confirmando que o método ignora esses erros e retorna o total correto.
        """
        (tmp_path / "arquivo.txt").write_text("abc")
        pasta = Pasta(caminho=tmp_path)

        def fake_stat() -> NoReturn:
            raise OSError("Simulado")

        monkeypatch.setattr(Path, "stat", fake_stat)

        total: int = pasta.calcular_tamanho_total()
        assert total == 0

    def test_contar_extensoes_varias(self, tmp_path: Path) -> None:
        """
        Testa a contagem de extensões considerando arquivos variados.

        Garante que arquivos sem extensão ou ocultos não sejam contados,
        e que as extensões válidas sejam corretamente contabilizadas.
        """
        (tmp_path / "a.py").write_text("1")
        (tmp_path / "b.txt").write_text("2")
        (tmp_path / ".oculto").write_text("3")
        (tmp_path / "sem_extensao").write_text("4")

        pasta = Pasta(caminho=tmp_path)
        contagem: dict[str, int] = pasta.contar_extensoes()

        assert contagem.get(".py") == 1
        assert contagem.get(".txt") == 1
        assert ".oculto" not in contagem
        assert "" not in contagem

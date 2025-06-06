"""
Testes automatizados para os modelos de dados relacionados ao sistema de arquivos.

Este módulo valida a criação, herança, preenchimento de campos e rejeição de tipos inválidos
para os modelos CaminhoBruto, CaminhoValido, CaminhoInvalido, Arquivo e Pasta.
"""

from src.htmlreader.core.models.objects_models import Arquivo, CaminhoBruto, CaminhoInvalido, CaminhoValido, Pasta


class TestModelosSistemaArquivos:
    """
    Classe dos testes automatizados para os modelos
    de dados relacionados ao sistema de arquivos.
    """

    def test_caminho_bruto_valido(self) -> None:
        """
        Testa a criação de um CaminhoBruto com caminho válido.
        """
        modelo = CaminhoBruto(caminho_original="/tmp/teste.txt")
        assert modelo.caminho_original == "/tmp/teste.txt"

    def test_caminho_valido_heranca_e_campos(self) -> None:
        """
        Testa a criação de um CaminhoValido e a herança do campo caminho_original.
        """
        modelo = CaminhoValido(caminho_original="entrada", caminho_absoluto="/absoluto/entrada")
        assert modelo.caminho_original == "entrada"
        assert modelo.caminho_absoluto == "/absoluto/entrada"

    def test_caminho_invalido_criacao(self) -> None:
        """
        Testa a criação de um CaminhoInvalido com caminho e motivo.
        """
        modelo = CaminhoInvalido(caminho_invalido="/caminho/errado", motivo="Não existe")
        assert modelo.caminho_invalido == "/caminho/errado"
        assert modelo.motivo == "Não existe"

    def test_arquivo_com_campos_opcionais(self) -> None:
        """
        Testa a criação de um Arquivo com todos os campos opcionais preenchidos.
        """
        arq = Arquivo(
            caminho_original="arq.txt",
            caminho_absoluto="/tmp/arq.txt",
            conteudo_arquivo="abc",
            tamanho_bytes=3,
            modificado_em_timestamp=123.4,
            criado_em_timestamp=100.0,
            pasta_atual="/tmp",
        )
        assert arq.conteudo_arquivo == "abc"
        assert arq.tamanho_bytes == 3
        assert arq.modificado_em_timestamp == 123.4
        assert arq.criado_em_timestamp == 100.0
        assert arq.pasta_atual == "/tmp"

    def test_arquivo_sem_campos_opcionais(self) -> None:
        """
        Testa a criação de um Arquivo sem preencher os campos opcionais.
        """
        arq = Arquivo(caminho_original="arq.txt", caminho_absoluto="/tmp/arq.txt")
        assert arq.conteudo_arquivo is None
        assert arq.tamanho_bytes is None
        assert arq.modificado_em_timestamp is None
        assert arq.criado_em_timestamp is None
        assert arq.pasta_atual is None

    def test_pasta_com_listagens(self) -> None:
        """
        Testa a criação de uma Pasta com arquivos e subpastas listados.
        """
        pasta = Pasta(
            caminho_original="pasta",
            caminho_absoluto="/tmp/pasta",
            arquivos_na_pasta=["a.txt", "b.txt"],
            subpastas=["sub1", "sub2"],
        )
        assert pasta.arquivos_na_pasta == ["a.txt", "b.txt"]
        assert pasta.subpastas == ["sub1", "sub2"]

    def test_pasta_sem_listagens(self) -> None:
        """
        Testa a criação de uma Pasta sem arquivos e subpastas listados.
        """
        pasta = Pasta(caminho_original="pasta", caminho_absoluto="/tmp/pasta")
        assert pasta.arquivos_na_pasta is None
        assert pasta.subpastas is None

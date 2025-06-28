"""
Módulo de representação e manipulação segura de arquivos.

Este módulo define a classe `Arquivo`, encapsulando operações comuns sobre arquivos:
- Verificações de existência e propriedades
- Acesso a metadados (nome, extensão, tamanho, datas)
- Leitura e escrita com segurança
- Suporte a operadores e navegação
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from core.utils.formatadores import (
    formatar_arquivo_tamanho_legivel,
    formatar_arquivo_data_para_string,
    formatar_arquivo_valor_booleano,
    formatar_arquivo_obter_extensao_legivel,
)


@dataclass
class Arquivo:
    """
    Representação orientada a objetos de um arquivo no sistema.

    Atributos:
        caminho (Path): Caminho físico do arquivo.
    """

    caminho: Path = field(repr=True)

    # ----------------------
    # Propriedades básicas
    # ----------------------

    @property
    def existe(self) -> bool:
        """Verifica se o arquivo existe e é acessível."""
        return self.caminho.is_file()

    @property
    def nome(self) -> str:
        """Retorna o nome completo do arquivo (com extensão)."""
        return self.caminho.name

    @property
    def nome_base(self) -> str:
        """Retorna o nome do arquivo sem a extensão."""
        return self.caminho.stem

    @property
    def extensao(self) -> str:
        """Retorna a extensão do arquivo (sem o ponto)."""
        return self.caminho.suffix.lstrip(".").lower()

    @property
    def extensao_legivel(self) -> str:
        """Retorna a extensão formatada (com ponto, se aplicável)."""
        return formatar_arquivo_obter_extensao_legivel(
            extensao_arquivo=self.caminho.suffix
        )

    @property
    def diretorio_pai(self) -> Path:
        """Retorna o diretório pai do arquivo."""
        return self.caminho.parent

    # ----------------------
    # Metadados e análise
    # ----------------------

    @property
    def tamanho_bytes(self) -> int:
        """Retorna o tamanho do arquivo em bytes."""
        try:
            return self.caminho.stat().st_size if self.existe else 0
        except OSError:
            return 0

    @property
    def tamanho_legivel(self) -> str:
        """Retorna o tamanho do arquivo em formato legível (ex: '1.2 MB')."""
        return formatar_arquivo_tamanho_legivel(tamanho_bytes=self.tamanho_bytes)

    @property
    def criado_em(self) -> datetime | None:
        """Data de criação do arquivo."""
        try:
            return (
                datetime.fromtimestamp(timestamp=self.caminho.stat().st_ctime)
                if self.existe
                else None
            )
        except OSError:
            return None

    @property
    def criado_em_legivel(self) -> str | None:
        """Data de criação formatada como string."""
        if not self.criado_em:
            return None
        return formatar_arquivo_data_para_string(
            float_data_e_hora=self.criado_em.timestamp()
        )

    @property
    def modificado_em(self) -> datetime | None:
        """Data de modificação do arquivo."""
        try:
            return (
                datetime.fromtimestamp(timestamp=self.caminho.stat().st_mtime)
                if self.existe
                else None
            )
        except OSError:
            return None

    @property
    def modificado_em_legivel(self) -> str | None:
        """Data de modificação formatada como string."""
        if not self.modificado_em:
            return None
        return formatar_arquivo_data_para_string(
            float_data_e_hora=self.modificado_em.timestamp()
        )

    @property
    def eh_oculto(self) -> bool:
        """Verifica se o arquivo é oculto (nome inicia com ponto)."""
        return self.nome.startswith(".")

    @property
    def eh_oculto_legivel(self) -> str:
        """Retorna visibilidade como valor legível ('Sim'/'Não')."""
        return formatar_arquivo_valor_booleano(valor=self.eh_oculto)

    # ----------------------
    # Operações
    # ----------------------

    def ler(self, encoding: str = "utf-8") -> str | None:
        """Lê o conteúdo do arquivo como texto."""
        try:
            return self.caminho.read_text(encoding=encoding) if self.existe else None
        except (OSError, UnicodeDecodeError, PermissionError):
            return None

    def criar(self, conteudo: str, encoding: str = "utf-8") -> bool:
        """
        Cria um novo arquivo com o conteúdo fornecido.

        Args:
            conteudo (str): Texto a ser salvo no arquivo.
            encoding (str): Codificação utilizada para escrita (padrão: utf-8).

        Returns:
            bool: True se o arquivo foi criado com sucesso; False se o arquivo já existia
            ou se ocorreu uma falha durante a criação.
        """
        if self.existe:
            return False
        try:
            self.caminho.parent.mkdir(parents=True, exist_ok=True)
            self.caminho.write_text(data=conteudo, encoding=encoding)
            return True
        except OSError:
            return False

    # ----------------------
    # Utilidades
    # ----------------------

    def __truediv__(self, subcaminho: str) -> Arquivo:
        """Permite composição de caminhos com o operador `/`."""
        return Arquivo(caminho=self.caminho / subcaminho)

    def __str__(self) -> str:
        return str(self.caminho)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.caminho}')"


# def exemplo_arquivo() -> None:
#     print("\n🔍 Teste com caminho válido")
#     caminho_valido = Path("teste_valido.txt")
#     arquivo_valido = Arquivo(caminho=caminho_valido)

#     conteudo_exemplo = "Conteúdo de teste para o arquivo."

#     # Escrita
#     sucesso: bool = arquivo_valido.criar(conteudo=conteudo_exemplo)
#     print(f"✔️ Escrita bem-sucedida: {sucesso}")

#     # Leitura
#     texto: str | None = arquivo_valido.ler()
#     print(f"📖 Leitura: {texto}")

#     # Metadados
#     print(f"📄 Nome: {arquivo_valido.nome}")
#     print(f"🧩 Extensão: {arquivo_valido.extensao}")
#     print(f"📁 Diretório pai: {arquivo_valido.diretorio_pai}")
#     print(f"📦 Existe: {arquivo_valido.existe}")
#     print(f"📏 Tamanho: {arquivo_valido.tamanho_bytes} bytes")
#     print(f"📅 Criado em: {arquivo_valido.criado_em}")
#     print(f"🕓 Modificado em: {arquivo_valido.modificado_em}")
#     print(f"🙈 É oculto: {arquivo_valido.eh_oculto}")

#     print("\n❌ Teste com caminho inválido")
#     caminho_invalido = Path("/caminho/que/nao/existe.txt")
#     arquivo_invalido = Arquivo(caminho=caminho_invalido)

#     print(f"📦 Existe: {arquivo_invalido.existe}")
#     print(f"📖 Leitura: {arquivo_invalido.ler()}")
#     print(
#         f"🧩 Escrita (sem sobrescrever): {arquivo_invalido.criar(conteudo='x', encoding='utf-8')}"
#     )


# if __name__ == "__main__":
#     exemplo_arquivo()

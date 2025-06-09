import os
from core.models.objects_models import Arquivo
from core.models.pasta_models import Pasta


class PastaService:
    """
    Serviço responsável por construir e listar estruturas de pastas com seus respectivos arquivos.
    """

    @staticmethod
    def construir_estrutura_pasta(caminho: str) -> Pasta:
        """
        Cria e retorna uma estrutura completa de Pasta, incluindo subpastas e arquivos,
        baseada em um diretório do sistema de arquivos.

        Args:
            caminho (str): Caminho absoluto da pasta a ser representada.

        Returns:
            Pasta: Estrutura recursiva representando a hierarquia da pasta e seus arquivos.
        """
        pasta = Pasta(nome=os.path.basename(caminho), caminho=caminho)

        if not os.path.exists(caminho) or not os.path.isdir(caminho):
            # Retorna a pasta vazia se o caminho não existir ou não for um diretório
            return pasta

        try:
            entradas = os.listdir(caminho)
        except PermissionError:
            # Em caso de falta de permissão, retorna a pasta atual sem listar conteúdos
            return pasta

        for entrada in entradas:
            caminho_completo = os.path.join(caminho, entrada)

            if os.path.isdir(caminho_completo):
                # Chamada recursiva para subdiretórios
                subpasta = PastaService.construir_estrutura_pasta(caminho_completo)
                pasta.subpastas.append(subpasta)
            else:
                try:
                    tamanho = os.path.getsize(caminho_completo)
                except OSError:
                    tamanho = 0  # Em caso de erro ao acessar o tamanho, define como 0

                tipo = "html" if entrada.lower().endswith(".html") else "outro"

                arquivo = Arquivo(
                    nome=entrada, caminho=caminho_completo, tamanho=tamanho, tipo=tipo
                )
                pasta.arquivos.append(arquivo)

        return pasta

    @staticmethod
    def listar_pasta(caminho: str) -> Pasta:
        """
        Lista os conteúdos de um diretório, construindo uma estrutura recursiva com subpastas e arquivos.

        Args:
            caminho (str): Caminho absoluto da pasta a ser listada.

        Returns:
            Pasta: Objeto contendo as subpastas e arquivos encontrados.
        """
        pasta = Pasta(nome=os.path.basename(caminho), caminho=caminho)

        try:
            entradas = os.listdir(caminho)
        except FileNotFoundError:
            return pasta

        for entrada in entradas:
            caminho_completo = os.path.join(caminho, entrada)

            if os.path.isdir(caminho_completo):
                subpasta = PastaService.listar_pasta(caminho_completo)
                pasta.subpastas.append(subpasta)
            else:
                tamanho = os.path.getsize(caminho_completo)
                tipo = "html" if entrada.lower().endswith(".html") else "outro"

                arquivo = Arquivo(
                    nome=entrada, caminho=caminho_completo, tamanho=tamanho, tipo=tipo
                )
                pasta.arquivos.append(arquivo)

        return pasta

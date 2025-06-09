from core.models.pasta_models import Pasta


class VisorService:
    @staticmethod
    def exibir_pasta(pasta: Pasta, nivel: int = 0) -> None:
        indent = "    " * nivel
        print(f"{indent}Pasta: {pasta.nome} (caminho: {pasta.caminho})")
        for arquivo in pasta.arquivos:
            print(
                f"{indent}    Arquivo: {arquivo.nome} - Tipo: {arquivo.tipo} - Tamanho: {arquivo.tamanho} bytes"
            )
        for subpasta in pasta.subpastas:
            VisorService.exibir_pasta(subpasta, nivel + 1)

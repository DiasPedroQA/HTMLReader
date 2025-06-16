"""
Controlador responsável por orquestrar a coleta de informações do sistema
operacional de forma específica para cada SO, com registro de operações.
"""

import json
from pathlib import Path
from core.services.system_services import obter_info_sistema, obter_diretorio_usuario
from core.models.pasta_model import Arquivo, ItemDoSistema, Pasta
from core.utils.formatadores import converter_bytes_em_tamanho_legivel


class ControladorSistema:
    """Controlador para operações específicas por sistema operacional."""

    @staticmethod
    def _registrar_log(operacao: str, mensagem: str) -> None:
        """Registra mensagens de log formatadas.

        Args:
            operacao: Nome da operação sendo registrada
            mensagem: Detalhes da operação
        """
        print(f"[ControladorSistema] {operacao}: {mensagem}")

    @staticmethod
    def identificar_sistema(tipo_sistema: str) -> str:
        """Obtém o sistema operacional conforme solicitado.

        Args:
            tipo_sistema: Tipo do sistema a identificar ('linux', 'windows', 'darwin')

        Returns:
            Nome do sistema operacional confirmado
        """
        nome_sistema: str = obter_info_sistema(nome_forcado=tipo_sistema)
        ControladorSistema._registrar_log(
            operacao="Identificação do Sistema",
            mensagem=f"Sistema confirmado: {nome_sistema}",
        )
        return nome_sistema

    @staticmethod
    def obter_caminho_usuario(tipo_sistema: str) -> Path | None:
        """Obtém o caminho do usuário para o sistema especificado.

        Args:
            tipo_sistema: Tipo do sistema operacional

        Returns:
            Path do diretório home ou None se inválido

        Raises:
            OSError: Quando o sistema não é suportado
        """
        try:
            sistema_atual: str = ControladorSistema.identificar_sistema(
                tipo_sistema=tipo_sistema
            )
            caminho_usuario: Path | None = obter_diretorio_usuario(
                nome_sistema=sistema_atual
            )

            mensagem: str = (
                f"Caminho encontrado: {caminho_usuario}"
                if caminho_usuario
                else "Nenhum caminho válido encontrado"
            )
            ControladorSistema._registrar_log(
                operacao="Identificação do Caminho", mensagem=mensagem
            )

            return caminho_usuario

        except OSError as erro:
            ControladorSistema._registrar_log(
                operacao="Erro", mensagem=f"Sistema não suportado: {str(erro)}"
            )
            return None


if __name__ == "__main__":
    # Exemplo de uso
    controlador = ControladorSistema()
    sistemas_verificar: tuple[str, str, str] = ("windows", "darwin", "linux")

    for sistema in sistemas_verificar:
        print(f"\nVerificando sistema {sistema.upper()}:")
        caminho: Path | None = controlador.obter_caminho_usuario(tipo_sistema=sistema)

        if caminho:
            print(f"  • Caminho válido encontrado: {caminho}")
            # Exemplo de uso do novo modelo

            try:
                # O método fábrica decide se cria uma Pasta ou um Arquivo
                item_raiz: ItemDoSistema = ItemDoSistema.from_caminho(
                    caminho_fornecido="/home/pedro-pm-dias/Downloads/Firefox"
                )

                # Agora, verificamos o tipo do item retornado
                if isinstance(item_raiz, Pasta):
                    print(f"O item é uma PASTA: {item_raiz.nome}")
                    print(
                        f"Ela contém {len(item_raiz.subarquivos)} arquivo(s) e"
                        f" {len(item_raiz.subpastas)} subpasta(s)."
                    )

                    # Exibindo o conteúdo da pasta
                    for arquivo in item_raiz.subarquivos:
                        print(f"  - Arquivo: {arquivo.nome}")

                    for subpasta in item_raiz.subpastas:
                        print(
                            f"  - Subpasta: {subpasta.nome} (Tamanho: {
                                converter_bytes_em_tamanho_legivel(
                                    tamanho_bytes=subpasta.tamanho_em_bytes
                                )
                            })"
                        )

                    # Usando o método para_dict_formatado que existe na Pasta
                    print("\n--- Dicionário Formatado da Pasta ---")
                    print(
                        json.dumps(
                            item_raiz.para_dict_formatado(recursivo=False),
                            indent=4,
                            ensure_ascii=False,
                        )
                    )

                elif isinstance(item_raiz, Arquivo):
                    print(f"O item é um ARQUIVO: {item_raiz.nome}")
                    print(
                        f"Tamanho: {
                            converter_bytes_em_tamanho_legivel(
                                tamanho_bytes=item_raiz.tamanho_em_bytes
                            )
                        }"
                    )

                    # Usando o método para_dict_formatado que existe no Arquivo
                    print("\n--- Dicionário Formatado do Arquivo ---")
                    print(
                        json.dumps(
                            item_raiz.para_dict_formatado(),
                            indent=4,
                            ensure_ascii=False,
                        )
                    )

            except (ValueError, FileNotFoundError) as e:
                print(f"Ocorreu um erro: {e}")

        else:
            print(f"  • Não foi possível determinar um caminho válido para {sistema}")

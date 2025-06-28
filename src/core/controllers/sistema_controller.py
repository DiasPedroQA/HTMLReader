# # controlador_sistema.py
# # pylint: disable=W0212

# """
# Controlador para informações do sistema operacional e estrutura de diretórios do usuário.
# """

# from pathlib import Path

# # from core.models.model_arquivo import Arquivo
# # from core.models.model_caminho_base import CaminhoBase
# # from core.models.model_pasta import Pasta
# from core.utils.sistema_operacional import SistemaOperacional

# # from core.controllers.pastas_controller import PastasController


# class ControladorSistema:
#     """
#     Controlador central para informações do sistema operacional.
#     """

#     def info_sistema(self) -> dict[str, str | Path]:
#         """
#         Retorna informações básicas do sistema e diretório do usuário.

#         Returns:
#             dict[str, str | Path]: Contendo sistema operacional e caminho raiz.
#         """
#         sistema_atual: SistemaOperacional = SistemaOperacional.detectar_sistema()
#         return {
#             "sistema_operacional": sistema_atual.value,
#             "diretorio_usuario": sistema_atual.obter_raiz_usuario_logado,
#         }


# # # Exemplo de uso
# # if __name__ == "__main__":
# #     controlador = ControladorSistema()
# #     info: dict[str, str | Path] = controlador.info_sistema()

# #     print("\nInformações do Sistema:")
# #     print(f"SO: {info['sistema_operacional']}")
# #     print(f"Diretório usuário: {info['diretorio_usuario']}")
# #     diretorio_usuario_path = Path(info['diretorio_usuario'])
# #     print(f"Existe? {diretorio_usuario_path.exists()}")

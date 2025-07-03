# """
# Pacote principal da aplicação.

# Configura:
#     - Caminhos absolutos
#     - Variáveis de ambiente
#     - Inicialização do sistema
# """

# import sys
# from pathlib import Path

# from loggers import setup_logging

# # Configura caminhos
# BASE_DIR = Path(__file__).parent.parent
# sys.path.insert(0, str(BASE_DIR))

# # Variáveis especiais
# __version__ = "1.0.0"
# __author__ = "Seu Nome"


# # Inicialização
# def init():
#     """Configuração inicial do pacote."""

#     setup_logging()


# __all__ = ["__version__", "__author__", "BASE_DIR"]

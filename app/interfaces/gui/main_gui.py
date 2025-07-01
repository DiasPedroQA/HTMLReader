# """
# Módulo principal da interface gráfica do HTMLReader.
# Coordena a criação e o empacotamento dos widgets da aplicação.
# """

# import tkinter as tk
# from pathlib import Path
# from interfaces.gui.widgets.header_widget import HeaderWidget
# from interfaces.gui.widgets.footer_widget import FooterWidget
# from interfaces.gui.widgets.sidebar_widget import SidebarWidget
# from interfaces.gui.widgets.main_section_widget import VisualizadorArquivoPasta


# class Aplicacao(tk.Tk):
#     """
#     Classe principal da aplicação com interface gráfica Tkinter.
#     Organiza o layout geral contendo cabeçalho, rodapé, menu lateral e conteúdo principal.
#     """

#     def __init__(self) -> None:
#         """
#         Inicializa a janela principal da aplicação e monta a interface.
#         """
#         super().__init__()
#         self.title("App Modular com Widgets Tkinter")
#         self.geometry("800x600")
#         self.configure(bg="white")
#         self._criar_layout()

#     def _criar_layout(self) -> None:
#         """
#         Cria e posiciona todos os widgets da interface gráfica.
#         """
#         caminho_base = Path.home()  # Caminho expandido para o diretório do usuário

#         header = HeaderWidget(master=self, caminho_raiz=caminho_base)
#         header.pack(side="top", fill="x")

#         footer = FooterWidget(master=self)
#         footer.pack(side="bottom", fill="x")

#         area_central = tk.Frame(self)
#         area_central.pack(expand=True, fill="both")

#         sidebar = SidebarWidget(
#             master=area_central,
#             botoes=[
#                 ("Ação 1", self.executar_acao_1),
#                 ("Ação 2", self.executar_acao_2),
#                 ("Sair", self.destroy),
#             ],
#         )
#         sidebar.pack(side="left", fill="y")

#         self.main_section = VisualizadorArquivoPasta(master=area_central)
#         self.main_section.pack(side="left", expand=True, fill="both")

#     def executar_acao_1(self) -> None:
#         """
#         Executa a Ação 1 (exemplo).
#         """
#         print("Ação 1 executada")

#     def executar_acao_2(self) -> None:
#         """
#         Executa a Ação 2 (exemplo).
#         """
#         print("Ação 2 executada")


# if __name__ == "__main__":
#     app = Aplicacao()
#     app.mainloop()

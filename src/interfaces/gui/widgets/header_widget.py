"""
Módulo responsável por definir o widget de cabeçalho da interface gráfica.
Este componente exibe informações do sistema no topo da aplicação.
"""

import tkinter as tk


class HeaderWidget(tk.Frame):
    """
    Widget que representa o cabeçalho da interface gráfica.
    Exibe o título da aplicação e informações do ambiente do usuário.
    """

    def __init__(
        self,
        master: tk.Misc | None = None,
        caminho_raiz: str | None = None,
        infos_sistema: dict[str, str] | None = None,
        **kwargs: object,
    ) -> None:
        """
        Inicializa o HeaderWidget com informações do sistema.

        :param master: Componente pai ao qual o cabeçalho será vinculado.
        :param caminho_raiz: Caminho raiz da aplicação, opcional.
        :param infos_sistema: Dicionário contendo dados do sistema (SO, usuário, pasta raiz).
        :param kwargs: Argumentos adicionais para o Frame.
        """
        super().__init__(master=master, bg="darkgray", height=80)
        self.caminho_raiz: str | None = caminho_raiz
        self.infos_sistema: dict[str, str] = infos_sistema or {}

        self.pack_propagate(flag=False)
        self._criar_componentes()

    def _criar_componentes(self) -> None:
        """Cria os componentes visuais do cabeçalho."""
        container = tk.Frame(master=self, bg="darkgray")
        container.pack(expand=True, fill="both", padx=10)

        # Título da aplicação
        titulo_label = tk.Label(
            master=container,
            text="HTMLReader",
            bg="darkgray",
            fg="white",
            font=("Arial", 16, "bold"),
        )
        titulo_label.pack(anchor="w")

        # Labels informativos dinâmicos
        for chave, valor in self.infos_sistema.items():
            texto: str = f"{chave.capitalize()}: {valor}"
            label = tk.Label(
                master=container,
                text=texto,
                bg="darkgray",
                fg="white",
                font=("Arial", 10),
            )
            label.pack(anchor="w")

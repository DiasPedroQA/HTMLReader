"""
Módulo responsável pela criação do widget de rodapé da aplicação Tkinter.
Este componente exibe uma faixa inferior com mensagens dinâmicas de status.
"""

import tkinter as tk
from typing import Any


class FooterWidget(tk.Frame):
    """
    Widget que representa o rodapé da interface gráfica.
    Exibe mensagens dinâmicas de status na parte inferior da janela.
    """

    def __init__(
        self,
        master: tk.Misc | None = None,
        texto_inicial: str = "Pronto",
        **kwargs: Any,
    ) -> None:
        """
        Inicializa o FooterWidget com um fundo verde claro e texto customizável.

        :param master: Componente pai ao qual o rodapé será anexado.
        :param texto_inicial: Texto inicial exibido no rodapé.
        :param kwargs: Argumentos adicionais passados ao construtor da classe `tk.Frame`.
        """
        super().__init__(master=master, bg="lightgreen", height=30, **kwargs)
        self.pack_propagate(flag=False)

        self._label = tk.Label(
            master=self,
            text=texto_inicial,
            bg="lightgreen",
            font=("Arial", 10),
            anchor="w",
            padx=10,
        )
        self._label.pack(fill="both", expand=True)

    def atualizar_texto(self, mensagem: str) -> None:
        """
        Atualiza o texto exibido no rodapé.

        :param mensagem: Novo texto a ser exibido.
        """
        self._label.config(text=mensagem)

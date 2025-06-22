"""
Módulo responsável por definir o widget da barra lateral (sidebar) da interface gráfica.
Exibe um menu vertical com botões configuráveis dinamicamente.
"""

import tkinter as tk
from collections.abc import Callable
from typing import Any, TypeAlias

BotaoConfig: TypeAlias = tuple[str, Callable[[], None]]


class SidebarWidget(tk.Frame):
    """
    Widget que representa uma barra lateral contendo botões de ações verticais.
    Permite atualização dinâmica dos botões e destaque do botão ativo.
    """

    def __init__(
        self,
        master: tk.Misc | None = None,
        botoes: list[BotaoConfig] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Inicializa a SidebarWidget com um fundo azul claro e um conjunto opcional de botões.

        :param master: Componente pai ao qual a barra lateral será anexada.
        :param botoes: Lista de tuplas (texto, função) para gerar os botões inicialmente.
        :param kwargs: Argumentos adicionais passados para o construtor de `tk.Frame`.
        """
        super().__init__(master=master, bg="lightblue", width=150, **kwargs)
        self.pack_propagate(flag=False)

        self._botoes: dict[str, Callable[[], None]] = {}
        self._botao_widgets: dict[str, tk.Button] = {}
        self._botao_ativo: str | None = None

        # Título do menu
        label = tk.Label(master=self, text="Menu / Ações", bg="lightblue", font=("Arial", 12, "bold"))
        label.pack(pady=10)

        # Container interno para os botões
        self._frame_botoes = tk.Frame(master=self, bg="lightblue")
        self._frame_botoes.pack(fill="both", expand=True)

        # Criação inicial dos botões
        if botoes:
            self.atualizar_botoes(botoes=botoes)

    def atualizar_botoes(self, botoes: list[BotaoConfig]) -> None:
        """
        Atualiza dinamicamente os botões exibidos na sidebar.

        :param botoes: Lista de tuplas contendo (texto, função).
        """

        def criar_callback(mensagem: str) -> Callable[[], None]:
            def callback() -> None:
                self._executar_acao(texto=mensagem)

            return callback

        # Limpa os botões anteriores
        for widget in self._frame_botoes.winfo_children():
            widget.destroy()
        self._botoes.clear()
        self._botao_widgets.clear()
        self._botao_ativo = None

        # Adiciona novos botões
        for texto, comando in botoes:
            self._botoes[texto] = comando

            botao = tk.Button(
                master=self._frame_botoes,
                text=texto,
                command=criar_callback(mensagem=texto),
                bg="white",
                relief="raised",
                anchor="w",
                padx=5,
            )
            botao.pack(fill="x", padx=10, pady=4)
            self._botao_widgets[texto] = botao

    def _executar_acao(self, texto: str) -> None:
        """
        Executa a ação associada a um botão e destaca visualmente o botão ativo.

        :param texto: Texto do botão clicado.
        """
        if self._botao_ativo and self._botao_ativo in self._botao_widgets:
            self._botao_widgets[self._botao_ativo].configure(bg="white")

        self._botao_ativo = texto
        self._botao_widgets[texto].configure(bg="#d0e6ff")

        if texto in self._botoes:
            self._botoes[texto]()

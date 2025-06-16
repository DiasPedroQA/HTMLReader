"""
Módulo contendo o widget VisualizadorArquivoPasta para a interface gráfica do HTMLReader.
Este componente exibe uma árvore de diretórios e permite visualizar conteúdos de arquivos.
A lógica de acesso ao sistema de arquivos deve ser separada do widget.
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path
from typing import Any


class VisualizadorArquivoPasta(tk.Frame):
    """
    Widget visualizador de arquivos e pastas, somente leitura.
    Exibe uma árvore de diretórios e arquivos à esquerda e o conteúdo do item selecionado à direita.
    """

    TAMANHO_MAX_ARQUIVO: int = 1024 * 1024  # Limite de 1MB para leitura do arquivo

    def __init__(
        self,
        master: tk.Misc | None = None,
        caminho_raiz: Path | str = ".",
        **kwargs: Any,
    ) -> None:
        """
        Inicializa o widget.

        Parâmetros:
            master (tk.Misc | None): Componente pai.
            caminho_raiz (Path | str): Caminho raiz da árvore exibida.
            kwargs (Any): Argumentos adicionais para o Frame.
        """
        super().__init__(master=master, **kwargs)
        self.caminho_raiz: Path = Path(caminho_raiz).expanduser().resolve()

        # Configura árvore (painel esquerdo)
        self.tree = ttk.Treeview(master=self, columns=("fullpath",), show="tree")
        self.tree.pack(side="left", fill="y")

        # Scrollbar vertical para a árvore
        self.scrollbar_tree = ttk.Scrollbar(
            master=self, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=self.scrollbar_tree.set)
        self.scrollbar_tree.pack(side="left", fill="y")

        # Área de texto para visualização (painel direito)
        self.texto_visualizacao = tk.Text(master=self, wrap="word", state="disabled")
        self.texto_visualizacao.pack(side="right", fill="both", expand=True)

        # Popula a árvore com o nó raiz
        self._popular_tree()

        # Eventos para expandir nós e selecionar itens
        self.tree.bind("<<TreeviewOpen>>", self._on_item_expandido)
        self.tree.bind("<<TreeviewSelect>>", self._on_item_selecionado)

    def _popular_tree(self) -> None:
        """Limpa e insere o nó raiz na árvore."""
        self.tree.delete(*self.tree.get_children())
        self._inserir_item(parent="", caminho=self.caminho_raiz)

    def _inserir_item(self, parent: str, caminho: Path) -> None:
        """
        Insere um item na árvore.

        Parâmetros:
            parent (str): ID do nó pai.
            caminho (Path): Caminho do item a ser inserido.
        """
        node_id: str = self.tree.insert(parent, "end", text=caminho.name, open=False)
        self.tree.set(node_id, "fullpath", str(caminho))

        if caminho.is_dir():
            # Insere um nó "falso" para permitir expansão dinâmica
            self.tree.insert(node_id, "end", text="carregando...")

    def _on_item_expandido(self, _event: tk.Event | None = None) -> None:
        """
        Handler chamado ao expandir um nó da árvore para carregar seus filhos.

        Parâmetros:
            _event (tk.Event | None): Evento Tkinter (opcional).
        """
        node_id: str = self.tree.focus()
        fullpath = self.tree.set(node_id, "fullpath")
        caminho = Path(fullpath)

        # Remove nós filhos existentes (nó "falso")
        self.tree.delete(*self.tree.get_children(node_id))

        try:
            filhos: list[Path] = sorted(
                caminho.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())
            )
            for filho in filhos:
                self._inserir_item(node_id, filho)
        except OSError as e:
            self.tree.insert(node_id, "end", text=f"Erro ao listar: {e}")

    def _on_item_selecionado(self, _: tk.Event) -> None:
        """
        Handler chamado ao selecionar um item da árvore para exibir seu conteúdo.

        Parâmetros:
            _ (tk.Event): Evento de seleção do Tkinter (não utilizado).
        """
        node_id: str = self.tree.focus()
        if not node_id:
            return

        fullpath: str = self.tree.set(node_id, "fullpath")
        caminho = Path(fullpath)

        if caminho.is_dir():
            self._mostrar_conteudo_pasta(caminho_pasta=caminho)
        else:
            self._mostrar_conteudo_arquivo(caminho_arquivo=caminho)

    def _mostrar_conteudo_pasta(self, caminho_pasta: Path) -> None:
        """
        Exibe o conteúdo da pasta no painel de texto.

        Parâmetros:
            caminho_pasta (Path): Caminho da pasta a exibir.
        """
        self.texto_visualizacao.config(state="normal")
        self.texto_visualizacao.delete("1.0", "end")

        try:
            itens: str = "\n".join(f.name for f in sorted(caminho_pasta.iterdir()))
            conteudo: str = f"Conteúdo da pasta {caminho_pasta}:\n\n{itens}"
        except OSError as e:
            conteudo = f"Erro ao listar conteúdo da pasta:\n{e}"

        self.texto_visualizacao.insert("1.0", conteudo)
        self.texto_visualizacao.config(state="disabled")

    def _mostrar_conteudo_arquivo(self, caminho_arquivo: Path) -> None:
        """
        Exibe o conteúdo do arquivo no painel de texto.

        Parâmetros:
            caminho_arquivo (Path): Caminho do arquivo a exibir.
        """
        self.texto_visualizacao.config(state="normal")
        self.texto_visualizacao.delete("1.0", "end")

        try:
            if caminho_arquivo.stat().st_size > self.TAMANHO_MAX_ARQUIVO:
                conteudo: str = (
                    f"Arquivo muito grande para exibir "
                    f"(>{self.TAMANHO_MAX_ARQUIVO // 1024} KB)."
                )
            else:
                with caminho_arquivo.open(mode="r", encoding="utf-8") as f:
                    conteudo = f.read()
        except (OSError, UnicodeDecodeError) as e:
            conteudo = f"Erro ao ler arquivo:\n{e}"

        self.texto_visualizacao.insert("1.0", conteudo)
        self.texto_visualizacao.config(state="disabled")

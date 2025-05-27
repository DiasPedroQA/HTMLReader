"""
Módulo de interface gráfica para o HTMLReader.
Fornece janela Tkinter para exibir informações do sistema,
analisar caminhos e processar HTML usando o backend.
"""

import tkinter as tk
from tkinter import scrolledtext, filedialog
from htmlreader.core.utils.system_utils import get_os_info, analyze_path


def build_os_frame(parent):
    """
    Cria o frame com informações do sistema operacional.

    Args:
        parent: Widget pai.

    Returns:
        tk.LabelFrame: Frame preenchido com informações do sistema.
    """
    frame = tk.LabelFrame(parent, text="Informações do Sistema")
    frame.pack(fill=tk.X, padx=10, pady=5)
    for k, v in get_os_info().items():
        tk.Label(frame, text=f"{k}: {v}").pack(anchor="w")
    return frame


def build_path_frame(parent):
    """
    Cria o frame para análise de caminhos.

    Args:
        parent: Widget pai.

    Returns:
        tk.LabelFrame: Frame com entrada de caminho e resultado da análise.
    """
    frame = tk.LabelFrame(parent, text="Analisador de Caminho")
    frame.pack(fill=tk.X, padx=10, pady=5)

    entry = tk.Entry(frame)
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

    result = scrolledtext.ScrolledText(frame, height=5, state="disabled")
    result.pack(fill=tk.X, padx=5, pady=(5, 5))

    def choose_path():
        """
        Abre diálogo para selecionar arquivo ou diretório e preenche o campo de entrada.
        """
        path = filedialog.askopenfilename() or filedialog.askdirectory()
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    def analyze():
        """
        Analisa o caminho informado e exibe o resultado no campo de texto.
        """
        info = analyze_path(entry.get().strip())
        result.config(state="normal")
        result.delete("1.0", tk.END)
        for k, v in info.items():
            result.insert(tk.END, f"{k}: {v}\n")
        result.config(state="disabled")

    tk.Button(frame, text="...", width=3, command=choose_path).pack(
        side=tk.LEFT, padx=5
    )
    tk.Button(frame, text="Analisar", command=analyze).pack(pady=(0, 5))
    return frame


def build_html_frame(parent):
    """
    Cria o frame para processamento de HTML.

    Args:
        parent: Widget pai.

    Returns:
        tuple: Frame, campo de entrada e campo de saída.
    """
    frame = tk.LabelFrame(parent, text="HTML Parser")
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    inp = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=10)
    inp.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    out = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=10, state="disabled")
    out.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

    return frame, inp, out


def run_gui() -> None:
    """
    Inicializa e executa a interface gráfica principal do HTMLReader.
    """
    window = tk.Tk()
    window.title("HTMLReader – GUI")
    window.geometry("700x600")

    build_os_frame(window)
    build_path_frame(window)
    build_html_frame(window)

    window.mainloop()


if __name__ == "__main__":
    run_gui()

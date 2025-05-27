"""
Módulo de interface gráfica para o HTMLReader.
Fornece janela Tkinter para exibir informações do sistema,
analisar caminhos e processar HTML usando o backend.
"""

import tkinter as tk
from tkinter import scrolledtext, filedialog
from htmlreader.backend.cli import get_os_info, analyze_path


def run_gui() -> None:
    """
    Inicializa e exibe a interface gráfica do HTMLReader.
    Coleta entrada do usuário e exibe os resultados de:
      - Informações do sistema operacional
      - Análise de caminhos de arquivos/diretórios
      - Parsing de HTML (título, links e texto)
    """
    window = tk.Tk()
    window.title("HTMLReader – GUI")
    window.geometry("700x600")

    # --- OS Info Frame ---
    os_frame = tk.LabelFrame(window, text="Informações do Sistema")
    os_frame.pack(fill=tk.X, padx=10, pady=5)
    info = get_os_info()
    for k, v in info.items():
        lbl = tk.Label(os_frame, text=f"{k}: {v}")
        lbl.pack(anchor="w")

    # --- Path Analyzer Frame ---
    path_frame = tk.LabelFrame(window, text="Analisador de Caminho")
    path_frame.pack(fill=tk.X, padx=10, pady=5)

    path_entry = tk.Entry(path_frame)
    path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

    def choose_path() -> None:
        """Abre diálogo para selecionar arquivo ou diretório."""
        file = filedialog.askopenfilename()
        if file:
            path_entry.delete(0, tk.END)
            path_entry.insert(0, file)
        else:
            directory = filedialog.askdirectory()
            if directory:
                path_entry.delete(0, tk.END)
                path_entry.insert(0, directory)

    tk.Button(path_frame, text="...", width=3, command=choose_path).pack(
        side=tk.LEFT, padx=5
    )
    path_result = scrolledtext.ScrolledText(path_frame, height=5, state="disabled")
    path_result.pack(fill=tk.X, padx=5, pady=(5, 5))

    def on_analyze_path() -> None:
        """Executa análise de caminho usando o backend e exibe o resultado."""
        p = path_entry.get().strip()
        info = analyze_path(p)
        path_result.config(state="normal")
        path_result.delete("1.0", tk.END)
        for k, v in info.items():
            path_result.insert(tk.END, f"{k}: {v}\n")
        path_result.config(state="disabled")

    tk.Button(path_frame, text="Analisar", command=on_analyze_path).pack(pady=(0, 5))

    # --- HTML Parser Frame ---
    html_frame = tk.LabelFrame(window, text="HTML Parser")
    html_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    html_input = scrolledtext.ScrolledText(html_frame, wrap=tk.WORD, height=10)
    html_input.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    html_output = scrolledtext.ScrolledText(
        html_frame, wrap=tk.WORD, height=10, state="disabled"
    )
    html_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))


if __name__ == "__main__":
    run_gui()

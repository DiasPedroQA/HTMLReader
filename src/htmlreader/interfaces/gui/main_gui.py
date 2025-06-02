"""
Interface gráfica principal do HTMLReader.

Permite ao usuário selecionar uma pasta e
visualizar seu conteúdo usando o visor_service.
"""

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from src.htmlreader.core.services import visor_service
from src.htmlreader.core.models.visor_models import FiltroVisor


def visualizar_pasta():
    """
    Abre um diálogo para seleção de pasta, lista o conteúdo da pasta selecionada
    e exibe os itens na interface gráfica. Em caso de erro, exibe uma mensagem.
    """
    path = filedialog.askdirectory()
    if not path:
        return
    try:
        lista = visor_service.listar_conteudo(Path(path), FiltroVisor())
        text_output.delete(1.0, tk.END)
        for item in lista.itens:
            text_output.insert(tk.END, f"[{item.tipo.upper()}] {item.path}\n")
    except (OSError, ValueError) as e:
        messagebox.showerror("Erro", str(e))


root = tk.Tk()
root.title("HTMLReader GUI")

btn = tk.Button(root, text="Selecionar Pasta", command=visualizar_pasta)
btn.pack(pady=10)

text_output = tk.Text(root, height=25, width=80)
text_output.pack(padx=10, pady=10)

root.mainloop()

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from core.controllers.conversao_controller import ConversaoController


class HTMLReaderGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("HTMLReader - Interface Gráfica")
        self.geometry("800x600")

        self.btn_abrir = tk.Button(
            self, text="Abrir Arquivo HTML", command=self.abrir_arquivo
        )
        self.btn_abrir.pack(pady=10)

        self.text_area = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, width=100, height=30
        )
        self.text_area.pack(padx=10, pady=10)

    def abrir_arquivo(self) -> None:
        caminho = filedialog.askopenfilename(
            filetypes=[("Arquivos HTML", "*.html"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    conteudo = f.read()
                controller = ConversaoController()
                resultado = controller.converter_html_para_json(conteudo)
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, resultado)
            except (OSError, UnicodeDecodeError) as e:
                messagebox.showerror("Erro", f"Erro ao processar o arquivo:\n{e}")


if __name__ == "__main__":
    app = HTMLReaderGUI()
    app.mainloop()

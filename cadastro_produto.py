import tkinter as tk
from tkinter import messagebox
from db import conectar
from product_utils import reorder_product_ids

def abrir_tela_cadastro(callback=None):
    janela = tk.Toplevel()
    janela.title("Cadastro de Produto")
    janela.geometry("300x250")

    tk.Label(janela, text="Nome do Produto:").pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="Quantidade Inicial:").pack()
    entry_quantidade = tk.Entry(janela)
    entry_quantidade.pack()

    tk.Label(janela, text="Quantidade Mínima:").pack()
    entry_minimo = tk.Entry(janela)
    entry_minimo.pack()

    def salvar():
        nome = entry_nome.get().strip()
        try:
            quantidade = int(entry_quantidade.get())
            minimo = int(entry_minimo.get())
        except ValueError:
            messagebox.showerror("Erro", "Quantidade e mínimo devem ser números inteiros.")
            return

        if nome == "":
            messagebox.showerror("Erro", "O nome do produto é obrigatório.")
            return

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produtos (nome, quantidade, minimo) VALUES (?, ?, ?)", 
                       (nome, quantidade, minimo))
        conn.commit()
        conn.close()

        reorder_product_ids()

        messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado!")
        if callback:
            callback()
        janela.destroy()

    tk.Button(janela, text="Cadastrar", command=salvar).pack(pady=10)

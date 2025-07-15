import tkinter as tk
from tkinter import messagebox
from db import conectar

def abrir_edicao_estoque(produto_id, nome_produto, quantidade_atual):
    janela = tk.Toplevel()
    janela.title(f"Atualizar Estoque - {nome_produto}")
    janela.geometry("300x200")

    tk.Label(janela, text=f"Estoque atual: {quantidade_atual}").pack(pady=10)
    tk.Label(janela, text="Quantidade a alterar (+ ou -):").pack()
    entry = tk.Entry(janela)
    entry.pack()

    def salvar():
        try:
            valor = int(entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Informe um número válido.")
            return

        nova_qtd = quantidade_atual + valor
        if nova_qtd < 0:
            messagebox.showerror("Erro", "O estoque não pode ficar negativo.")
            return

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (nova_qtd, produto_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Estoque atualizado com sucesso!")
        janela.destroy()

    tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)

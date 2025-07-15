import tkinter as tk
from tkinter import messagebox
from db import conectar
from utils import criptografar_senha

def abrir_tela_cadastro_usuario():
    janela = tk.Toplevel()
    janela.title("Cadastro de Usuário")
    janela.geometry("300x300")

    tk.Label(janela, text="Nome completo:").pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="Usuário (login):").pack()
    entry_usuario = tk.Entry(janela)
    entry_usuario.pack()

    tk.Label(janela, text="Senha:").pack()
    entry_senha = tk.Entry(janela, show="*")
    entry_senha.pack()

    tk.Label(janela, text="Perfil:").pack()
    perfil_var = tk.StringVar(janela)
    perfil_var.set("comum")  # padrão
    tk.OptionMenu(janela, perfil_var, "admin", "comum").pack()

    def cadastrar():
        nome = entry_nome.get().strip()
        usuario = entry_usuario.get().strip()
        senha = entry_senha.get().strip()
        perfil = perfil_var.get()

        if not nome or not usuario or not senha:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return

        senha_hash = criptografar_senha(senha)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
        if cursor.fetchone():
            messagebox.showerror("Erro", "Usuário já existe.")
            conn.close()
            return

        cursor.execute("INSERT INTO usuarios (nome, usuario, senha, perfil) VALUES (?, ?, ?, ?)",
                       (nome, usuario, senha_hash, perfil))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        janela.destroy()

    tk.Button(janela, text="Cadastrar", command=cadastrar).pack(pady=10)

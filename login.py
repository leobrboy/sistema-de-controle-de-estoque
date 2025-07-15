import tkinter as tk
from tkinter import messagebox
from db import conectar
from utils import verificar_senha
import dashboard

def fazer_login(usuario, senha, root):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
    user = cursor.fetchone()

    if user and verificar_senha(senha, user['senha']):
        messagebox.showinfo("Login", f"Bem-vindo, {user['nome']}!")
        root.destroy()
        dashboard.abrir_dashboard(user)
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos.")

def iniciar_login():
    root = tk.Tk()
    root.title("Login")
    root.geometry("300x200")

    tk.Label(root, text="Usuário:").pack()
    entry_usuario = tk.Entry(root)
    entry_usuario.pack()

    tk.Label(root, text="Senha:").pack()
    entry_senha = tk.Entry(root, show="*")
    entry_senha.pack()

    def ao_clicar():
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        fazer_login(usuario, senha, root)

    tk.Button(root, text="Entrar", command=ao_clicar).pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    iniciar_login()

import tkinter as tk
from tkinter import messagebox
from db import conectar

def abrir_dashboard(usuario_logado):
    root = tk.Tk()
    root.title("Dashboard - Controle de Estoque")
    root.state('zoomed')
    root.geometry("700x450")

    tk.Label(root, text=f"Usuário: {usuario_logado['nome']} ({usuario_logado['perfil']})", font=("Arial", 10)).pack(anchor='ne', padx=10, pady=5)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    headers = ["ID", "Produto", "Quantidade", "Mínimo"]
    for col, h in enumerate(headers):
        tk.Label(frame, text=h, width=15, borderwidth=1, relief="solid").grid(row=0, column=col)

    conn = conectar()
    cursor = conn.cursor()

    # Pagination variables
    items_per_page = 25
    current_page = 1

    def load_page(page):
        nonlocal current_page
        current_page = page
        for widget in frame.winfo_children():
            widget.destroy()

        for col, h in enumerate(headers):
            tk.Label(frame, text=h, width=15, borderwidth=1, relief="solid").grid(row=0, column=col)

        offset = (page - 1) * items_per_page
        cursor.execute("SELECT * FROM produtos ORDER BY id LIMIT ? OFFSET ?", (items_per_page, offset))
        produtos = cursor.fetchall()

        from editar_estoque import abrir_edicao_estoque

        for i, produto in enumerate(produtos, start=1):
            id_, nome, qtd, minimo = produto
            alerta = qtd < minimo
            cor_fundo = "red" if alerta else "white"
            cor_texto = "white" if alerta else "black"

            tk.Label(frame, text=id_, width=5, bg=cor_fundo, fg=cor_texto, borderwidth=1, relief="solid").grid(row=i, column=0)
            tk.Label(frame, text=nome, width=20, bg=cor_fundo, fg=cor_texto, borderwidth=1, relief="solid").grid(row=i, column=1)
            tk.Label(frame, text=qtd, width=12, bg=cor_fundo, fg=cor_texto, borderwidth=1, relief="solid").grid(row=i, column=2)
            tk.Label(frame, text=minimo, width=10, bg=cor_fundo, fg=cor_texto, borderwidth=1, relief="solid").grid(row=i, column=3)

            def remover_produto(produto_id):
                if messagebox.askyesno("Confirmação", "Tem certeza que deseja remover este produto?"):
                    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
                    conn.commit()

                    from product_utils import reorder_product_ids
                    reorder_product_ids()

                    messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
                    load_page(current_page)

            tk.Button(frame, text="Editar", command=lambda p=produto: abrir_edicao_estoque(p[0], p[1], p[2])).grid(row=i, column=4)
            if usuario_logado['perfil'] == 'admin':
                tk.Button(frame, text="Remover", command=lambda p=produto: remover_produto(p[0])).grid(row=i, column=5)

        # Pagination controls
        cursor.execute("SELECT COUNT(*) FROM produtos")
        total_items = cursor.fetchone()[0]
        total_pages = (total_items + items_per_page - 1) // items_per_page

        # Use a persistent pagination frame and label
        if not hasattr(root, 'pagination_frame'):
            root.pagination_frame = tk.Frame(root)
            root.pagination_frame.pack(pady=5)

            root.page_label = tk.Label(root.pagination_frame, text=f"Página {current_page} de {total_pages}")
            root.page_label.pack(side='left', padx=5)

            root.prev_button = tk.Button(root.pagination_frame, text="Anterior", command=lambda: load_page(current_page - 1) if current_page > 1 else None)
            root.prev_button.pack(side='left', padx=5)

            root.next_button = tk.Button(root.pagination_frame, text="Próxima", command=lambda: load_page(current_page + 1) if current_page < total_pages else None)
            root.next_button.pack(side='left', padx=5)
        else:
            root.page_label.config(text=f"Página {current_page} de {total_pages}")
            root.prev_button.config(state='normal' if current_page > 1 else 'disabled')
            root.next_button.config(state='normal' if current_page < total_pages else 'disabled')

        # No need to create new pagination frame or buttons on each load_page call

    load_page(current_page)

    def refresh_dashboard():
        root.destroy()
        abrir_dashboard(usuario_logado)

    if usuario_logado['perfil'] == 'admin':
        from cadastro_produto import abrir_tela_cadastro
        from cadastro_usuario import abrir_tela_cadastro_usuario

        tk.Button(root, text="Cadastrar Produto", command=lambda: abrir_tela_cadastro(callback=refresh_dashboard)).pack()
        tk.Button(root, text="Cadastrar Usuário", command=abrir_tela_cadastro_usuario).pack()

    def sair():
        root.destroy()
        import login
        login.iniciar_login()

    if usuario_logado['perfil'] == 'admin':
        def abrir_consultar_usuarios():
            janela = tk.Toplevel()
            janela.title("Consulta de Usuários")
            janela.geometry("600x400")

            frame = tk.Frame(janela)
            frame.pack(pady=10)

            headers = ["ID", "Nome", "Perfil", "Editar", "Remover"]
            for col, h in enumerate(headers):
                tk.Label(frame, text=h, width=15, borderwidth=1, relief="solid").grid(row=0, column=col)

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, perfil FROM usuarios")
            usuarios = cursor.fetchall()

            def abrir_editar_usuario(usuario):
                edit_janela = tk.Toplevel()
                edit_janela.title(f"Editar Usuário - {usuario[1]}")
                edit_janela.geometry("300x250")

                tk.Label(edit_janela, text="Nome:").pack()
                tk.Label(edit_janela, text=usuario[1]).pack()

                tk.Label(edit_janela, text="Perfil:").pack()
                perfil_var = tk.StringVar(value=usuario[2])
                perfil_entry = tk.Entry(edit_janela, textvariable=perfil_var)
                perfil_entry.pack()

                tk.Label(edit_janela, text="Nova Senha:").pack()
                senha_entry = tk.Entry(edit_janela, show="*")
                senha_entry.pack()

                def salvar_edicao():
                    novo_perfil = perfil_var.get().strip()
                    nova_senha = senha_entry.get().strip()

                    if novo_perfil == "":
                        messagebox.showerror("Erro", "O perfil não pode ser vazio.")
                        return

                    conn = conectar()
                    cursor = conn.cursor()
                    if nova_senha:
                        cursor.execute("UPDATE usuarios SET perfil = ?, senha = ? WHERE id = ?", (novo_perfil, nova_senha, usuario[0]))
                    else:
                        cursor.execute("UPDATE usuarios SET perfil = ? WHERE id = ?", (novo_perfil, usuario[0]))
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
                    edit_janela.destroy()
                    janela.destroy()
                    abrir_consultar_usuarios()

                tk.Button(edit_janela, text="Salvar", command=salvar_edicao).pack(pady=10)

            def remover_usuario(usuario_id):
                if messagebox.askyesno("Confirmação", "Tem certeza que deseja remover este usuário?"):
                    conn = conectar()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Sucesso", "Usuário removido com sucesso!")
                    janela.destroy()
                    abrir_consultar_usuarios()

            for i, usuario in enumerate(usuarios, start=1):
                id_, nome, perfil = usuario
                tk.Label(frame, text=id_, width=15, borderwidth=1, relief="solid").grid(row=i, column=0)
                tk.Label(frame, text=nome, width=15, borderwidth=1, relief="solid").grid(row=i, column=1)
                tk.Label(frame, text=perfil, width=15, borderwidth=1, relief="solid").grid(row=i, column=2)
                tk.Button(frame, text="Editar", command=lambda u=usuario: abrir_editar_usuario(u)).grid(row=i, column=3)
                tk.Button(frame, text="Remover", command=lambda u=usuario: remover_usuario(u[0])).grid(row=i, column=4)

            tk.Button(janela, text="Fechar", command=janela.destroy).pack(pady=10)

        tk.Button(root, text="Consultar Usuários", command=abrir_consultar_usuarios).pack()

    tk.Button(root, text="Sair", command=sair).pack(side='bottom', pady=10)

    root.mainloop()

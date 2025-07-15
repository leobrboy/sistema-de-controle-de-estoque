import sqlite3
from utils import criptografar_senha

def criar_usuario_default():
    conn = sqlite3.connect('estoque_db.sqlite3')
    cursor = conn.cursor()

    username = 'leo'
    password = 'leo123'
    nome = 'Administrador'
    perfil = 'admin'
    senha_hash = criptografar_senha(password)

    cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (username,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO usuarios (nome, usuario, senha, perfil) VALUES (?, ?, ?, ?)",
                       (nome, username, senha_hash, perfil))
        conn.commit()
        print("Usuário default criado com sucesso.")
    else:
        print("Usuário default já existe.")

    conn.close()

if __name__ == "__main__":
    criar_usuario_default()

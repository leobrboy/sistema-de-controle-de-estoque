import sqlite3

def criar_tabelas():
    conn = sqlite3.connect('estoque_db.sqlite3')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        usuario TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        perfil TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        minimo INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabelas()
    print("Tabelas criadas com sucesso.")

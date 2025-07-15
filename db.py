import sqlite3

def conectar():
    conn = sqlite3.connect('estoque_db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

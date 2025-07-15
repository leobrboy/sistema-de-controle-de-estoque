import sqlite3

def reorder_product_ids(db_path='estoque_db.sqlite3'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM produtos ORDER BY id")
    ids = [row[0] for row in cursor.fetchall()]

    new_id = 1
    for old_id in ids:
        cursor.execute("UPDATE produtos SET id = ? WHERE id = ?", (new_id, old_id))
        new_id += 1

    conn.commit()
    conn.close()

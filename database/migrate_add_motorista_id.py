import sqlite3
import os

DB_PATH = os.getenv('DB_PATH', 'frota.db')


def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    cols = [row[1] for row in cursor.fetchall()]
    return column in cols


def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Banco '{DB_PATH}' não encontrado. Rode 'python database/seed.py' primeiro.")
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if not column_exists(cur, 'veiculos', 'motorista_id'):
        try:
            cur.execute('ALTER TABLE veiculos ADD COLUMN motorista_id INTEGER')
            print('Coluna veiculos.motorista_id adicionada com sucesso.')
        except Exception as e:
            print('Erro ao adicionar coluna motorista_id:', e)
    else:
        print('Coluna veiculos.motorista_id já existe.')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    migrate()

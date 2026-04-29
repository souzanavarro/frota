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
    # adicionar valor_frete
    if not column_exists(cur, 'viagens', 'valor_frete'):
        try:
            cur.execute('ALTER TABLE viagens ADD COLUMN valor_frete REAL DEFAULT 0.0')
            print('Coluna viagens.valor_frete adicionada com sucesso.')
        except Exception as e:
            print('Erro ao adicionar coluna valor_frete:', e)
    else:
        print('Coluna viagens.valor_frete já existe.')

    # adicionar transportador_id
    if not column_exists(cur, 'viagens', 'transportador_id'):
        try:
            cur.execute('ALTER TABLE viagens ADD COLUMN transportador_id INTEGER')
            print('Coluna viagens.transportador_id adicionada com sucesso.')
        except Exception as e:
            print('Erro ao adicionar coluna transportador_id:', e)
    else:
        print('Coluna viagens.transportador_id já existe.')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    migrate()

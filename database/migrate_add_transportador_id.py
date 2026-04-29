import sqlite3
import os

DB_PATH = os.getenv('DB_PATH', 'frota.db')


def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    cols = [row[1] for row in cursor.fetchall()]
    return column in cols


def ensure_transportadores_table(cursor):
    # create transportadores table if not exists (basic schema)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transportadores (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      cnpj TEXT UNIQUE NOT NULL,
      nome_fantasia TEXT,
      telefone_contato TEXT,
      nome_pessoa_contato TEXT,
      nome_empresa TEXT,
      created_at DATETIME
    );
    ''')


def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Banco '{DB_PATH}' não encontrado. Rode 'python database/seed.py' primeiro.")
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    ensure_transportadores_table(cur)
    if not column_exists(cur, 'users', 'transportador_id'):
        try:
            cur.execute('ALTER TABLE users ADD COLUMN transportador_id INTEGER')
            print('Coluna users.transportador_id adicionada com sucesso.')
        except Exception as e:
            print('Erro ao adicionar coluna:', e)
    else:
        print('Coluna users.transportador_id já existe.')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    migrate()

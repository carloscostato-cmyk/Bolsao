import sqlite3
import os

DB = os.path.join(os.path.dirname(__file__), '..', 'sistema.db')
SQL = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'seed_pontos_bolsao.sql')

def load():
    if not os.path.exists(DB):
        print('Database not found:', DB)
        return
    if not os.path.exists(SQL):
        print('Seed SQL not found:', SQL)
        return
    with open(SQL, 'r', encoding='utf-8') as f:
        sql = f.read()
    conn = sqlite3.connect(DB)
    try:
        conn.executescript(sql)
        conn.commit()
        print('Seed loaded successfully')
    except Exception as e:
        print('Error loading seed:', e)
    finally:
        conn.close()

if __name__ == '__main__':
    load()

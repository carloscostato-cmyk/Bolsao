import sqlite3

def criar_banco():
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()

    # Tabela para "Pontos Bolsão" (Catálogo de Pacotes)
    # Inspirado na aba "Pontos Bolsão" do Excel
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pontos_bolsao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        point_pack_number TEXT NOT NULL UNIQUE,
        responsavel TEXT NOT NULL,
        projetos TEXT,
        pontos INTEGER NOT NULL,
        used_amount REAL DEFAULT 0,
        registration_date TEXT,
        expiration_date TEXT
    )
    ''')

    # Tabela para "Pontos utilizados" (Tabela de Consumo)
    # Inspirado na aba "Pontos utilizados" do Excel
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pontos_utilizados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bolsao_id INTEGER,
        serial_number TEXT NOT NULL,
        dados_cliente TEXT,
        product_model TEXT,
        valor_pontos_dia REAL NOT NULL,
        data_aplicacao TEXT NOT NULL,
        data_fim TEXT,
        FOREIGN KEY (bolsao_id) REFERENCES pontos_bolsao (id)
    )
    ''')

    # Tabela para "Base de Conciliação" (Base Oficial Fortinet)
    # Será populada via upload, mas a estrutura pode ser definida
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS base_conciliacao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        serial_number TEXT NOT NULL,
        description TEXT,
        usage_date TEXT,
        points REAL NOT NULL
    )
    ''')


    conn.commit()
    conn.close()
    print("Banco de dados 'sistema.db' e tabelas criados com sucesso.")

if __name__ == '__main__':
    criar_banco()

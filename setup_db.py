import sqlite3
CRIAR_CORTES = '''
CREATE TABLE IF NOT EXISTS  corte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_corte VARCHAR,
    preco DOUBLE,
    quantidade FLOAT
    );'''

CRIAR_VENDAS = """CREATE TABLE IF NOT EXISTS venda (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   data_venda DATETIME NOT NULL,
   corte_id INTEGER NOT NULL,
   quantidade FLOAT NOT NULL,
   valor_total DOUBLE NOT NULL,
   FOREIGN KEY (corte_id) REFERENCES corte(id)
);"""

CRIAR_COMPRAS = """CREATE TABLE IF NOT EXISTS compra (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    corte_id INT NOT NULL,
    quantidade FLOAT NOT NULL,
    data_entrada DATETIME NOT NULL,
    preco_kg DOUBLE NOT NULL,
    FOREIGN KEY(corte_id) REFERENCES corte(id)
);"""


def create_tables(db):
    cursor = db.cursor()
    cursor.execute(CRIAR_CORTES)
    cursor.execute(CRIAR_VENDAS)
    cursor.execute(CRIAR_COMPRAS)

    cursor.close()
    db.commit()


if __name__ == '__main__':
    connection = sqlite3.connect('acougue.db')
    print("Iniciando criação do banco de dados")
    create_tables(connection)
    print("Criação feita com sucesso!")

CREATE TABLE IF NOT EXISTS  corte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_corte VARCHAR,
    preco DOUBLE,
    quantidade FLOAT
);

CREATE TABLE IF NOT EXISTS venda (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   data_venda DATETIME NOT NULL,
   corte_id INTEGER NOT NULL,
   quantidade FLOAT NOT NULL,
   valor_total DOUBLE NOT NULL,
   FOREIGN KEY (corte_id) REFERENCES corte(id)
);

CREATE TABLE IF NOT EXISTS compra (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    corte_id INT NOT NULL,
    quantidade FLOAT NOT NULL,
    data_entrada DATETIME NOT NULL,
    preco_kg DOUBLE NOT NULL,
    FOREIGN KEY(corte_id) REFERENCES corte(id)
);


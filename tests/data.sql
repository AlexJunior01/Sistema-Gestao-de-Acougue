insert into corte(nome_corte, preco, quantidade) VALUES('Frango', 15.99, 2);
insert into corte(nome_corte, preco, quantidade) VALUES('Coxinha de Frango', 4.20, 50);

insert into venda(data_venda, corte_id, quantidade, valor_total) values ('2021-11-15', 1, 2, 35);
insert into venda(data_venda, corte_id, quantidade, valor_total) values ('2021-11-15', 2, 40, 100);

insert into compra(data_entrada, corte_id, quantidade, preco_kg) values ('2021-11-15', 1, 2, 35);
insert into compra(data_entrada, corte_id, quantidade, preco_kg) values ('2021-11-15', 2, 40, 20);


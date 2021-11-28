import pytest
from acougue.db import get_db


def test_resumo_vendas(client):
    resp = client.get('/vendas')
    assert client.get('/vendas').status_code == 200

    assert b'Frango' in resp.data
    assert b'Coxinha de Frango' in resp.data


def test_nova_venda_valida(client, app):
    old = 0
    data = {'id_corte': '1', 'peso': '10',
            'valor_total': '159.90'}
    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM venda').fetchone()[0]
        old = count
        assert count == 2

    client.post('/vendas', data=data)

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM venda').fetchone()[0]

        assert count > old
        assert count == 3


def test_nova_venda_com_peso_negativo(client, app):
    old = 0
    data = {'id_corte': '1', 'peso': '-10', 'valor_total': '159.90'}

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM venda').fetchone()[0]
        old = count

    client.post('/vendas', data=data)

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM venda').fetchone()[0]

        assert count == old
        assert count == 2


def test_nova_venda_com_id_invalido(client, app):
    old = 0
    data = {'id_corte': '1123214', 'peso': '10', 'valor_total': '159.90'}

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM venda').fetchone()[0]
        old = count

    client.post('/vendas', data=data)

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM venda').fetchone()[0]

        assert count == old
        assert count == 2


def test_calcula_venda_valido(client):
    resp = client.get('/vendas')
    assert b'31.98' not in resp.data

    data = {'id_corte': '1', 'peso': '2'}
    resp = client.post('/calcular_venda', data=data)

    assert b'31.98' in resp.data


def test_integracao_estoque(client, app):
    qtd_old = 0
    data = {'id_corte': '2', 'peso': '10',
            'valor_total': '159.90'}

    with app.app_context():
        db = get_db()
        qtd_old = db.execute('SELECT quantidade FROM corte WHERE id=2').fetchone()[0]

    client.post('/vendas', data=data)

    with app.app_context():
        db = get_db()
        qtd = db.execute('SELECT quantidade FROM corte WHERE id=2').fetchone()[0]

        assert qtd < qtd_old
        assert qtd == 40

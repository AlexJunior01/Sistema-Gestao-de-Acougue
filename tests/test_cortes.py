import pytest
from acougue.db import get_db


def test_resumo_cortes(client):
    resp = client.get('/cortes')
    assert client.get('/cortes').status_code == 200

    assert b'Frango' in resp.data
    assert b'Coxinha de Frango' in resp.data


def test_novo_corte_valido(client):
    client.post('/cortes', data={'corte': 'Alcatra', 'preco': '43.50'})

    resp = client.get('/cortes')
    assert b'Alcatra' in resp.data


def test_novo_corte_ja_existente(client, app):
    old = 0
    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM corte').fetchone()[0]
        old = count
        assert count == 2

    client.post('/cortes', data={'corte': 'Frango', 'preco': '43.50'})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM corte').fetchone()[0]
        assert count == old


def test_deletar_corte(client, app):
    old = 0
    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM corte').fetchone()[0]
        old = count

    client.post('/deletar_corte', data={'id': '1'})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM corte').fetchone()[0]
        assert old > count
        assert count == 1


def test_deletar_corte_inexistente(client, app):
    old = 0
    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM corte').fetchone()[0]
        old = count

    client.post('/deletar_corte', data={'id': '15'})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM corte').fetchone()[0]
        assert old == count


def test_atualizar_corte(client, app):
    client.post('/atualizar_corte', data={'id': '1', 'corte': 'Frango a passarinho'})

    with app.app_context():
        db = get_db()
        corte = db.execute('SELECT nome_corte FROM corte WHERE id=1').fetchone()[0]

        assert corte == 'Frango a passarinho'


def test_atualizar_corte_com_quantidade_negativo(client, app):
    with app.app_context():
        db = get_db()
        quantidade_antiga = db.execute('SELECT quantidade FROM corte WHERE id=1').fetchone()[0]

    client.post('/atualizar_corte', data={'id': '1', 'quantidade': '-5'})

    with app.app_context():
        db = get_db()
        quantidade = db.execute('SELECT quantidade FROM corte WHERE id=1').fetchone()[0]
        assert quantidade == quantidade_antiga


def test_atualizar_corte_com_preco_negativo(client, app):
    with app.app_context():
        db = get_db()
        preco_antigo = db.execute('SELECT preco FROM corte WHERE id=1').fetchone()[0]

    client.post('/atualizar_corte', data={'id': '1', 'preco': '-5'})

    with app.app_context():
        db = get_db()
        preco = db.execute('SELECT preco FROM corte WHERE id=1').fetchone()[0]
        assert preco == preco_antigo

from flask import Blueprint, redirect, render_template, request
from acougue.db import get_db

bp = Blueprint('vendas', __name__)


@bp.route("/vendas", methods=["GET", "POST"])
def vendas():
    if request.method == "POST":
        id_corte = request.form.get('id_corte')
        peso = request.form.get('peso')
        valor_total = request.form.get('valor_total')
        corte = db_recuperar_corte_por_id(id_corte)

        if corte:
            novo_peso = corte['quantidade'] - float(peso)
            db_insere_venda(id_corte, peso, valor_total)
            db_atualizar_estoque(id_corte, novo_peso)
        return redirect("/vendas")
    else:
        rows = db_recuperar_resumo_vendas()
        return render_template("vendas.html", vendas=rows)


@bp.route("/calcular_venda", methods=["GET", "POST"])
def calcula_venda():
    rows = db_recuperar_resumo_vendas()

    id_corte = request.form.get('id_corte')
    peso = request.form.get('peso')
    preco = db_recuperar_preco_do_corte(id_corte)
    valor_total = float(preco[0]) * float(peso)

    return render_template("vendas.html", vendas=rows, valor_total=valor_total, id_corte=id_corte, peso=peso)


@bp.route("/limpar_venda", methods=["GET", "POST"])
def limpar_venda():
    rows = db_recuperar_resumo_vendas()
    return render_template("vendas.html", vendas=rows, valor_total=0)


def db_insere_venda(id_corte, peso, valor_total):
    connection = get_db()
    sql = '''INSERT INTO venda(corte_id, quantidade, valor_total, data_venda) 
                VALUES(?, ?, ?, datetime('now'));'''
    connection.execute(sql, (id_corte, peso, valor_total))
    connection.commit()


def db_recuperar_corte_por_id(id):
    connection = get_db()
    result = connection.execute("SELECT * FROM corte WHERE id = ?;", (id,)).fetchone()
    return result


def db_atualizar_estoque(id_corte, novo_peso):
    connection = get_db()
    sql = '''UPDATE corte SET quantidade = ? WHERE id = ?'''
    connection.execute(sql, (novo_peso, id_corte))
    connection.commit()


def db_recuperar_resumo_vendas():
    connection = get_db()
    rows = connection.execute('''SELECT venda.id, data_venda, nome_corte, venda.quantidade, valor_total 
        FROM venda INNER JOIN corte ON venda.corte_id = corte.id
        ORDER BY venda.data_venda DESC LIMIT 5;''').fetchall()
    return rows


def db_recuperar_preco_do_corte(id_corte):
    connection = get_db()
    preco = connection.execute("SELECT preco FROM corte WHERE id = ?;", (id_corte,)).fetchone()

    return preco

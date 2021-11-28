import ctypes

from flask import Blueprint, redirect, render_template, request
from acougue.db import get_db

bp = Blueprint('compras', __name__)


@bp.route("/compras", methods=["GET", "POST"])
def compras():
    if request.method == "POST":
        id_corte = request.form.get('id_corte')
        peso = request.form.get('peso')
        preco = request.form.get('preco')
        corte = db_recuperar_corte_por_id(id_corte)

        if(float(peso) < 0):
            ctypes.windll.user32.MessageBoxW(0, "Peso não pode ter valor negativo", "Erro", 0)
        elif(float(preco) < 0):
            ctypes.windll.user32.MessageBoxW(0, "Preço não pode ter valor negativo", "Erro", 0)
        elif corte:
            novo_peso = corte['quantidade'] + float(peso)
            db_insere_compra(id_corte, peso, preco)
            db_atualizar_estoque(id_corte, novo_peso)
        else:
            ctypes.windll.user32.MessageBoxW(0, "Id de corte inexistente", "Erro", 0)

        return redirect("/compras")
    else:
        rows = db_recuperar_resumo_compras()
        return render_template("compras.html", compras=rows)


@bp.route("/calcular_compra", methods=["GET", "POST"])
def calcula_compra():
    rows = db_recuperar_resumo_compras()
    id_corte = request.form.get('id_corte')
    peso = request.form.get('peso')
    preco = request.form.get('preco')

    valor_total = float(preco) * float(peso)
    return render_template("compras.html", compras=rows, preco=preco, valor_total=valor_total, id_corte=id_corte,
                   peso=peso)


@bp.route("/limpar_compra", methods=["GET", "POST"])
def limpar_compra():
    rows = db_recuperar_resumo_compras()
    return render_template("compras.html", compras=rows, valor_total=0)


def db_insere_compra(id_corte, peso, preco):
    connection = get_db()
    sql = '''INSERT INTO compra(corte_id, quantidade, preco_kg, data_entrada) 
            VALUES(?, ?, ?, datetime('now'));'''
    connection.execute(sql, (id_corte, peso, preco))
    connection.commit()


def db_recuperar_resumo_compras():
    connection = get_db()
    rows = connection.execute('''SELECT compra.id, data_entrada, nome_corte, compra.quantidade, preco_kg FROM compra 
    INNER JOIN corte ON compra.corte_id = corte.id
    ORDER BY compra.data_entrada DESC LIMIT 5;''').fetchall()
    return rows


def db_recuperar_corte_por_id(id):
    connection = get_db()
    result = connection.execute("SELECT * FROM corte WHERE id = ?;", (id,)).fetchone()
    return result


def db_atualizar_estoque(id_corte, novo_peso):
    connection = get_db()
    sql = '''UPDATE corte SET quantidade = ? WHERE id = ?'''
    connection.execute(sql, (novo_peso, id_corte))
    connection.commit()

from flask import Blueprint, redirect, render_template, request, flash
from acougue.db import get_db

bp = Blueprint('relatorios', __name__, url_prefix='/relatorios')

@bp.route("/compras", methods=["GET", "POST"])
def relatorio_compras():
    if request.method == "POST":
        compras = db_buscar_compras(request.form.get('data_inicio'), request.form.get('data_fim'));
        return render_template("relatorio_compras.html", compras=compras)

    return render_template("relatorio_compras.html")


@bp.route("/vendas", methods=["GET", "POST"])
def relatorio_vendas():
    if request.method == "POST":
        vendas = db_buscar_vendas(request.form.get('data_inicio'), request.form.get('data_fim'));
        return render_template("relatorio_vendas.html", vendas=vendas)

    return render_template("relatorio_vendas.html")

@bp.route("/estoque", methods=["GET", "POST"])
def relatorio_estoque():
    if request.method == "POST":
        peso = request.form.get('peso')
        
        if not peso:
            flash("Peso não informado")
        elif (float(peso) < 0):
            flash("Peso não pode ser negativo")
        else:
            cortes = db_buscar_estoque(peso);
            return render_template("relatorio_estoque.html", cortes=cortes)

    return render_template("relatorio_estoque.html")


@bp.route("/", methods=["GET", "POST"])
def relatorios():
    return render_template("relatorios.html")


def db_buscar_compras(data_inicio, data_fim):
    connection = get_db()
    sql = '''SELECT compra.id, data_entrada, nome_corte, compra.quantidade, preco_kg FROM compra 
    INNER JOIN corte ON compra.corte_id = corte.id
    WHERE data_entrada BETWEEN ? and date(?, '+1 day') OR data_entrada BETWEEN ? and date(?, '+1 day')
    ORDER BY compra.data_entrada DESC;'''
    rows = connection.execute(sql, (data_inicio, data_fim, data_fim, data_inicio)).fetchall()
    return rows


def db_buscar_vendas(data_inicio, data_fim):
    connection = get_db()
    sql = '''SELECT venda.id, data_venda, nome_corte, venda.quantidade, valor_total FROM venda 
    INNER JOIN corte ON venda.corte_id = corte.id
    WHERE data_venda BETWEEN ? and date(?, '+1 day') OR data_venda BETWEEN ? and date(?, '+1 day')
    ORDER BY venda.data_venda DESC;'''

    rows = connection.execute(sql, (data_inicio, data_fim, data_fim, data_inicio)).fetchall()
    return rows

def db_buscar_estoque(peso):
    connection = get_db()
    sql = '''SELECT nome_corte, quantidade FROM corte 
    WHERE quantidade <= ?
    ORDER BY quantidade;'''

    rows = connection.execute(sql, (peso, )).fetchall()
    return rows

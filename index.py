import sqlite3
from flask import Flask, render_template, request, redirect
import os
from contextlib import closing

currentDirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
db = sqlite3.connect('acougue.db')
db.row_factory = sqlite3.Row


def get_corte_id(id):
    with closing(sqlite3.connect("acougue.db")) as connection:
        with closing(connection.cursor()) as cursor:
            result = cursor.execute("SELECT id FROM corte WHERE id = ?;", (id,)).fetchone()
    return result


def insert_corte(corte, preco):
    with closing(sqlite3.connect("acougue.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("INSERT INTO corte(nome_corte, preco, quantidade) VALUES(?, ?, 0)",
                           (corte, preco))
            connection.commit()


def deletar_corte_db(id_corte):
    with closing(sqlite3.connect("acougue.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("DELETE FROM corte WHERE id = ?;", (id_corte,))
            connection.commit()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect("/")

    else:
        # insert_corte()
        return render_template("tela_inicial.html")


def get_resumo_vendas():
    with closing(sqlite3.connect("acougue.db")) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            rows = connection.execute('''SELECT venda.id, data_venda, nome_corte, venda.quantidade, valor_total FROM venda 
            INNER JOIN corte ON venda.corte_id = corte.id
            ORDER BY venda.data_venda DESC LIMIT 5;''').fetchall()
    return rows


def insere_venda(id_corte, peso, valor_total, cursor):
    sql = '''INSERT INTO venda(corte_id, quantidade, valor_total, data_venda) 
            VALUES(?, ?, ?, datetime('now'));'''
    cursor.execute(sql, (id_corte, peso, valor_total))


def nova_venda(id_corte, peso, valor_total):
    print(id_corte)
    print(peso)
    print(valor_total)
    with closing(sqlite3.connect("acougue.db")) as connection:
        with closing(connection.cursor()) as cursor:
            corte = get_corte_id(id_corte)
            if corte:
                insere_venda(id_corte, peso, valor_total, cursor)
                connection.commit()


@app.route("/vendas", methods=["GET", "POST"])
def vendas():
    if request.method == "POST":
        nova_venda(request.form.get('id_corte'), request.form.get('peso'), request.form.get('valor_total'))
        return redirect("/vendas")
    else:
        rows = get_resumo_vendas()
        return render_template("vendas.html", vendas=rows)


@app.route("/calcular_venda", methods=["GET", "POST"])
def calcula_venda():
    with closing(sqlite3.connect("acougue.db")) as connection:
        with closing(connection.cursor()) as cursor:
            rows = get_resumo_vendas()

            id_corte = request.form.get('id_corte')
            peso = request.form.get('peso')

            preco = cursor.execute("SELECT preco FROM corte WHERE id = ?;", (id_corte,)).fetchone()

            valor_total = float(preco[0]) * float(peso)

    return render_template("vendas.html", vendas=rows, valor_total=valor_total, id_corte=id_corte, peso=peso)


@app.route("/limpar_venda", methods=["GET", "POST"])
def limpar_venda():
    with closing(sqlite3.connect("acougue.db")) as connection:
        with closing(connection.cursor()) as cursor:
            rows = get_resumo_vendas()

    return render_template("vendas.html", vendas=rows, valor_total=0)


@app.route("/compras", methods=["GET", "POST"])
def compras():
    return render_template("compras.html")


@app.route("/cortes", methods=["GET", "POST"])
def cortes():
    if request.method == "POST":
        insert_corte(request.form.get('corte'), request.form.get('preco'))
        return redirect("/cortes")
    else:
        with closing(sqlite3.connect("acougue.db")) as connection:
            with closing(connection.cursor()) as cursor:
                rows = cursor.execute("SELECT * FROM corte;").fetchall()

        return render_template("cortes.html", carnes=rows)


@app.route("/deletar_corte", methods=["GET", "POST"])
def deletar_corte():
    if request.method == "POST":
        deletar_corte_db(request.form.get('id'))
        return redirect("/cortes")

    return redirect("/cortes")


@app.route("/atualizar_corte", methods=["GET", "POST"])
def atualizar_corte():
    if request.method == "POST":
        id = request.form.get('id')
        corte = request.form.get('corte')
        preco = request.form.get('preco')
        quantidade = request.form.get('quantidade')

        with closing(sqlite3.connect("acougue.db")) as connection:
            with closing(connection.cursor()) as cursor:
                if corte:
                    cursor.execute("UPDATE corte SET nome_corte = ? WHERE id = ?", (corte, id,))
                if preco:
                    cursor.execute("UPDATE corte SET preco = ? WHERE id = ?", (preco, id,))
                if quantidade:
                    cursor.execute("UPDATE corte SET quantidade = ? WHERE id = ?", (quantidade, id,))
                connection.commit()

        return redirect("/cortes")

    return redirect("/cortes")


@app.route("/relatorios", methods=["GET", "POST"])
def relatorios():
    return render_template("relatorios.html")


if __name__ == "__main__":
    app.run(debug=True)

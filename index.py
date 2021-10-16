import sqlite3
from flask import Flask, render_template, request, redirect
import os
from contextlib import closing

currentDirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
db = sqlite3.connect('acougue.db')


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


@app.route("/vendas", methods=["GET", "POST"])
def vendas():
    return render_template("vendas.html")


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

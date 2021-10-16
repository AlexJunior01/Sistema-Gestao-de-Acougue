import sqlite3
from flask import Flask, render_template, request, redirect
import os
from contextlib import closing

currentDirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
db = sqlite3.connect('acougue.db')


def insert_corte(corte, preco, quantidade):
    with closing(sqlite3.connect("acougue.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("INSERT INTO corte(nome_corte, preco, quantidade) VALUES(?, ?, ?)",
                           (corte, preco, quantidade))
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
        insert_corte(request.form.get('corte'), request.form.get('preco'), request.form.get('quantidade'))
        return redirect("/cortes")
    else:
        with closing(sqlite3.connect("acougue.db")) as connection:
            with closing(connection.cursor()) as cursor:
                rows = cursor.execute("SELECT * FROM corte;").fetchall()

        return render_template("cortes.html", carnes=rows)


@app.route("/relatorios", methods=["GET", "POST"])
def relatorios():
    return render_template("relatorios.html")


if __name__ == "__main__":
    app.run(debug=True)

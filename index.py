import sqlite3
from flask import Flask, render_template, request, redirect
import os

currentDirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    connection = sqlite3.connect(currentDirectory + "/acougue.db")
    db = connection.cursor()
    
    if request.method == "POST":
        return redirect("/")

    else:
        return render_template("tela_inicial.html", people=people)


@app.route("/vendas", methods=["GET", "POST"])
def vendas():
	return render_template("vendas.html")


@app.route("/compras", methods=["GET", "POST"])
def compras():
	return render_template("compras.html")


@app.route("/cortes", methods=["GET", "POST"])
def cortes():
	return render_template("cortes.html")


@app.route("/relatorios", methods=["GET", "POST"])
def relatorios():
	return render_template("relatorios.html")


if __name__ == "__main__":
	app.run(debug=True)

from flask import Blueprint, redirect, render_template, request
from acougue.db import get_db

bp = Blueprint('cortes', __name__, )


@bp.route("/deletar_corte", methods=["GET", "POST"])
def deletar_corte():
    if request.method == "POST":
        db_deletar_corte(request.form.get('id'))
        return redirect("/cortes")

    return redirect("/cortes")


@bp.route("/atualizar_corte", methods=["GET", "POST"])
def atualizar_corte():
    if request.method == "POST":
        id = request.form.get('id')
        corte = request.form.get('corte')
        preco = request.form.get('preco')
        quantidade = request.form.get('quantidade')

        db_atualizar_corte(id, corte, preco, quantidade)
        return redirect("/cortes")

    return redirect("/cortes")


@bp.route("/cortes", methods=["GET", "POST"])
def cortes():
    if request.method == "POST":
        db_inserir_corte(request.form.get('corte'), request.form.get('preco'))
        return redirect("/cortes")
    else:
        rows = db_recuperar_cortes()
        return render_template("cortes.html", carnes=rows)


def db_recuperar_cortes():
    connection = get_db()
    rows = connection.execute("SELECT * FROM corte;").fetchall()
    return rows


def db_inserir_corte(corte, preco):
    connection = get_db()
    connection.execute("INSERT INTO corte(nome_corte, preco, quantidade) VALUES(?, ?, 0)",
                       (corte, preco))
    connection.commit()


def db_deletar_corte(id_corte):
    connection = get_db()
    connection.execute("DELETE FROM corte WHERE id = ?;", (id_corte,))
    connection.commit()


def db_atualizar_corte(id, corte, preco, quantidade):
    connection = get_db()
    if corte:
        connection.execute("UPDATE corte SET nome_corte = ? WHERE id = ?", (corte, id,))
    if preco:
        connection.execute("UPDATE corte SET preco = ? WHERE id = ?", (preco, id,))
    if quantidade:
        connection.execute("UPDATE corte SET quantidade = ? WHERE id = ?", (quantidade, id,))
    connection.commit()

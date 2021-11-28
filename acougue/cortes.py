from flask import Blueprint, redirect, render_template, request, flash

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
    if db_verifica_existencia_corte(corte):
        redirect('/cortes')
    else:
        connection = get_db()
        connection.execute("INSERT INTO corte(nome_corte, preco, quantidade) VALUES(?, ?, 0)",
                           (corte, preco))
        connection.commit()


def db_deletar_corte(id_corte):
    
    result = db_recuperar_corte_por_id(id_corte)
    
    if(not(result)):
        flash(f'Impossível remover corte! ID {id_corte} não existe', 'error')
        return redirect("/cortes")

    connection = get_db()
    connection.execute("DELETE FROM corte WHERE id = ?;", (id_corte,))
    connection.commit()
    
    return redirect("/cortes")


def db_atualizar_corte(id, corte, preco, quantidade):
    connection = get_db()
    if corte:
        result = db_recuperar_corte_por_id(id)
        if result:
            connection.execute("UPDATE corte SET nome_corte = ? WHERE id = ?", (corte, id,))
        else:
            flash(f"Não foi possível atualizar corte, Id {id} não existe", "Erro")
    if preco:
        if (float(preco) > 0):
            connection.execute("UPDATE corte SET preco = ? WHERE id = ?", (preco, id,))
        else:
            flash("Não foi possível atualizar corte, preço deve ser maior do que zero", "Erro")
    if quantidade:
        if (float(quantidade) > 0):
            connection.execute("UPDATE corte SET quantidade = ? WHERE id = ?", (quantidade, id,))
        else:
            flash("Não foi possível atualizar corte, quantidade deve ser maior do que zero", "Erro")
    connection.commit()


def db_verifica_existencia_corte(corte):
    connection = get_db()
    result = connection.execute("SELECT nome_corte FROM corte;").fetchall()

    for resultado in result:
        if(resultado['nome_corte'].lower() == corte.lower()):
            flash("Corte já existe", "Erro")
            return True
    return False


def db_recuperar_corte_por_id(id):
    connection = get_db()
    result = connection.execute("SELECT * FROM corte WHERE id = ?;", (id,)).fetchone()
    return result

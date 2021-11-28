import sqlite3
from flask import Flask, render_template, request, redirect
import os
from contextlib import closing
import ctypes  

currentDirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
db = sqlite3.connect('acougue.db')
db.row_factory = sqlite3.Row


def get_corte_id(id):
    with closing(sqlite3.connect("acougue.db")) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            result = cursor.execute("SELECT * FROM corte WHERE id = ?;", (id,)).fetchone()
    return result

def verifica_existencia_corte(corte):
    with closing(sqlite3.connect("acougue.db")) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            result = cursor.execute("SELECT nome_corte FROM corte;").fetchall()
    for resultado in result:
        if(resultado['nome_corte'].lower() == corte.lower()):
            ctypes.windll.user32.MessageBoxW(0, "Corte já existente", "Erro", 0)
            return True
    return False



def insert_corte(corte, preco):
    if (verifica_existencia_corte(corte)):
        return redirect("/cortes")
    else:
        with closing(sqlite3.connect("acougue.db")) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("INSERT INTO corte(nome_corte, preco, quantidade) VALUES(?, ?, 0)",
                           (corte, preco))
                connection.commit()


def deletar_corte_db(id_corte):
    try:
        result = get_corte_id(id)
        with closing(sqlite3.connect("acougue.db")) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("DELETE FROM corte WHERE id = ?;", (id_corte,))
                connection.commit()
    except:
        ctypes.windll.user32.MessageBoxW(0, "Não foi possível remover corte, Id corte inexistente", "Erro", 0)
        return redirect("/cortes")


def atualizar_estoque(id_corte, novo_peso, cursor):
    sql = '''UPDATE corte SET quantidade = ? WHERE id = ?'''
    cursor.execute(sql, (novo_peso, id_corte))

################################################################ INDEX ################################################################
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect("/")

    else:
        return render_template("tela_inicial.html")



################################################################ VENDAS ################################################################
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
    with closing(sqlite3.connect("acougue.db")) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            corte = get_corte_id(id_corte)
            if corte:
                novo_peso = corte['quantidade'] - float(peso)
                insere_venda(id_corte, peso, valor_total, cursor)
                atualizar_estoque(id_corte, novo_peso, cursor)
                connection.commit()

def buscar_vendas(data_inicio, data_fim):
    with closing(sqlite3.connect("acougue.db")) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
       	    rows = connection.execute('''SELECT venda.id, data_venda, nome_corte, venda.quantidade, valor_total FROM venda 
            INNER JOIN corte ON venda.corte_id = corte.id
            WHERE data_venda BETWEEN ? and date(?, '+1 day') OR data_venda BETWEEN ? and date(?, '+1 day')
            ORDER BY venda.data_venda DESC;''', (data_inicio, data_fim, data_fim, data_inicio)).fetchall()
    return rows


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

            try:
                preco = cursor.execute("SELECT preco FROM corte WHERE id = ?;", (id_corte,)).fetchone()
                valor_total = float(preco[0]) * float(peso)
            except:
                ctypes.windll.user32.MessageBoxW(0, "Id de corte inexistente", "Erro", 0)
                return render_template("vendas.html", vendas=rows)

    return render_template("vendas.html", vendas=rows, valor_total=valor_total, id_corte=id_corte, peso=peso)


@app.route("/limpar_venda", methods=["GET", "POST"])
def limpar_venda():
    with closing(sqlite3.connect("acougue.db")) as connection:
        with closing(connection.cursor()) as cursor:
            rows = get_resumo_vendas()

    return render_template("vendas.html", vendas=rows, valor_total=0)


############################################### COMPRAS ##################################################################
def get_resumo_compras():
    with closing(sqlite3.connect("acougue.db")) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            rows = connection.execute('''SELECT compra.id, data_entrada, nome_corte, compra.quantidade, preco_kg FROM compra 
            INNER JOIN corte ON compra.corte_id = corte.id
            ORDER BY compra.data_entrada DESC LIMIT 5;''').fetchall()
    return rows

def insere_compra(id_corte, peso, preco, cursor):
    sql = '''INSERT INTO compra(corte_id, quantidade, preco_kg, data_entrada) 
            VALUES(?, ?, ?, datetime('now'));'''
    cursor.execute(sql, (id_corte, peso, preco))


def nova_compra(id_corte, peso, preco):
    with closing(sqlite3.connect("acougue.db")) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
            corte = get_corte_id(id_corte)
            if corte:
                novo_peso = corte['quantidade'] + float(peso)
                insere_compra(id_corte, peso, preco, cursor)
                atualizar_estoque(id_corte, novo_peso, cursor)
                connection.commit()
            else:
                ctypes.windll.user32.MessageBoxW(0, "Id de corte inexistente", "Erro", 0)

def buscar_compras(data_inicio, data_fim):
    with closing(sqlite3.connect("acougue.db")) as connection:
        connection.row_factory = sqlite3.Row
        with closing(connection.cursor()) as cursor:
       	    rows = connection.execute('''SELECT compra.id, data_entrada, nome_corte, compra.quantidade, preco_kg FROM compra 
            INNER JOIN corte ON compra.corte_id = corte.id
            WHERE data_entrada BETWEEN ? and date(?, '+1 day') OR data_entrada BETWEEN ? and date(?, '+1 day')
            ORDER BY compra.data_entrada DESC;''', (data_inicio, data_fim, data_fim, data_inicio)).fetchall()
    return rows

@app.route("/compras", methods=["GET", "POST"])
def compras():
    if request.method == "POST":
        nova_compra(request.form.get('id_corte'), request.form.get('peso'), request.form.get('preco'))
        return redirect("/compras")
    else:
        rows = get_resumo_compras()
        return render_template("compras.html", compras=rows)


@app.route("/calcular_compra", methods=["GET", "POST"])
def calcula_compra():
    with closing(sqlite3.connect("acougue.db")) as connection:
        with closing(connection.cursor()) as cursor:
            rows = get_resumo_compras()

            id_corte = request.form.get('id_corte')
            peso = request.form.get('peso')
            preco = request.form.get('preco')

            valor_total = float(preco) * float(peso)

    return render_template("compras.html", compras=rows, preco=preco, valor_total=valor_total, id_corte=id_corte, peso=peso)


@app.route("/limpar_compra", methods=["GET", "POST"])
def limpar_compra():
    with closing(sqlite3.connect("acougue.db")) as connection:
        with closing(connection.cursor()) as cursor:
            rows = get_resumo_compras()

    return render_template("compras.html", compras=rows, valor_total=0)


################################################################ CORTES ################################################################

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
                    result = get_corte_id(id)
                    if(result):
                        cursor.execute("UPDATE corte SET nome_corte = ? WHERE id = ?", (corte, id,))
                    else:
                        ctypes.windll.user32.MessageBoxW(0, "Não foi possível atualizar corte, Id de corte inexistente", "Erro", 0)
                if preco:
                    if (float(preco) > 0):
                        cursor.execute("UPDATE corte SET preco = ? WHERE id = ?", (preco, id,))
                    else:
                        ctypes.windll.user32.MessageBoxW(0, "Não foi possível atualizar corte, preço deve ser maior do que zero", "Erro", 0)
                if quantidade:
                    if (float(quantidade) > 0):
                        cursor.execute("UPDATE corte SET quantidade = ? WHERE id = ?", (quantidade, id,))
                    else:
                        ctypes.windll.user32.MessageBoxW(0, "Não foi possível atualizar corte, quantidade deve ser maior do que zero", "Erro", 0)
                connection.commit()

        return redirect("/cortes")

    return redirect("/cortes")


################################################################ RELATORIOS ################################################################

@app.route("/relatorio_compras", methods=["GET", "POST"])
def relatorio_compras():
    if request.method == "POST":
        compras = buscar_compras(request.form.get('data_inicio'), request.form.get('data_fim'));
        return render_template("relatorio_compras.html", compras=compras)

    return render_template("relatorio_compras.html")


@app.route("/relatorio_vendas", methods=["GET", "POST"])
def relatorio_vendas():
    if request.method == "POST":
        vendas = buscar_vendas(request.form.get('data_inicio'), request.form.get('data_fim'));
        return render_template("relatorio_vendas.html", vendas=vendas)

    return render_template("relatorio_vendas.html")


@app.route("/relatorios", methods=["GET", "POST"])
def relatorios():
    return render_template("relatorios.html")


if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, render_template, request, redirect
import os
from . import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'acougue.db'),
    )

    app.config.from_pyfile('config.py', silent=True)

    def recuperar_cortes():
        connection = db.get_db()
        rows = connection.execute("SELECT * FROM corte;").fetchall()
        return rows

    def get_corte_id(id):
        connection = db.get_db()
        result = connection.execute("SELECT * FROM corte WHERE id = ?;", (id,)).fetchone()
        return result

    def insert_corte(corte, preco):
        connection = db.get_db()
        connection.execute("INSERT INTO corte(nome_corte, preco, quantidade) VALUES(?, ?, 0)",
                           (corte, preco))
        connection.commit()

    def deletar_corte_db(id_corte):
        connection = db.get_db()
        connection.execute("DELETE FROM corte WHERE id = ?;", (id_corte,))
        connection.commit()

    def atualizar_estoque(id_corte, novo_peso):
        connection = db.get_db()
        sql = '''UPDATE corte SET quantidade = ? WHERE id = ?'''
        connection.execute(sql, (novo_peso, id_corte))

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            return redirect("/")
        else:
            return render_template("tela_inicial.html")

    def get_resumo_vendas():
        connection = db.get_db()
        rows = connection.execute('''SELECT venda.id, data_venda, nome_corte, venda.quantidade, valor_total 
            FROM venda INNER JOIN corte ON venda.corte_id = corte.id
            ORDER BY venda.data_venda DESC LIMIT 5;''').fetchall()
        return rows

    def insere_venda(id_corte, peso, valor_total):
        connection = db.get_db()
        sql = '''INSERT INTO venda(corte_id, quantidade, valor_total, data_venda) 
                    VALUES(?, ?, ?, datetime('now'));'''
        connection.execute(sql, (id_corte, peso, valor_total))

    def nova_venda(id_corte, peso, valor_total):
        connection = db.get_db()
        corte = get_corte_id(id_corte)
        if corte:
            novo_peso = corte['quantidade'] - float(peso)
            insere_venda(id_corte, peso, valor_total)
            atualizar_estoque(id_corte, novo_peso)
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
        connection = db.get_db()
        rows = get_resumo_vendas()

        id_corte = request.form.get('id_corte')
        peso = request.form.get('peso')
        preco = connection.execute("SELECT preco FROM corte WHERE id = ?;", (id_corte,)).fetchone()
        valor_total = float(preco[0]) * float(peso)

        return render_template("vendas.html", vendas=rows, valor_total=valor_total, id_corte=id_corte, peso=peso)

    @app.route("/limpar_venda", methods=["GET", "POST"])
    def limpar_venda():
        rows = get_resumo_vendas()
        return render_template("vendas.html", vendas=rows, valor_total=0)

    ############################################## COMPRAS ##################################################################
    def get_resumo_compras():
        connection = db.get_db()
        rows = connection.execute('''SELECT compra.id, data_entrada, nome_corte, compra.quantidade, preco_kg FROM compra 
        INNER JOIN corte ON compra.corte_id = corte.id
        ORDER BY compra.data_entrada DESC LIMIT 5;''').fetchall()
        return rows

    def insere_compra(id_corte, peso, preco):
        connection = db.get_db()
        sql = '''INSERT INTO compra(corte_id, quantidade, preco_kg, data_entrada) 
                VALUES(?, ?, ?, datetime('now'));'''
        connection.execute(sql, (id_corte, peso, preco))

    def nova_compra(id_corte, peso, preco):
        connection = db.get_db()
        corte = get_corte_id(id_corte)
        if corte:
            novo_peso = corte['quantidade'] + float(peso)
            insere_compra(id_corte, peso, preco)
            atualizar_estoque(id_corte, novo_peso)
            connection.commit()

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

        rows = get_resumo_compras()

        id_corte = request.form.get('id_corte')
        peso = request.form.get('peso')
        preco = request.form.get('preco')

        valor_total = float(preco) * float(peso)
        return render_template("compras.html", compras=rows, preco=preco, valor_total=valor_total, id_corte=id_corte,
                       peso=peso)

    @app.route("/limpar_compra", methods=["GET", "POST"])
    def limpar_compra():
        rows = get_resumo_compras()
        return render_template("compras.html", compras=rows, valor_total=0)

    @app.route("/cortes", methods=["GET", "POST"])
    def cortes():
        if request.method == "POST":
            insert_corte(request.form.get('corte'), request.form.get('preco'))
            return redirect("/cortes")
        else:
            rows = recuperar_cortes()
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

            connection = db.get_db()
            if corte:
                connection.execute("UPDATE corte SET nome_corte = ? WHERE id = ?", (corte, id,))
            if preco:
                connection.execute("UPDATE corte SET preco = ? WHERE id = ?", (preco, id,))
            if quantidade:
                connection.execute("UPDATE corte SET quantidade = ? WHERE id = ?", (quantidade, id,))
            connection.commit()

            return redirect("/cortes")

        return redirect("/cortes")

    @app.route("/relatorios", methods=["GET", "POST"])
    def relatorios():
        return render_template("relatorios.html")

    @app.route("/relatorio_compras", methods=["GET", "POST"])
    def relatorio_compras():
        return render_template("relatorio_compras.html")


    @app.route("/relatorio_vendas", methods=["GET", "POST"])
    def relatorio_vendas():
        return render_template("relatorio_vendas.html")


    db.init_app(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

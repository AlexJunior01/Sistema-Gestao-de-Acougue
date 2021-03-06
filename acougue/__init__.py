from flask import Flask, render_template, request, redirect
import os
from . import db, cortes, vendas, compras, relatorios


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'acougue.db'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

        # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            return redirect("/")
        else:
            return render_template("tela_inicial.html")

    db.init_app(app)
    app.register_blueprint(cortes.bp)
    app.register_blueprint(vendas.bp)
    app.register_blueprint(compras.bp)
    app.register_blueprint(relatorios.bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

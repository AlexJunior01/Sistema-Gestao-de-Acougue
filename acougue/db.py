import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        print(f"Database {current_app.config['DATABASE']}\n\n")
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Conecta com o banco de dados e roda o script de criação"""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Configuração de comando para iniciar o banco de dados"""
    click.echo("Iniciando criação do banco de dados")
    init_db()
    click.echo("Banco criado")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
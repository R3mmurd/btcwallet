""" BTC Wallet

This file functions to handle the database.

Author: Alejandro Mujica (aledrums@gmail.com)
"""
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """
    Get a database connection.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    Close the database connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    Execute the script that creates the database structure.
    """
    db = get_db()

    with current_app.open_resource('btcwallet.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Command to create the database structure.
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

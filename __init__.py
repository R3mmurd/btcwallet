""" BTC Wallet

This file contains project configuration.

Author: Alejandro Mujica (aledrums@gmail.com)
"""
import os

from flask import Flask, render_template, g

from .src.helpers import btc

from bit import PrivateKeyTestnet


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join('btcwallet.db'),
        TEMPLATES_AUTO_RELOAD=True,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    from .src import db, auth, wallet, history
    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(wallet.bp)
    app.register_blueprint(history.bp)

    @app.after_request
    def after_request(response):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Expires'] = 0
        response.headers['Pragma'] = 'no-cache'
        return response

    @app.route('/')
    @auth.login_required
    def index():
        user = g.user
        wallets = db.get_db().execute(
            'SELECT * FROM wallets WHERE user_id = ?', (user['id'],)
        ).fetchall()

        wallets = [
            {
                '#': i,
                'id': wallet['id'],
                'name': wallet['name'],
                'address': wallet['address'],
                'balance': PrivateKeyTestnet(wallet['wif']).get_balance('btc')
            } for i, wallet in enumerate(wallets)
        ]

        return render_template('index.html', username=user['username'], wallets=wallets)

    return app


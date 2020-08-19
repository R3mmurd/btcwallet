""" BTC Wallet

This file contains the controller to handle transaction history.

Author: Alejandro Mujica (aledrums@gmail.com)
"""
from datetime import datetime

from flask import Blueprint, g, render_template

from .auth import login_required
from .db import get_db
from .helpers import btc


bp = Blueprint('history', __name__, url_prefix='/history')

@bp.route("/")
@login_required
def history():
    db = get_db()
    query = (
        'SELECT t.address_to, t.amount, t.datetime, t.transaction_id '
        'FROM transactions as t INNER JOIN wallets as w ON w.id = t.wallet_id '
        "WHERE w.user_id = ?"
    )
    rows = db.execute(query,(g.user['id'],)).fetchall()
    rows = [
        {
            '#': i,
            'transaction_id': row['transaction_id'],
            'address_to': row['address_to'],
            'amount': btc(row['amount']),
            'datetime': datetime.fromisoformat(
                row["datetime"]
            ).strftime("%b %d, %Y %I:%M:%S")

        } for i, row in enumerate(rows)
    ]
    return render_template('history.html', rows=rows)

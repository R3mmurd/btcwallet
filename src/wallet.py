""" BTC Wallet

This file contains the controllers to handle wallets.

Author: Alejandro Mujica (aledrums@gmail.com)
"""
from datetime import datetime
from decimal import Decimal, InvalidOperation

from flask import (
    Blueprint, flash, g, redirect, url_for, render_template, request
)

from werkzeug.security import check_password_hash

from .auth import login_required
from .db import get_db

from bit import PrivateKeyTestnet


bp = Blueprint('wallet', __name__, url_prefix='/wallet')


@bp.route("/", methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']

        if not name:
            flash('Name is required.', 'danger')
            return redirect(url_for('wallet.create'))

        db = get_db()
        key = PrivateKeyTestnet()
        db.execute(
            'INSERT INTO wallets (name, address, wif, user_id) VALUES (?, ?, ?, ?)',
            (name, key.address, key.to_wif(), g.user['id'])
        )
        db.commit()
        
        flash('Wallet created successfully', 'success')
        return redirect(url_for('index'))
    
    return render_template('wallet/create.html')


@bp.route("/<wallet_id>", methods=('GET', 'POST',))
@login_required
def delete(wallet_id):
    if request.method == 'POST':
        password = request.form['password']
        error = ''
        if not password:
            error = 'Password is required.'
        elif not (check_password_hash(g.user['password'], password)):
            error = 'Incorrect password.'
        
        if error:
            flash(error, 'danger')
            return redirect(url_for('wallet.delete', wallet_id=wallet_id))

        db = get_db()
        db.execute('DELETE FROM wallets WHERE id = ?', (wallet_id,))
        db.commit()
        flash('Wallet deleted successfully', 'success')
        return redirect(url_for('index'))
    
    wallet = get_db().execute(
        "SELECT * FROM wallets WHERE id = ?", (wallet_id,)
    ).fetchone()
    key = PrivateKeyTestnet(wallet['wif']) 
    balance = key.get_balance('btc')
    return render_template('wallet/delete.html', wallet_id=wallet_id, balance=balance)


@bp.route("/send/<wallet_id>", methods=('GET', 'POST'))
@login_required
def send(wallet_id):
    db = get_db()
    wallet = db.execute(
        "SELECT * FROM wallets WHERE id = ?", (wallet_id,)
    ).fetchone()
    key = PrivateKeyTestnet(wallet['wif']) 
    balance = key.get_balance('btc')

    if request.method == 'POST':
        dest_address = request.form['dest_address']
        amount = request.form['amount']
        password = request.form['password']
        error = ''

        if not dest_address:
            error = 'Destination Address is required'
        elif not amount:
            error = 'Amount is required'
        elif not password:
            error = 'Password is required'
        else:
            try:
                amount = Decimal(amount)

                if amount <= 0:
                    raise ValueError

            except (InvalidOperation, ValueError):
                error = 'Amount must be real number greater than zero'
        
        if not error and not (check_password_hash(g.user['password'], password)):
            error = 'Incorrect password.'
        elif not error and amount > Decimal(balance):
            error = 'There is not enough balance in the wallet.'
        
        if error:
            flash(error, 'danger')
            return redirect(url_for('wallet.send', wallet_id=wallet_id))

        tx_hash = key.send([(dest_address, amount, 'btc')])

        db.execute(
            'INSERT INTO transactions (address_to, amount, transaction_id, wallet_id, datetime) VALUES (?, ?, ?, ?, ?)',
            (dest_address, float(amount), tx_hash, wallet_id, datetime.now().isoformat(' '))
        )
        db.commit()
        msg = (f'You have sent {amount} BTC successfully'
                f' to the    address: {dest_address}.'
                f' Tx hash: {tx_hash}')
        flash(msg, 'success')
        return redirect(url_for("index"))
            

    return render_template('wallet/send.html', wallet=wallet, balance=balance)

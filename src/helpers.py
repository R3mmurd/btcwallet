""" BTC Wallet

This file contains helpers funtions to format values by currency type.

Author: Alejandro Mujica (aledrums@gmail.com)
"""


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def btc(value):
    """Format value as BTC."""
    return f"{value:,.8f}"
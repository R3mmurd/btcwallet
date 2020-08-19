# BTC Wallet

This is a small web application that allows users to create and handle [Bitcoins](https://bitcoin.org/en/) wallets.
This app only works on [Testnet](https://en.bitcoin.it/wiki/Testnet).

## Installing the app in development mode

- Clone this repository: `git clone git@github.com:R3mmurd/btcwallet.git`.
- Locate inside the downloaded directory: `cd btcwallet`.
- Create a virtual environment. For example: `python3 -m venv env`.
- Activate the virtual environment. For example: `source env/bin/activate`.
- Install the requirements: `pip install -r requirements.txt`
- Set the following variables:

    ```bash
        export FLASK_APP=.
        export FLASK_ENV=development
    ```

- Init the database: `flask init-db`.
- Run the server: `flask run`.


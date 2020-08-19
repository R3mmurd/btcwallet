-- Remove existing indices
DROP INDEX IF EXISTS idx_user_username;
DROP INDEX IF EXISTS idx_wallet_user_id;
DROP INDEX IF EXISTS idx_trasanctions_user_id;

-- Remove existing tables
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS wallets;
DROP TABLE IF EXISTS transactions;

-- Table  for users
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

-- Unique index for username
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- Table for wallets
CREATE TABLE wallets (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    wif TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE NO ACTION
);

-- Index for wallets user_id
CREATE INDEX idx_wallets_user_id ON wallets(user_id);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    address_to TEXT NOT NULL,
    amount NUMERIC NOT NULL,
    transaction_id TEXT NOT NULL,
    wallet_id INTEGER NOT NULL,
    datetime TEXT NOT NULL,
    FOREIGN KEY(wallet_id) REFERENCES wallets(id) ON DELETE CASCADE ON UPDATE NO ACTION
);

-- Index for transactions user_id
CREATE INDEX idx_trasanctions_wallet_id ON transactions(wallet_id);

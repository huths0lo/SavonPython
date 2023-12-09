# Database Schema.  Used if a new database is created.

DB_SCHEMA = [
    """ CREATE TABLE IF NOT EXISTS user_accounts (
        id integer PRIMARY KEY,
        name varchar NOT NULL,
        created_data text,
        end_date text
        ); """,
    """ CREATE TABLE IF NOT EXISTS control (
        id integer PRIMARY KEY,
        name varchar NOT NULL,
        created_data text,
        end_date text
        ); """,
]

DB_TEST_COMMANDS = [
    'SELECT * FROM user_accounts;',
    'SELECT * FROM control;'
]
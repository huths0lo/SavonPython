# Database Schema.  Used if a new database is created.

DB_SCHEMA = [
    "CREATE DATABASE savon_python;",
    """ CREATE TABLE IF NOT EXISTS savon_python.user_accounts (
        id integer PRIMARY KEY,
        name varchar NOT NULL,
        created_data text,
        end_date text
        ); """,
    """ CREATE TABLE IF NOT EXISTS savon_python.control (
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
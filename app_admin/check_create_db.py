import sqlite3
from sqlite3 import Error
import os
import sys
import fnmatch


from app_admin.sql_commands import DB_SCHEMA, DB_TEST_COMMANDS

db_path = os.getcwd() + '/app_db/'
db_file_extension = '.sqlite'


def find(extension, path):
    pattern = '*' + extension
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def find_db_else_create_new():
    db_file = find(db_file_extension, db_path)
    if len(db_file) == 0:
        print('\nNo database file found!  DB Setup will now run.')
        db_file = [create_new_db()]
    if len(db_file) == 0:
        print('\nFailed to connect to db.  Aborting.\n')
        sys.exit()
    return db_file[0]


def create_new_db():
    if len(find(db_file_extension, db_path)) != 0:
        should_delete = input('WARNING!!! - Database file found in working directory.  If you proceed, it will be overwritten.\n\nTo prodeed type "DELETE": ')
        if should_delete.lower() != 'delete':
            print('\nAborting.\n')
            sys.exit()
    db_file = input('What would you like to name the database file? (default: savonpy_db) - Press enter for default: ')
    if db_file == '':
        db_file = db_path + 'savonpy_db' + db_file_extension
    else:
        db_file = db_path + db_file + db_file_extension
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
        print('\nFailed to create db file.  Aborting.\n')
        sys.exit()
    finally:
        if conn:
            conn.close()
    if not create_db_schema(db_file):
        print('\nFailed to create db file.  Aborting.\n')
        sys.exit()
    print(f'New database file created: {db_file}')
    confirm_db_schema(db_file)
    return db_file

def confirm_db_schema(db_file):
    conn = sqlite3.connect(db_file)
    for sql_command in DB_TEST_COMMANDS:
        try:
            c = conn.cursor()
            test = c.fetchone(sql_command)
        except Error as e:
            print(e)
            print('\nDatabase integrity check failed!\n')
            sys.exit()
    print('Database integrity confirmed!')
    return



def create_db_schema(db_file):
    conn = sqlite3.connect(db_file)
    for sql_command in DB_SCHEMA:
        try:
            c = conn.cursor()
            c.execute(sql_command)
        except Error as e:
            print(e)
            print('\nFailed to create db file.  Aborting.\n')
            sys.exit()
    return True



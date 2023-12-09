import sqlite3
from sqlite3 import Error as SQLError
import os
import sys

from db_schema import DB_SCHEMA

db_path = os.getcwd()
db_file_extension = '.sqlite'

import os, fnmatch
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def find_db_else_create_new():
    db_files = find(db_file_extension, db_path)
    if len(db_files) == 0:
        print('\nNo database file found!  DB Setup will now run.')
        db_file = [create_new_db()]
    if len(db_files) == 0:
        print('\nFailed to connect to db.  Aborting.\n')
        sys.exit()



def create_new_db():
    if len(find(db_file_extension, db_path)) != 0:
        should_delete = input('WARNING!!! - Database file found in working directory.  If you proceed, it will be overwritten.\n\nTo prodeed type "DELETE": ')
        if should_delete.lower() != 'delete':
            print('\nAborting.\n')
            sys.exit()
    db_file = input('What would you like to name the database file? (default: savonpy_db) - Press enter for default: ')
    if db_file == '':
        db_file = 'savonpy_db' + db_file_extension
    else:
        db_file = db_file + db_file_extension
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except SQLError as e:
        print(e)
        print('\nFailed to create db file.  Aborting.\n')
        sys.exit()
    finally:
        if conn:
            conn.close()
    if not create_db_schema(db_file):
        print('\nFailed to create db file.  Aborting.\n')
        sys.exit()
    print(f'New database file created: {db_path}/{db_file}')
    return db_file



def create_db_schema(db_file):
    conn = sqlite3.connect(db_file)
    for sql_command in DB_SCHEMA:
        try:
            c = conn.cursor()
            c.execute(sql_command)
        except SQLError as e:
            print(e)
            print('\nFailed to create db file.  Aborting.\n')
            sys.exit()
    return True



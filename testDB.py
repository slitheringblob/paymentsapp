import sqlite3
from sqlite3 import Error

def create_Connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)

    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


if __name__=='__main__':
    create_Connection(r"C:\Users\jayde\Documents\sqlite3\db\paymentsappDB.db")
    

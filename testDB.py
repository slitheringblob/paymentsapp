import sqlite3
from sqlite3 import Error

def create_Connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection Established")
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)


if __name__=='__main__':
    create_Connection(r"C:\Users\jayde\Documents\sqlite3\db\vpt.db")
    

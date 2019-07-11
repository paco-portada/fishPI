import fishPI
import sqlite3
import os

from sqlite3 import Error
from fishPI import logging
from fishPI import services
from fishPI import config

conn = None

def close_conn(conn):
    try:
        conn.close()
    except Error as e:
        print(e)
            
def create_conn():
    conn = sqlite3.connect(fishPI.config.database)
    return conn

def database_exists():
    return os.path.exists(fishPI.config.database)

def create_table(create_table_sql):
    conn = create_conn()
    c = conn.cursor()
    c.execute(create_table_sql)
    print("executed")
    close_conn(conn)

def create_schema():
    if(database_exists()):
        return True

    sql_create_meta_table = """ CREATE TABLE IF NOT EXISTS meta (
                                    id INTEGER PRIMARY KEY,
                                    key TEXT NOT NULL,
                                    value TEXT,
                                    added DATETIME DEFAULT CURRENT_TIMESTAMP
                                ); """
    conn = create_conn()
    create_table(sql_create_meta_table)
    close_conn(conn)

def key_count(key):
        conn = create_conn()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM meta WHERE key=?", (key,))
        result=cursor.fetchone()
        close_conn(conn)
        return result[0]

def save_meta(key, value, unique = True):

    meta = (key, value)

    if(unique and key_count(key) > 0):

        sql = ''' UPDATE meta set value = ? where key = ? '''
        conn = create_conn()
        cur = conn.cursor()
        cur.execute(sql, meta)
        close_conn(conn)
        return True

    else:

        sql = ''' INSERT INTO meta(key,value)
                VALUES(?,?) '''
        conn = create_conn()
        cur = conn.cursor()
        cur.execute(sql, meta)
        close_conn(conn)
        return cur.lastrowid

def get_meta(key, unique = True):
        conn = create_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, key, value, added FROM meta WHERE key=?", (key,))

        if(unique):
            result=cursor.fetchone()
            close_conn(conn)
            return result[0]
        else:
            result=cursor.fetchall()
            close_conn(conn)
            return result
         
         
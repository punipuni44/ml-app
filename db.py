import sqlite3

# DB接続
def get_connection():
    return sqlite3.connect("data.db")

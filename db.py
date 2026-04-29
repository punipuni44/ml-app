import sqlite3

def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# DB接続
def get_connection():
    return sqlite3.connect("data.db")

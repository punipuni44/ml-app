
# レコード全取得
def insert_log(cursor, day, prediction):
    cursor.execute(
        "INSERT INTO logs (day, prediction) VALUES (?, ?)",
        (day, prediction)
    )

# レコード全取得
def fetch_logs(cursor):
    cursor.execute("SELECT id, day, prediction, created_at FROM logs")
    return cursor.fetchall()

# レコードを辞書形式に変換
def rows_to_logs(rows):
    return [
        {
            "id": row[0],
            "day": row[1],
            "prediction": row[2],
            "created_at": row[3]
        }
        for row in rows
    ]
from fastapi import FastAPI
import pandas as pd

from db import get_connection
from crud import insert_log, fetch_logs, rows_to_logs
from ml import create_model

app = FastAPI()

model = create_model()

# ルート
@app.get("/")
def root():
    return {"message": "API is running"}

# 予測API
@app.get("/predict")
def predict(day: int):
    input_data = pd.DataFrame([[day]], columns=["day"])
    result = model.predict(input_data)
    prediction = float(result[0])

    # DB保存
    conn = get_connection()
    try:
        cursor = conn.cursor()
        insert_log(cursor, day, prediction)
        conn.commit()
    finally:
        conn.close()

    return {"prediction": prediction}

# レコード取得API
@app.get("/logs")
def get_logs() -> dict:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # DBからログ一覧を取得
        rows = fetch_logs(cursor)
        # API用形式に変換
        logs = rows_to_logs(rows)
    finally:
        conn.close()

    return {"logs": logs}

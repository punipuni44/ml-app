from fastapi import FastAPI, Depends, Query
import pandas as pd
from sqlite3 import Connection

from db import get_db
from crud import insert_log, fetch_logs, rows_to_logs
from ml import create_model
from schemas import PredictionResponse, LogsResponse

app = FastAPI()

model = create_model()

# ルート
@app.get("/")
def root() -> dict:
    return {"message": "API is running"}

# 予測API
@app.get("/predict", response_model=PredictionResponse)
def predict(
    day: int = Query(ge=1, le=365), 
    db: Connection = Depends(get_db)
) -> PredictionResponse:

    # モデル学習・予測
    input_data = pd.DataFrame([[day]], columns=["day"])
    result = model.predict(input_data)
    prediction = float(result[0])

    # DB保存
    cursor = db.cursor()
    insert_log(cursor, day, prediction)

    return {"prediction": prediction}

# レコード取得API
@app.get("/logs", response_model=LogsResponse)
def get_logs(db: Connection = Depends(get_db)) -> LogsResponse:

    cursor = db.cursor()

    # DBからログ一覧を取得
    rows = fetch_logs(cursor)

    # API用形式に変換
    logs = rows_to_logs(rows)

    return {"logs": logs}

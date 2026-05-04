from sqlite3 import Connection

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.exceptions import RequestValidationError

from crud import fetch_logs, insert_log, rows_to_logs
from db import get_db
from handlers import validation_exception_handler
from ml import create_model
from schemas import ErrorResponse, LogsResponse, PredictionResponse

app = FastAPI()

app.add_exception_handler(RequestValidationError, validation_exception_handler)

model = create_model()

# ルート
@app.get("/")
def root() -> dict:
    return {"message": "API is running"}

# 予測API
@app.get(
    "/predict", 
    # 正常系レスポンスのスキーマ
    response_model=PredictionResponse,
    # エラー系レスポンスのスキーマ
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse}
    }
)
def predict(
    day: int = Query(ge=1, le=365), 
    db: Connection = Depends(get_db)
) -> PredictionResponse:

    # モデル学習・予測
    input_data = pd.DataFrame([[day]], columns=["day"])
    result = model.predict(input_data)
    prediction = float(result[0])

    # エラーハンドリング
    if prediction < 0:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "INVALID_PREDICTION",
                    "message": "Prediction result must be non-negative"
                }
            }
        )

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

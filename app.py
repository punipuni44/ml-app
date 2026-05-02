from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import pandas as pd
from sqlite3 import Connection

from db import get_db
from crud import insert_log, fetch_logs, rows_to_logs
from ml import create_model
from schemas import PredictionResponse, LogsResponse, ErrorResponse

app = FastAPI()

model = create_model()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request parameter"
            }
        },
    )

# ルート
@app.get("/")
def root() -> dict:
    return {"message": "API is running"}

# 予測API
@app.get(
    "/predict", 
    response_model=PredictionResponse,
    responses={
        400: {"model": ErrorResponse}
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

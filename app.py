from fastapi import FastAPI
from sklearn.linear_model import LinearRegression
import pandas as pd
import sqlite3

app = FastAPI()

# データ
data = {
    "day": [1,2,3,4,5],
    "sales": [100,150,200,250,300]
}

df = pd.DataFrame(data)
X = df[["day"]]
y = df["sales"]

# モデル作成＆学習
model = LinearRegression()
model.fit(X, y)

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
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO logs (day, prediction) VALUES (?, ?)",
        (day, prediction)
    )

    conn.commit()
    conn.close()

    return {"prediction" : prediction}
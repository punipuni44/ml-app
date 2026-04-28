from sklearn.linear_model import LinearRegression
import pandas as pd

def create_model():
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

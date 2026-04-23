import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# ダミーデータ
data = {
    "day": [1,2,3,4,5],
    "sales": [100,150,200,250,300]
}

df = pd.DataFrame(data)

# 学習
X = df[["day"]]
y = df["sales"]

model = LinearRegression()
model.fit(X, y)

# 予測
pred = model.predict(pd.DataFrame([[6]], columns=["day"]))
print("Day6 prediction:", pred)

# グラフ
plt.scatter(df["day"], df["sales"])
plt.plot(df["day"], model.predict(X))
plt.savefig("result.png")
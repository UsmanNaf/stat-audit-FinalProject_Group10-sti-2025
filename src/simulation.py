import pandas as pd
import random
import matplotlib.pyplot as plt

df = pd.read_csv("../data/clean/issues_clean.csv")
df = df.dropna(subset=["closed_at"])

df["created_at"] = pd.to_datetime(df["created_at"])
df["closed_at"] = pd.to_datetime(df["closed_at"])

df["close_days"] = (df["closed_at"] - df["created_at"]).dt.days
df = df[df["close_days"] >= 0]
close_days = df["close_days"].tolist()

num_simulations = 10000

count_over_30 = 0

for _ in range(num_simulations):

    sampled_day = random.choice(close_days)

    if sampled_day > 30:
        count_over_30 += 1

probability = count_over_30 / num_simulations

print("Estimated Probability:", probability)

plt.hist(df["close_days"], bins=30)

plt.title("Issue Closure Duration")
plt.xlabel("Days")
plt.ylabel("Frequency")

plt.show()
import pandas as pd

df = pd.read_csv("chat_log.csv", names=["timestamp","question","article","success"])
print("Top asked articles:\n", df["article"].value_counts())
print("Success rates:\n", df.groupby("article")["success"].value_counts(normalize=True))

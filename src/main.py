import numpy as np
import pandas as pd
import sqlite3

np.random.seed(42)

users = np.arange(1, 51)
apps = ["Instagram", "LinkedIn", "YouTube", "WhatsApp", "Slack"]

categories = {
    "Instagram": "Social",
    "LinkedIn": "Work",
    "YouTube": "Entertainment",
    "WhatsApp": "Social",
    "Slack": "Work"
}

data = []

for _ in range(500):
    app = np.random.choice(apps)
    data.append([
        np.random.choice(users),
        pd.Timestamp("2024-01-01") + pd.Timedelta(days=np.random.randint(0, 30)),
        app,
        np.random.randint(10, 300),
        categories[app],
        round(np.random.uniform(4, 9), 1)
    ])

df = pd.DataFrame(data, columns=[
    "UserID", "Date", "App", "UsageMinutes", "Category", "SleepHours"
])

df["IsAddictive"] = df["UsageMinutes"] > 180
df["ProductivityScore"] = df["SleepHours"] * 10 - df["UsageMinutes"] * 0.1

df.to_csv("data/usage.csv", index=False)

conn = sqlite3.connect("behavior.db")
df.to_sql("usage", conn, if_exists="replace", index=False)

query = """
SELECT UserID, SUM(UsageMinutes) as TotalUsage
FROM usage
GROUP BY UserID
ORDER BY TotalUsage DESC
LIMIT 5
"""

print(pd.read_sql(query, conn))



import pandas as pd

# Load the jackpot results CSV
df = pd.read_csv("jackpot_results.csv")

# Decode the outcome
df["outcome_decode"] = df["outcome"].map({
    "Draw": 0,
    "Home": 1,
    "Away": 2
})

# Display the data
print(df.head())
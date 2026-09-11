import pandas as pd

# Load the jackpot results CSV
df = pd.read_csv("jackpot_results.csv")

# Decode the outcome
df["outcome_decode"] = df["outcome"].map({
    "Draw": 0,
    "Home": 1,
    "Away": 2
})

# Keep only complete groups of 17
number_of_groups = len(df) // 17

# Create the grouped dataset
grouped_data = []

for i in range(number_of_groups):
    start = i * 17
    end = start + 17

    # Get 17 consecutive decoded outcomes
    group = df["outcome_decode"].iloc[start:end]

    # Combine the 17 values into one string
    sequence = "".join(group.astype(str))

    grouped_data.append(sequence)

# Create a new DataFrame
grouped_df = pd.DataFrame({
    "outcome_sequence": grouped_data
})

# Display the new dataset
print(grouped_df.to_string(index=False))

# Save it as a new CSV
grouped_df.to_csv("jackpot_groups.csv", index=False)
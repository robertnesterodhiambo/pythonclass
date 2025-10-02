import os
import random
from datetime import datetime, timedelta

# Start and end dates

start_date = datetime(2025, 9, 28)
end_date = datetime(2025, 10, 1)


# Path to the text file
date_file_path = "commit_dates.txt"

# Generate the dates with multiple commits for each day
with open(date_file_path, "w") as file:
    current_date = start_date
    while current_date <= end_date:
        commits_per_day = random.randint(1, 8)
        for _ in range(commits_per_day):
            file.write(current_date.strftime("%Y-%m-%dT%H:%M:%S") + "\n")
        current_date += timedelta(days=1)

# Function to run a shell command
def run_command(command):
    os.system(command)

# Read the dates from the file and create commits
with open(date_file_path, "r") as file:
    for date in file:
        date = date.strip()
        commit_message = f"Commit for {date.split('T')[0]}"
        
        run_command(f'GIT_COMMITTER_DATE="{date}" git commit --allow-empty --date "{date}" -m "{commit_message}"')
        run_command("git push")

# Clean up the text file after use
os.remove(date_file_path)

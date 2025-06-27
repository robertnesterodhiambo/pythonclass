import os
import pandas as pd

# Get the current directory where the script is located
current_folder = os.path.dirname(os.path.abspath(__file__))

# Find the first .xlsx file in the folder
xlsx_files = [f for f in os.listdir(current_folder) if f.endswith('.xlsx')]

if not xlsx_files:
    print("No .xlsx file found in the folder.")
else:
    xlsx_path = os.path.join(current_folder, xlsx_files[0])
    print(f"Importing file: {xlsx_files[0]}")

    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(xlsx_path)

    # Show the first few rows
    print(df.head())

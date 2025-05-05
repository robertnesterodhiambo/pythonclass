import pandas as pd

# Load the CSV file
file_path = '/home/dragon/DATA/stock_details_5_years.csv'
df = pd.read_csv(file_path)

# Extract the 'Company' column (ensure it's named exactly 'Company')
if 'Company' in df.columns:
    companies = df['Company'].dropna().unique()
    
    # Save to text file
    with open('company_list.txt', 'w') as f:
        for name in companies:
            f.write(f"{name}\n")
    
    print("Company names saved to company_list.txt")
else:
    print("'Company' column not found in the CSV.")

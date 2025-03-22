from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import pandas as pd
import os

# Load the Excel file
excel_path = os.path.join(os.getcwd(), "TEX (1).xlsx")
df = pd.read_excel(excel_path)  # Read the first sheet

# Combine all columns into one column (ignoring NaN values)
df_combined = df.melt(value_name="Combined_Column")["Combined_Column"].dropna()

# Save to CSV file
csv_path = os.path.join(os.getcwd(), "combined_data.csv")
df_combined.to_csv(csv_path, index=False)

# Re-import the CSV file
df_reimported = pd.read_csv(csv_path)

# Print first few rows to verify
print(df_reimported.head())

# Set up Firefox options
options = Options()
options.add_argument("--start-maximized")  # Open browser in maximized mode (optional)

# Set up geckodriver path (assuming it's in the same folder as the script)
gecko_path = os.path.join(os.getcwd(), "geckodriver")
service = Service(gecko_path)

# Initialize the WebDriver
driver = webdriver.Firefox(service=service, options=options)
driver.set_page_load_timeout(300)  # Set timeout to 5 minutes

# Open the given website
driver.get("https://tex.textainer.com/Equipment/StatusAndSpecificationsInquiry.aspx")

# Keep the browser open (optional)
input("Press Enter to close the browser...")

driver.quit()

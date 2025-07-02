import os
import re
import shutil
from datetime import datetime

# Define the folder where the PDF is located
source_folder = '.'  # change if it's in a specific folder

# Define the target folder
target_folder = 'PDF'
os.makedirs(target_folder, exist_ok=True)

# Pattern to match PDF files named like "Boletim_da_PI_-_2025-07-02.pdf"
pattern = re.compile(r'Boletim_da_PI_-_(\d{4}-\d{2}-\d{2})\.pdf')

latest_file = None
latest_date = None

# Scan all files in the source folder
for filename in os.listdir(source_folder):
    match = pattern.match(filename)
    if match:
        file_date = datetime.strptime(match.group(1), '%Y-%m-%d')
        if latest_date is None or file_date > latest_date:
            latest_date = file_date
            latest_file = filename

# If we found any matching file, copy it
if latest_file:
    current_date_str = datetime.today().strftime('%Y-%m-%d')
    target_path = os.path.join(target_folder, f"{current_date_str}.pdf")
    shutil.copy2(os.path.join(source_folder, latest_file), target_path)
    print(f"Copied '{latest_file}' to '{target_path}'")
else:
    print("No matching PDF found.")

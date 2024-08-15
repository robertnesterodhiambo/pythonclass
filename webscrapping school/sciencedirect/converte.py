import re
import csv

# Step 1: Read the text file
with open('link.txt', 'r') as file:
    content = file.read()

# Step 2: Extract the links using regular expressions
links = re.findall(r'https?://[^\s,\'"]+', content)

# Step 3: Write the links into a CSV file
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['links'])  # Write the column header

    # Write each link as a new row in the CSV file
    for link in links:
        writer.writerow([link])

print("Links have been successfully extracted and saved to output.csv")

import csv
import re

def extract_full_names(file_path, output_csv):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Split sections based on 3 or more newlines
        sections = re.split(r"\n{3,}", content.strip())

        # Extract the first line from each section as the full name
        full_names = [section.strip().split("\n")[0] for section in sections if section.strip()]

        # Write names to CSV
        with open(output_csv, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Full Name"])  # Header
            for name in full_names:
                writer.writerow([name])

        print(f"Full names successfully saved to {output_csv}")

    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"Error: {e}")

# File paths
input_file = "formatted_text.txt"
output_csv = "full_names.csv"

# Run the function
extract_full_names(input_file, output_csv)

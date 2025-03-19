import csv
import re

def extract_names_and_divisions(file_path, output_csv):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Split text into chunks based on multiple blank lines (4 or more spaces/newlines)
        sections = re.split(r"(?:\n\s*){4,}", content.strip())

        # Extract full names (first line) and divisions (second line)
        extracted_data = []
        for section in sections:
            lines = section.strip().split("\n")
            if len(lines) >= 2:
                full_name = lines[0].strip()
                division = lines[1].strip()
                extracted_data.append([full_name, division])

        # Save to CSV
        with open(output_csv, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Full Name", "Division"])  # CSV headers
            writer.writerows(extracted_data)

        print(f"Full names and divisions successfully saved to {output_csv}")

    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"Error: {e}")

# File paths
input_file = "formatted_text.txt"
output_csv = "full_names_divisions.csv"

# Run the function
extract_names_and_divisions(input_file, output_csv)

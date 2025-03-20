import csv
import re

def extract_data(file_path, output_csv):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Split text into chunks based on multiple blank lines (4 or more spaces/newlines)
        sections = re.split(r"(?:\n\s*){4,}", content.strip())

        extracted_data = []
        phone_pattern = r"\(\d{3}\) \d{3}-\d{4}"  # Matches (XXX) XXX-XXXX format

        for section in sections:
            lines = section.strip().split("\n")
            if len(lines) < 2:
                continue  # Skip if there's not enough data

            full_name = lines[0].strip()
            division = lines[1].strip()
            insurance_network = ""
            phone_numbers = []
            final_line = ""

            # Combine all text from the 3rd line onwards
            if len(lines) > 2:
                text_section = "\n".join(lines[2:])

                # Find the first phone number
                match = re.search(phone_pattern, text_section)
                if match:
                    insurance_network = text_section[:match.start()].strip()  # Extract text before phone number
                    
                    # Extract all phone numbers
                    phone_numbers = re.findall(phone_pattern, text_section)
                    
                    # Extract the full line containing the first phone number
                    for line in lines[2:]:
                        if match.group(0) in line:
                            final_line = line.strip()
                            break

            # Convert list of phone numbers into a single comma-separated string
            phone_numbers_str = ", ".join(phone_numbers)

            extracted_data.append([full_name, division, insurance_network, phone_numbers_str, final_line])

        # Save to CSV
        with open(output_csv, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Full Name", "Division", "Insurance Network", "Phone Numbers", "Final"])  # CSV headers
            writer.writerows(extracted_data)

        print(f"Data successfully saved to {output_csv}")

    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"Error: {e}")

# File paths
input_file = "formatted_text.txt"
output_csv = "extracted_data.csv"

# Run the function
extract_data(input_file, output_csv)

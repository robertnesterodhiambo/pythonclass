# Install required libraries
#!pip install requests beautifulsoup4
########  !pip install selenium
#!apt update
#!apt install chromium-chromedriver
#!pip install selenium
#!apt-get update
#!apt-get install -y firefox
#!apt-get install -y wget
#!wget -O geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz"
#!tar -xvzf geckodriver.tar.gz
#!chmod +x geckodriver
#!mv geckodriver /usr/local/bin/


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import csv

# Setup Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize the driver
dr = webdriver.Chrome(options=options)

# Open the website
dr.get("https://www.agedcarequickstart.com.au/")

def perform_search(address):
    # Locate the input field by its ID and enter the address
    input_field = dr.find_element(By.ID, "location")
    input_field.clear()  # Clear the field before entering the new address
    input_field.send_keys(address)

    # Submit the search (by pressing Enter)
    input_field.send_keys(Keys.RETURN)

    # Wait for the results and the radius select element to load
    time.sleep(10)  # Adjust time as needed

    # Locate the <select> element by its ID
    select_element = dr.find_element(By.ID, "radius")

    # Create a Select object and choose the option by visible text
    select = Select(select_element)
    select.select_by_visible_text("50 km")

    # Optionally, wait for the page to update after selecting the radius
    time.sleep(10)  # Adjust time as needed

    # Scroll to the bottom of the page to load all information
    dr.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for the new content to load
    time.sleep(10)  # Adjust time as needed

def collect_links():
    links = []
    # Locate all divs with the class 'col mb-4'
    divs = dr.find_elements(By.CSS_SELECTOR, "div.col.mb-4")

    for div in divs:
        # Find all anchor tags within each div with the class 'fo-black text-decoration-none'
        anchors = div.find_elements(By.CSS_SELECTOR, "a.fo-black.text-decoration-none")
        for anchor in anchors:
            links.append(anchor.get_attribute("href"))

    return links

def save_links_to_csv(links, filename):
    # Save the collected links to a CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Link"])  # Write header
        for link in links:
            writer.writerow([link])

def extract_home_info(link):
    # Open the link in the browser
    dr.get(link)

    # Wait for the page to load
    time.sleep(5)  # Adjust time as needed

    # Extract the text from the <h1> tag with the specified class (home name)
    h1_element = dr.find_element(By.CSS_SELECTOR, "h1.fw-bold.fs-1.fo-blue-800.text-center.mt-4.mb-2")
    home_name = h1_element.text

    # Extract the text from the <div> with class 'mb-4 text-center' (location)
    location_element = dr.find_element(By.CSS_SELECTOR, "div.mb-4.text-center")
    location = location_element.text

    # Extract the text from the <div> with id 'details' (for about_home, phone_number, and email)
    details_div = dr.find_element(By.ID, "details")
    row_divs = details_div.find_elements(By.CSS_SELECTOR, "div.row")

    # Extract phone number from the 8th row (index 7)
    phone_number_div = row_divs[7].find_element(By.CSS_SELECTOR, "div.col-12.col-md-11.ps-md-0.mb-3") if len(row_divs) > 7 else None
    phone_number = phone_number_div.text if phone_number_div else ""

    # Extract email from the last row
    last_row_div = row_divs[-1] if row_divs else None
    email_div = last_row_div.find_element(By.CSS_SELECTOR, "div.col-12.col-md-11.ps-md-0.mb-3") if last_row_div else None
    email = email_div.text if email_div else ""

    # Extract the about_home information from the second div of the details section
    about_home_div = details_div.find_element(By.CSS_SELECTOR, "div.col-12.col-xl-9")
    about_home_rows = about_home_div.find_elements(By.CSS_SELECTOR, "div.row")

    # The second div in this section contains the about_home information
    about_home = about_home_rows[1].text if len(about_home_rows) > 1 else ""

    # Extract rating from the #ratings section
    ratings_div = dr.find_element(By.ID, "ratings")
    rating_container = ratings_div.find_element(By.CSS_SELECTOR, "div.col-12.col-md-7.col-xl-9.mb-3")
    stars = rating_container.find_elements(By.CSS_SELECTOR, "p svg use[href='#star_blue']")
    rating = len(stars)  # Count the number of filled stars

    return home_name, location, about_home, phone_number, email, rating, link

# List of addresses to search
addresses = [str(i) for i in range(3100, 3300)]

all_links = []

# Loop through each address and perform search to collect all links
for address in addresses:
    perform_search(address)
    links = collect_links()
    all_links.extend(links)
    print(f"Links from search {address}:", links)

# Save all collected links to a CSV file
csv_filename = "collected_links.csv"
save_links_to_csv(all_links, csv_filename)
print(f"All links saved to {csv_filename}")

# If you want to proceed with extracting information after saving, uncomment the following lines:
# home_infos = []

# # Open each collected link and extract home information
# for link in all_links:
#     home_name, location, about_home, phone_number, email, rating, link = extract_home_info(link)
#     home_infos.append({
#         'home_name': home_name,
#         'location': location,
#         'about_home': about_home,
#         'phone_number': phone_number,
#         'email': email,
#         'rating': rating,
#         'link': link
#     })

# # Output the collected home information
# print("Home information collected:", home_infos)

# Quit the browser
dr.quit()

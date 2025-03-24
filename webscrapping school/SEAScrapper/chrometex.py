import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load the CSV file
file_path = "combined_data.csv"
df = pd.read_csv(file_path)

# Get the first 10 entries from the 'Combined_Column'
entries = df["Combined_Column"].astype(str).tolist()[:10]

# Set up Chrome WebDriver (Chromedriver in the same folder)
chrome_path = "./chromedriver"  # Ensure chromedriver is in the same folder
service = Service(chrome_path)
options = Options()
# options.add_argument("--headless")  # Uncomment to run in headless mode

driver = webdriver.Chrome(service=service, options=options)

# Open the target website
url = "https://tex.textainer.com/Equipment/StatusAndSpecificationsInquiry.aspx"
driver.get(url)

# Set timeout duration
timeout = 15  # Adjust based on network speed

# Iframe IDs to check
iframe_ids = [
    "ReportFramectl00_bodyContent_rptViewer",
    "PrintFramectl00_bodyContent_rptViewer",
    "ctl00_bodyContent_rptViewerTouchSession0"
]

# Dictionary to store results
results = {}

# Loop through the first 10 entries
for index, entry in enumerate(entries):
    try:
        print(f"\n🔍 Searching for: {entry}")

        # Locate the input field and enter the entry
        text_area = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "ctl00_bodyContent_ucEqpIds_txtEqpId"))
        )
        text_area.clear()
        text_area.send_keys(entry)

        # Click the submit button
        submit_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "ctl00_bodyContent_btnSubmit"))
        )
        submit_button.click()

        # **Wait for an iframe to appear**
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )

        # **Try extracting data from the available iframes**
        current_status = "No Report Found"
        for iframe_id in iframe_ids:
            try:
                driver.switch_to.default_content()  # Ensure we are on the main page
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, iframe_id))
                )
                driver.switch_to.frame(iframe_id)

                # **Wait for text inside the iframe to load**
                WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                # **Extract text from the iframe**
                current_status = driver.execute_script("return document.body.innerText;").strip()

                if current_status:
                    break  # If we find text, stop checking other iframes

            except Exception:
                continue  # If the iframe is not found or empty, check the next one

        print(f"✅ Status for {entry}: {current_status[:200]}...")  # Show first 200 chars
        results[entry] = current_status

        # **Switch back to the main page**
        driver.switch_to.default_content()

    except Exception as e:
        print(f"❌ Error processing {entry}: {e}")
        results[entry] = "Error"

    # **Go back to search for the next entry**
    driver.back()

    # **Ensure the page reloads before the next search**
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, "ctl00_bodyContent_ucEqpIds_txtEqpId"))
    )

    # **Ensure the submit button is available before continuing**
    WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.ID, "ctl00_bodyContent_btnSubmit"))
    )

# Close the browser
driver.quit()

# Save results
results_df = pd.DataFrame(list(results.items()), columns=["Entry", "Current Status"])
results_df.to_csv("extracted_statuses.csv", index=False)

print("\n✅ Completed! Data saved to 'extracted_statuses.csv'.")

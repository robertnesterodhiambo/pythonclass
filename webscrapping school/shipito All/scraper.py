from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Set up the Chrome WebDriver with headless options
chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

# Read the CSV file containing country details
df = pd.read_csv("100 Country list 20180621.csv")

# Open the Shipito shipping calculator page
driver.get("https://www.shipito.com/en/shipping-calculator")

# Weight values to loop through
all_lbs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250]

# Final output and fail lists to store results
final_output = []
fail = []

# Loop through the rows in the DataFrame (each row represents a country)
for index, row in df.iterrows():
    try:
        print(f"Processing: {index} - {row['countryname']}")

        # Scroll down to make sure elements are visible
        driver.execute_script("window.scrollTo(0, 400)")

        # Click on the warehouse dropdown and select the warehouse
        driver.find_element(By.XPATH, "//button[@class='btn dropdown-toggle']").click()
        driver.find_element(By.XPATH, "//a[@data-value='7']").click()  # Select Torrance warehouse
        time.sleep(5)

        # Scroll further to make the country dropdown visible
        driver.execute_script("window.scrollTo(0, 950)")
        driver.find_element(By.XPATH, "//li[@class='dropdown st-selected-country']").click()

        # Type the country name into the filter input
        country_filter_input = driver.find_elements(By.XPATH, "//input[@class='form-control st-country-filter']")[1]
        country_filter_input.send_keys(str(row["countryname"]).strip())

        # Input city and zip code
        driver.find_element(By.XPATH, "//input[@name='shippingcalculator.city']").clear()
        driver.find_element(By.XPATH, "//input[@name='shippingcalculator.city']").send_keys(str(row["city"]).strip())
        driver.find_element(By.XPATH, "//input[@name='shippingcalculator.postalcode']").clear()
        driver.find_element(By.XPATH, "//input[@name='shippingcalculator.postalcode']").send_keys(str(row["zipcode"]).strip())

        # Print the selected country name
        print(driver.find_elements(By.XPATH, "//span[@class='st-selected-country-name']")[0].text)

        # Iterate over the weight list
        for el in all_lbs:
            # Clear and input weight value
            weight_input = driver.find_element(By.XPATH, "//input[@name='shippingcalculator.scaleweight_val']")
            weight_input.clear()
            weight_input.send_keys(str(el))

            # Click the calculate button
            driver.find_element(By.XPATH, "//button[@class='btn btn-secondary btn-calculator']").click()

            # Wait for the results table to appear
            wait1 = WebDriverWait(driver, 10)
            tb1 = wait1.until(EC.presence_of_element_located((By.XPATH, "//table[@class='table quotes-table']")))

            # If the table is empty, log it
            if len(tb1.text) == 0:
                final_output.append(["California USA", row["countryname"], row["city"], row["zipcode"], el])
                print("** No results:", ["California USA", row["countryname"], row["city"], row["zipcode"], el])
            else:
                # Extract the table rows and append the data to the final output
                for eachbody in tb1.find_elements(By.XPATH, "tbody"):
                    for eachtr in eachbody.find_elements(By.XPATH, "tr"):
                        if len(eachtr.text) != 0:
                            etbl = []
                            for td in eachtr.find_elements(By.XPATH, "td"):
                                etbl.append(str(td.text).strip())

                            final_output.append(
                                ["California USA", row["countryname"], row["city"], row["zipcode"], el, etbl[0],
                                 etbl[1].split(" ")[0], etbl[1].split(" ")[1]] + etbl[2:])
                            print(["California USA", row["countryname"], row["city"], row["zipcode"], el, etbl[0],
                                   etbl[1].split(" ")[0], etbl[1].split(" ")[1]] + etbl[2:])

        # Save the final output to Excel file
        final_df = pd.DataFrame(final_output,
                                columns=["Sending Warehouse", "Receiving Country", "Receiving City", "Receiving Zipcode",
                                         "Weight in (LBS)", "Shipping Method", "Postage", "Postage Currency", "Estimated Delivery Time",
                                         "Insurance", "Tracking", "Weight", "Limits"])
        final_df.to_excel("shipto.xlsx", index=False)

    except Exception as e:
        # Log failed attempts
        print(f"Failed for {index}: {e}")
        fail.append(index)
        continue

# Final cleanup: Export fail data to Excel
fail_df = pd.DataFrame(fail, columns=["Failed Indexes"])
fail_df.to_excel("fail.xlsx", index=False)

driver.quit()

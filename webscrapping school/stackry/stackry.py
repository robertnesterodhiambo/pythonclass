from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # Add this import
from selenium.webdriver.support import expected_conditions as EC  # Add this import
import time
import pandas as pd

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

df = pd.read_csv("100 Country list 20180621.csv")

driver.get("https://www.stackry.com/en/shipping-calculator")

final_output = []
wait = WebDriverWait(driver, 15)  # This should work now after the correct import

for i, row in df.iterrows():
    print(i)
    driver.get("https://www.stackry.com/en/shipping-calculator")
    driver.execute_script("window.scrollTo(0, 400)")

    try:
        # Wait for country dropdown
        wait.until(EC.presence_of_element_located((By.ID, "country")))
        alcc = driver.find_element(By.XPATH, '//select[@id="country"]')
        alcc.find_element(By.XPATH, 'option[@value="' + str(row["countryiso"]) + '"]').click()
    except:
        continue

    # Fill in address details
    driver.find_element(By.XPATH, "//input[@id='city_calculator']").clear()
    driver.find_element(By.XPATH, "//input[@id='city_calculator']").send_keys(str(row["city"]))
    driver.find_element(By.XPATH, "//input[@name='length']").clear()
    driver.find_element(By.XPATH, "//input[@name='length']").send_keys("1")
    driver.find_element(By.XPATH, "//input[@name='width']").clear()
    driver.find_element(By.XPATH, "//input[@name='width']").send_keys("1")
    driver.find_element(By.XPATH, "//input[@name='height']").clear()
    driver.find_element(By.XPATH, "//input[@name='height']").send_keys("1")

    if driver.find_element(By.XPATH, "//div[@id='postal_section']").get_attribute("style") != 'display: none;':
        driver.find_element(By.XPATH, "//input[@id='postal_code']").clear()
        driver.find_element(By.XPATH, "//input[@id='postal_code']").send_keys(str(row["zipcode"]))

    # Loop through weights and save immediately after processing each one
    for el in [1, 2]: #, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250]:
        print("\n")
        driver.find_element(By.XPATH, "//input[@name='weight']").clear()
        driver.find_element(By.XPATH, "//input[@name='weight']").send_keys(str(el))
        driver.execute_script("window.scrollTo(0, 500)")
        driver.find_element(By.XPATH, "//input[@id='calculate']").click()

        if el == 1 and i == 0:
            time.sleep(10)
        else:
            time.sleep(1)
            # Wait for loading spinner to disappear
            try:
                wait.until_not(EC.presence_of_element_located((By.CLASS_NAME, "loading")))
            except:
                pass

        try:
            # Click to show unavailable shipping methods
            ss = driver.find_element(By.XPATH, "//a[@class='calculator-show-unavailable']")
            if "Show unavailable shipping methods" in ss.text:
                ss.click()
        except:
            pass

        # Parse results
        tt = 0
        for eachbody in driver.find_elements(By.XPATH, "//table/tbody"):
            tt += 1
            for eachtr in eachbody.find_elements(By.XPATH, "tr"):
                if len(eachtr.text) != 0:
                    etbl = [td.text for td in eachtr.find_elements(By.XPATH, "td")]
                    if tt == 1:
                        # Available shipping
                        try:
                            final_output.append([
                                row["countryname"], row["city"], row["zipcode"], el,
                                etbl[0], etbl[1], etbl[2][1:], "AVAILABLE SHIPPING METHODS"
                            ])
                        except:
                            final_output.append([row["countryname"], row["city"], row["zipcode"], el, etbl[0]])
                    else:
                        # Unavailable shipping
                        try:
                            final_output.append([
                                row["countryname"], row["city"], row["zipcode"], el,
                                etbl[0], etbl[1], etbl[2][1:], "UNAVAILABLE SHIPPING METHODS"
                            ])
                        except:
                            final_output.append([row["countryname"], row["city"], row["zipcode"], el, etbl[0]])

                    print(final_output[-1])

        # Save after each weight (individual weight saved to file immediately)
        if len(final_output) > 0:
            temp_df = pd.DataFrame(final_output, columns=[
                "Recieving Country", "Recieving City", "Recieving Zipcode", "Weight in (LBS)",
                "Shipping Method", "Estimated Delivery Time", "Price in USD", "SHIPPING METHODS"
            ])
            temp_df.to_excel("stackry_partial_output.xlsx", index=False)  # Saving after each weight

# Final output (if any)
if final_output:
    final_df = pd.DataFrame(final_output, columns=[
        "Recieving Country", "Recieving City", "Recieving Zipcode", "Weight in (LBS)",
        "Shipping Method", "Estimated Delivery Time", "Price in USD", "SHIPPING METHODS"
    ])
    final_df.to_excel("stackry_final_output.xlsx", index=False)

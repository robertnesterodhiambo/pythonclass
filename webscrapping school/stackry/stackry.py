from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

df = pd.read_csv("100 Country list 20180621.csv")

driver.get("https://www.stackry.com/en/shipping-calculator")

final_output = []
wait = WebDriverWait(driver, 15)

for i, row in df.iterrows():
    print(i)
    driver.get("https://www.stackry.com/en/shipping-calculator")
    time.sleep(3) 
    driver.execute_script("window.scrollTo(0, 400)")

    try:
        # Wait for and interact with React-based country input
        country_input = wait.until(EC.presence_of_element_located((By.ID, "react-select-4-input")))
        country_input.clear()
        country_input.send_keys(str(row["countryname"]))
        time.sleep(1)  # Allow dropdown to populate
        country_input.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Country selection failed for {row['countryname']} - {e}")
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

    for el in [1, 2]:  # Add more weights if needed
        print("\n")
        driver.find_element(By.XPATH, "//input[@name='weight']").clear()
        driver.find_element(By.XPATH, "//input[@name='weight']").send_keys(str(el))
        driver.execute_script("window.scrollTo(0, 500)")
        driver.find_element(By.XPATH, "//input[@id='calculate']").click()

        if el == 1 and i == 0:
            time.sleep(10)
        else:
            time.sleep(1)
            try:
                wait.until_not(EC.presence_of_element_located((By.CLASS_NAME, "loading")))
            except:
                pass

        try:
            ss = driver.find_element(By.XPATH, "//a[@class='calculator-show-unavailable']")
            if "Show unavailable shipping methods" in ss.text:
                ss.click()
        except:
            pass

        tt = 0
        for eachbody in driver.find_elements(By.XPATH, "//table/tbody"):
            tt += 1
            for eachtr in eachbody.find_elements(By.XPATH, "tr"):
                if len(eachtr.text) != 0:
                    etbl = [td.text for td in eachtr.find_elements(By.XPATH, "td")]
                    if tt == 1:
                        try:
                            final_output.append([
                                row["countryname"], row["city"], row["zipcode"], el,
                                etbl[0], etbl[1], etbl[2][1:], "AVAILABLE SHIPPING METHODS"
                            ])
                        except:
                            final_output.append([row["countryname"], row["city"], row["zipcode"], el, etbl[0]])
                    else:
                        try:
                            final_output.append([
                                row["countryname"], row["city"], row["zipcode"], el,
                                etbl[0], etbl[1], etbl[2][1:], "UNAVAILABLE SHIPPING METHODS"
                            ])
                        except:
                            final_output.append([row["countryname"], row["city"], row["zipcode"], el, etbl[0]])

                    print(final_output[-1])

        if len(final_output) > 0:
            temp_df = pd.DataFrame(final_output, columns=[
                "Recieving Country", "Recieving City", "Recieving Zipcode", "Weight in (LBS)",
                "Shipping Method", "Estimated Delivery Time", "Price in USD", "SHIPPING METHODS"
            ])
            temp_df.to_excel("stackry_partial_output.xlsx", index=False)

if final_output:
    final_df = pd.DataFrame(final_output, columns=[
        "Recieving Country", "Recieving City", "Recieving Zipcode", "Weight in (LBS)",
        "Shipping Method", "Estimated Delivery Time", "Price in USD", "SHIPPING METHODS"
    ])
    final_df.to_excel("stackry_final_output.xlsx", index=False)

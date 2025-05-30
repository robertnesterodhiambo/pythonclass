from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')  # Uncomment to run headlessly
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

df = pd.read_csv("100 Country list 20180621.csv")

driver.get("https://www.fishisfast.com/en/shipping_calculator")

all_lbs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250]
final_output = []

for index, row in df[0:].iterrows():
    time.sleep(3)
    print(index)
    try:
        driver.find_element(By.XPATH, "//body").click()
        driver.find_element(By.XPATH, "//div[@id='react-select-country']").click()
        driver.find_element(By.XPATH, "//div[contains(text(), '" + str(row['countryname']) + "')]").click()
        time.sleep(1)
    except:
        final_output.append([row["countryname"], row["city"], row["zipcode"]])
        print(final_output[-1])
        print("a")
        continue

    try:
        cc = driver.find_elements(By.XPATH, "//div[@class='mb-3']")[1].find_element(By.XPATH, "div/input[@class=' form-control']")
        cn = cc.get_attribute("name")
        time.sleep(1)
        cc.clear()
        if cn == "postalCode":
            cc.send_keys(row["zipcode"])
        else:
            cc.send_keys(row["city"])
    except:
        print("b")
        try:
            driver.find_element(By.XPATH, "//div[@id='react-select-city']").click()
            time.sleep(1)
            driver.find_element(By.XPATH, "//div[contains(text(), '" + str(row['city']) + "')]").click()
        except:
            final_output.append([row["countryname"], row["city"], row["zipcode"]])
            print(final_output[-1])
            continue

    for el in all_lbs:
        print("\n")
        driver.find_element(By.XPATH, "//input[@name='weight']").clear()
        driver.find_element(By.XPATH, "//input[@name='weight']").send_keys(str(el))
        driver.find_element(By.XPATH, "//input[@value='Get Shipping Rates']").click()

        # Wait until the page is loaded and the "d-inline-block" elements appear
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "d-inline-block")))

        # Get all the "d-inline-block" div elements
        inline_blocks = driver.find_elements(By.CLASS_NAME, "d-inline-block")

        # Iterate through all "d-inline-block" div elements and click each one
        for block in inline_blocks:
            try:
                block.click()
                time.sleep(1)  # You can adjust the sleep time as needed
            except Exception as e:
                print(f"Error clicking block: {e}")

        p = 1
        while p:
            try:
                driver.find_element(By.XPATH, "//span[@class=' badge badge-secondary']")
                p = 1
            except:
                p = 0

        etbl = []
        for ee in driver.find_elements(By.XPATH, "//div[@class='card-header']")[1:]:
            etbl = []
            etbl += [e.strip("⚡ ").strip(" 🐌") for e in ee.text.split("\n") if "**" not in e]
            ee.click()
            for r in ee.find_elements(By.XPATH, "following-sibling::div/div/div[@class=' row']"):
                if r.find_elements(By.XPATH, "div")[0].text == ' Estimated delivery time':
                    continue
                if r.find_elements(By.XPATH, "div")[0].text == ' Tracking':
                    if r.find_elements(By.XPATH, "div")[1].find_element(By.XPATH, "span").get_attribute("class") == "text-success":
                        etbl.append("Yes")
                    else:
                        etbl.append("No")
                else:
                    etbl.append(r.find_elements(By.XPATH, "div")[1].text)
            final_output.append([row["countryname"], row["city"], row["zipcode"], el] + etbl)
            print(final_output[-1])
            ee.click()

        if len(etbl) < 1:
            final_output.append([row["countryname"], row["city"], row["zipcode"], el])
            print(final_output[-1])

final_df = pd.DataFrame(final_output, columns=["Recieving Country", "Recieving City", "Recieving Zipcode", "Weight in (LBS)", "Shipping Method", "Estimated Delivery Time", "Price", "Maximum weight", "Dimensional weight", "Maximum Size", "Tracking", "Frequency of departure", "Insurance"])
final_df.to_excel("fishisfast2.xlsx", index=False)

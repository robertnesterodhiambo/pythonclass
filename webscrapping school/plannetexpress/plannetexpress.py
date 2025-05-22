from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Setup Chrome
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--headless')  # Uncomment if you don't want a visible browser

service = Service('./chromedriver')  # Adjust path if needed
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

# Load data
df = pd.read_csv("100 Country list 20180621.csv")

# Go to site
driver.get("https://planetexpress.com/postage-calculator/")
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
driver.execute_script("window.scrollTo(0, 250)")

# Origin
ou = "United Kingdom"
all_lbs = [1,2,3,4,5,6,7,8,9,10,12,14,16,18,20,25,30,40,50,75,100,125,150,200,250]
final_output = []

for index, row in df.iterrows():
    print(f"\nProcessing: {row['countryname']} ({index})")

    try:
        # Step 1: Click country dropdown
        dropdowns = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "chosen-container-single"))
        )
        if len(dropdowns) >= 2:
            dropdowns[1].click()
        else:
            print("Country dropdown not found.")
            continue

        # Step 2: Type country in 2nd input
        inputs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "chosen-search-input"))
        )
        if len(inputs) >= 2:
            country_input = inputs[1]
        else:
            print("Country input not found.")
            continue

        country_input.clear()
        for c in str(row["countryname"]).strip():
            country_input.send_keys(c)
            time.sleep(0.2)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//ul[@class='chosen-results']/li"))
        )

        matched = False
        for option in driver.find_elements(By.XPATH, "//ul[@class='chosen-results']/li"):
            if option.text.lower().strip() == str(row["countryname"]).lower().strip():
                option.click()
                matched = True
                break
        if not matched:
            print(f"Country '{row['countryname']}' not found.")
            continue

        # Step 3: Type state in 3rd input (if present)
        try:
            # Wait a moment for the state dropdown to load
            time.sleep(0.5)
            dropdowns = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "chosen-container-single"))
            )
            if len(dropdowns) >= 3:
                dropdowns[2].click()

            inputs = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "chosen-search-input"))
            )
            if len(inputs) >= 3:
                state_input = inputs[2]
                state_input.clear()
                for s in str(row["state"]).strip():
                    state_input.send_keys(s)
                    time.sleep(0.2)

                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//ul[@class='chosen-results']/li"))
                )
                for option in driver.find_elements(By.XPATH, "//ul[@class='chosen-results']/li"):
                    if option.text.lower().strip() == str(row["state"]).strip().lower():
                        option.click()
                        break
        except Exception as e:
            print(f"State input failed: {e}")

    except Exception as e:
        print(f"Country/state dropdown error: {e}")
        continue

    try:
        driver.find_element(By.NAME, "city").clear()
        driver.find_element(By.NAME, "city").send_keys(str(row["city"]).strip())

        driver.find_element(By.NAME, "postalcode").clear()
        driver.find_element(By.NAME, "postalcode").send_keys(str(row["zipcode"]).strip())

        for field in ["length", "width", "height", "value"]:
            box = driver.find_element(By.NAME, field)
            box.clear()
            box.send_keys("1")

        for el in all_lbs:
            weight_box = driver.find_element(By.NAME, "weight")
            weight_box.clear()
            weight_box.send_keys(str(el))

            try:
                driver.execute_script("window.scrollTo(0, 500)")
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.NAME, "calculate"))
                ).click()
            except:
                time.sleep(1)
                driver.find_element(By.NAME, "calculate").click()

            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.ID, "preloader"))
            )

            results = driver.find_elements(By.XPATH, "//div[@class='d-flex justify-content-between']")
            if not results:
                final_output.append([ou, row["countryname"], row["city"], row["zipcode"], el])
                print(final_output[-1])
            else:
                for result in results:
                    data_container = result.find_element(By.CLASS_NAME, "dataContainer")
                    shipping_info = data_container.text.split("\n")
                    price = result.find_element(By.CLASS_NAME, "text-green").text.split()
                    insurance = result.find_element(By.TAG_NAME, "small").text
                    extra_insurance = insurance.split(" ")[-2] if insurance != "Insurance Included" else ""

                    final_output.append([ou, row["countryname"], row["city"], row["zipcode"], el] + shipping_info + price + [insurance, extra_insurance])
                    print(final_output[-1])

    except Exception as e:
        print(f"Form fill/calc error: {e}")
        continue

# Save output
df_out = pd.DataFrame(final_output, columns=[
    "Warehouse", "Receiving Country", "Receiving City", "Receiving Zipcode", "Weight (LBS)",
    "Shipping Method", "Estimated Delivery Time", "Price", "Currency", "Insurance", "Insurance Amount"
])
df_out.to_excel("plannetexpress_uk.xlsx", index=False)

# Close browser
driver.quit()


from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
df=pd.read_csv("100 Country list 20180621.csv")
driver.get("https://www.shipito.com/en/shipping-calculator")
all_lbs=[1,2,3,4,5,6,7,8,9,10,12,14,16,18,20,25,30,40,50,75,100,125,150,200,250]
final_output=[]
fail=[]
for index, row in df.iterrows():
    try:
        print(index)
        driver.execute_script("window.scrollTo(0, 400)")
        driver.find_element(By.XPATH,"//button[@class='btn dropdown-toggle']").click()
        driver.find_element(By.XPATH,"//a[@data-value='7']").click()
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, 950)")
        driver.find_element(By.XPATH,"//li[@class='dropdown st-selected-country']").click()
        driver.find_elements(By.XPATH,"//input[@class='form-control st-country-filter']")[1].send_keys(str(row["countryname"]).strip())
        driver.find_element(By.XPATH,"//input[@name='shippingcalculator.city']").clear()
        driver.find_element(By.XPATH,"//input[@name='shippingcalculator.city']").send_keys(str(row["city"]).strip())
        driver.find_element(By.XPATH,"//input[@name='shippingcalculator.postalcode']").clear()
        driver.find_element(By.XPATH,"//input[@name='shippingcalculator.postalcode']").send_keys(str(row["zipcode"]).strip())
        print(driver.find_elements(By.XPATH,"//span[@class='st-selected-country-name']")[0].text)
        for el in all_lbs:
            driver.find_element(By.XPATH,"//input[@name='shippingcalculator.scaleweight_val']").clear()
            driver.find_element(By.XPATH,"//input[@name='shippingcalculator.scaleweight_val']").send_keys(str(el))
            # driver.execute_script("window.scrollTo(0, 1500)")
            driver.find_element(By.XPATH,"//button[@class='btn btn-secondary btn-calculator']").click()
            wait1=WebDriverWait(driver, 10)
            tb1=wait1.until(EC.presence_of_element_located((By.XPATH, "//table[@class='table quotes-table']")))
            if len(tb1.text)==0:
                final_output.append(["California USA",row["countryname"],row["city"],row["zipcode"],el])
                print("**",["California USA",row["countryname"],row["city"],row["zipcode"],el])
            for eachbody in tb1.find_elements(By.XPATH,"tbody"):
                for eachtr in eachbody.find_elements(By.XPATH,"tr"):
                    if len(eachtr.text)!=0:
                        etbl=[]
                        for td in eachtr.find_elements(By.XPATH,"td"):
                            etbl.append(str(td.text).strip())
                        final_output.append(["California USA",row["countryname"],row["city"],row["zipcode"],el,etbl[0],etbl[1].split(" ")[0],etbl[1].split(" ")[1]]+etbl[2:])
                        print(["California USA",row["countryname"],row["city"],row["zipcode"],el,etbl[0],etbl[1].split(" ")[0],etbl[1].split(" ")[1]]+etbl[2:])
            final_df=pd.DataFrame(final_output,columns=["Sending Warehouse","Recieving Country","Recieving City","Recieving Zipcode","Weight in (LBS)","Shipping Method","Postage","Postage Currency","Estimated Delivery Time","Insurance","Tracking","Weight","Limits"])
            final_df.to_excel("shipto.xlsx",index=False)
    except:
        fail.append(index)
        continue
fail_df=pd.DataFrame(final_output)
final_df=pd.DataFrame(final_output,columns=["Sending Warehouse","Recieving Country","Recieving City","Recieving Zipcode","Weight in (LBS)","Shipping Method","Postage","Postage Currency","Estimated Delivery Time","Insurance","Tracking","Weight","Limits"])
final_df.to_excel("shipto_final.xlsx",index=False)
fail_df.to_excel("fail.xlsx",index=False)
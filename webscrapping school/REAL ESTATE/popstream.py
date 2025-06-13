import datetime
import undetected_chromedriver as uc
import mysql.connector
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

import time
import os
from database import get_data
import json
import sqlite3

options = uc.ChromeOptions()
#options.add_argument("--headless")  # Run in headless mode if needed
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
website = 'https://app.propstream.com/'
driver = uc.Chrome(options=options)
driver.execute_script("window.open('https://www.truthfinder.com/login');")
web_email = "cashpro@cashprohomebuyers.com"
web_password = "l.ZtLZX}e_vT"

truth_email = "cashpro@cashprohomebuyers.com"
truth_pwd = "tech6491"

propstream_email = "jewelercart@gmail.com"
propstream_pwd = "Taqwah79@@"

propstream_session = requests.Session()
truthfinder_session = requests.Session()
def log(msg):
    print(f"LOG: {msg}")
    if not os.path.isdir("logs"):
        os.mkdir("logs")

    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    with open(f"logs/{today}.txt", "a+") as log_file:
        log_file.write(f"{time} : {msg}\n")


def start_page():
    driver.get(website)
    # print("0")
    #
    # # switch to popstream
    # switch_tabs_webmail(0)
    # print("2")
    # # driver.maximize_window()
    # print("1")
    # verify_human()
    # # switch to truthfinder
    # switch_tabs_webmail(1)
    # # window_handles = driver.window_handles
    # # login to truthfinder
    # login_to_truthfinder(truth_email, truth_pwd)
    # # email verification
    # verification_by_email()
    # time.sleep(2)
    # driver.execute_script("window.open('http://client1.jewelercart.com:2096/');")
    # time.sleep(35)
    # # switch_to_google
    # switch_tabs_webmail(2)
    # # login_to_mail
    # login_to_email(web_email, web_password)
    # # verify_email
    # click_mail_to_verify()
    # time.sleep(5)
    # driver.close()
    # # close_gmail
    # switch_tabs_webmail(2)
    # time.sleep(3)
    # driver.close()
    # time.sleep(2)
    # # switch to popstream
    # switch_tabs_webmail(0)
    login_propstream()


def switch_tabs_webmail(no):
    driver.switch_to.window(driver.window_handles[no])


def verify_human():
    time.sleep(5)
    try:
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)

        input_elements = driver.find_element(By.TAG_NAME, "input")
        input_elements.click()
        time.sleep(5)
        driver.switch_to.default_content()
    except:
        print("No iframe found")


def try_catch(xpath):
    max_attempts = 5
    current_attempt = 1
    while current_attempt <= max_attempts:
        try:
            element = driver.find_element(By.XPATH, f'{xpath}')
            print("located")
            return element
        except Exception as e:
            print(f"Attempt {current_attempt} failed with error: {e}")
            if current_attempt < max_attempts:
                driver.refresh()
                print("Retrying...")
            else:
                print("Max attempts reached. Moving on to the next part of the code.")

        current_attempt += 1

def login_to_truthfinder(email, password):
    email_input = driver.find_element(By.XPATH,'//*[@id="login"]/div/div[2]/form/div[1]/input')
    email_input.send_keys(email)

    password_input = driver.find_element(By.XPATH, '//*[@id="login"]/div/div[2]/form/div[2]/input')
    password_input.send_keys(password)
    time.sleep(3)
    login_btn = driver.find_element(By.XPATH, '//*[@id="login"]/div/div[2]/form/div[3]/button')
    login_btn.click()

    cookies = driver.get_cookies()

    # Print the cookies
    for cookie in cookies:
        truthfinder_session.cookies.set(cookie['name'], cookie['value'])

    print("Logging in successfully ...")
    time.sleep(2)


def login_to_email(email, password):
    # By passing Your connection is not private
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, 'details-button'),
            )
        )

        advanced_btn = driver.find_element(By.ID, 'details-button')
        advanced_btn.click()

        proceed_link = driver.find_element(By.ID, 'proceed-link')
        proceed_link.click()
    except:
        print("All clear")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, 'user'),
        )
    )

    email_input = driver.find_element(By.ID, 'user')
    email_input.send_keys(email)

    pswd_input = driver.find_element(By.ID, 'pass')
    pswd_input.send_keys(password)

    login_btn = driver.find_element(By.ID, 'login_submit')
    login_btn.click()


def click_mail_to_verify():
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, 'messagelist'),
        )
    )

    refresh = driver.find_element(By.ID, "rcmbtn115")
    refresh.click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, 'messagelist'),
        )
    )
    wait = WebDriverWait(driver, 150)

    msg = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id]/td[2]/span[4]/a/span')))

    msg.click()

    msg_frame = driver.switch_to.frame("messagecontframe")

    verify_account = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="message-htmlpart1"]/div/center/div/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/a')))
    verify_account.click()

def verification_by_email():
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="verification"]/div/div[2]/button'),  # Element filtration
        )
    )
    verification_btn = driver.find_element(By.XPATH, '//*[@id="verification"]/div/div[2]/button')
    verification_btn.click()

def login_propstream():
    while True:
        try:
            driver.get(website)
            # Explicit Wait until username is visible
            email_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']") ))
            email_input.clear()
            time.sleep(2)
            email_input.send_keys(propstream_email)
            # Explicit Wait until password input is visible
            password_input = driver.find_element(By.XPATH, "//input[@name='password']")  # Element filtration
            time.sleep(2)

            password_input.send_keys(propstream_pwd)
            login_btn = driver.find_element(By.XPATH, '//*[@id="form-content"]/form/button')
            time.sleep(2)
            login_btn.click()
            driver.maximize_window()
            wait = WebDriverWait(driver, 30)

            # Define the XPath for the element you want to wait for
            element_xpath = '//*[@id="alert"]/div/div/div/div/div/div/div[2]/button/span'

            # Wait until the element is visible
            element = wait.until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
            # Get the cookies
            cookies = driver.get_cookies()

            # Print the cookies
            for cookie in cookies:
                propstream_session.cookies.set(cookie['name'], cookie['value'])

            print("Logging in successfully ...")
            return True
        except:
            driver.refresh()
            try:
                wait = WebDriverWait(driver, 30)
                # Wait until the element is visible
                element = wait.until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
                # Get the cookies
                cookies = driver.get_cookies()

                # Print the cookies
                for cookie in cookies:
                    propstream_session.cookies.set(cookie['name'], cookie['value'])

                print("Logging in successfully ...")
                time.sleep(2)
                driver.close()
            except:
                driver.refresh()
                continue

def request_function(url, headers, payload):
    try:
        response = propstream_session.get(url, headers=headers, data=payload)
        r = response.json()
        print(r)
        time.sleep(1)
        if r:
            return r
    except:
        response = propstream_session.get(url, headers=headers, data=payload)
        r = response.json()
        print(r)
        time.sleep(1)
        if r:
            return r

def popstream_information(address):
    url = f"https://app.propstream.com/eqbackend/resource/auth/ps4/property/suggestionsnew?q={address}"

    payload = {}
    headers = {
        'authority': 'app.propstream.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://app.propstream.com/search',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }

    r = request_function(url, headers, payload)
    for property in r:
        if property['stateCode'] == "GA":
            return r[0]['id']
    return None

def get_propstream_address_details(id):
    print("Prop Stream Scrapping Property Information")
    url = f"https://app.propstream.com/eqbackend/resource/auth/ps4/property/{id}?m=F"

    payload = {}
    headers = {
        'authority': 'app.propstream.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://app.propstream.com/search/1743767474',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }

    r = request_function(url, headers, payload)
    if r:
        scrapped_data = {
            'beds': r['ownerProperty'].get('beds', ''),
            'baths': r['ownerProperty'].get('bathrooms', ''),
            'sqFt': r['ownerProperty'].get('squareFeet', ''),
            'lot_size': r['ownerProperty'].get('lot_size', ''),
            'year_built': r.get('yearBuilt', ''),
            'APN': r.get('apn', ''),
            'property_type': r.get('landUse', ''),
            'status': r.get('marketStatus', ''),
            'distressed': r.get('distressed', ''),
            'short_scale': r.get('shortSale', ''),
            'HOA_COA': r.get('hoaPresent', ''),
            'owner_type': r.get('ownerType', ''),
            'owner_status': r.get('ownerOccupancy', ''),
            'occupancy': r.get('occupancy', ''),
            'length_of_ownership': r.get('ownershipLength', ''),
            'purchase_method': r.get('purchaseMethod', ''),
            'county': r['address'].get('countyName', ''),
            'estimated_value': r['ownerProperty'].get('estimatedValue', ''),
            'last_year': r['estimatedValueGraph']['series'][0]['points'][0].get('value', ''),
            'properties': r.get('propertiesOwned', ''),
            'avg_sale_price': r.get('compSaleAmount', ''),
            'days_on_market': r.get('compDaysOnMarket', ''),
            'open_mortgages': r['ownerProperty'].get('openLiens', ''),
            'est_mortgage_balance': r['ownerProperty'].get('openMortgageBalance', ''),
            'involuntary_liens': "",
            'total_involuntary_amt': "",
            'public_record': r['ownerProperty'].get('lastSaleAmount', ''),
            'MLS': "",
            'est_equity': r['ownerProperty'].get('estimatedEquity', ''),
            'linked_properties': "",
            'monthly_rent': r.get('rentAmount', ''),
            'gross_yield': r.get('grossYield', ''),
            'owner_1_name': r.get('owner1FullName', ''),
            'owner_2_name': r.get('owner2FullName', '')
        }
        return scrapped_data

def save_data_to_mysql(data):
    try:
        # Connect to the MySQL database
        conn_mysql = mysql.connector.connect(
            host='104.238.220.190',
            user='cashprohomebuyer_new_real_state',
            password='KH8lhGoLK4Sl',
            database='cashprohomebuyer_new_real_state', 
        )
        cursor_mysql = conn_mysql.cursor()

        # Insert data into the MySQL table
        keys = ', '.join(data.keys())
        placeholders = ', '.join(['%s' for _ in data.keys()])
        values = tuple(data.values())
        query = f"INSERT INTO properties_two ({keys}) VALUES ({placeholders})"
        cursor_mysql.execute(query, values)

        # Commit the changes to MySQL
        conn_mysql.commit()
        conn_mysql.close()
        print("Data saved to MySQL successfully!")
    except mysql.connector.Error as e:
        print("An error occurred while saving data to MySQL:", str(e))


def save_data_to_databases(data):
    try:
        # Connect to the SQLite database or create a new one if it doesn't exist
        conn_sqlite = sqlite3.connect('property_data.db')
        cursor_sqlite = conn_sqlite.cursor()

        # Insert data into the SQLite table
        keys = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data.keys()])
        values = tuple(data.values())
        query = f"INSERT INTO properties_two ({keys}) VALUES ({placeholders})"
        cursor_sqlite.execute(query, values)

        # Commit the changes to SQLite and MySQL
        conn_sqlite.commit()
        conn_sqlite.close()
        save_data_to_mysql(data)
        print("Data saved to both SQLite successfully!")
    except (sqlite3.Error, mysql.connector.Error) as e:
        print("An error occurred while saving data:", str(e))


def fetch_all_ids_from_sqlite():
    try:
        # Connect to the SQLite database or create a new one if it doesn't exist
        conn = sqlite3.connect("property_data.db")
        cursor = conn.cursor()

        # Fetch all the IDs from the table
        select_ids_query = f"SELECT ga_id FROM properties_two"
        cursor.execute(select_ids_query)
        rows = cursor.fetchall()

        # Extract the IDs from the fetched rows
        ids = [row[0] for row in rows]
        # Close the database connection
        conn.close()
        return ids
    except sqlite3.Error as e:
        print("An error occurred while fetching IDs from SQLite:", str(e))
        return []

def truth_finder_search(q):
    url = f"https://us-autocomplete-pro.api.smartystreets.com/lookup?auth-id=2617637110263865&search={q}"

    payload = {}
    headers = {
        'authority': 'us-autocomplete-pro.api.smartystreets.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.truthfinder.com',
        'referer': 'https://www.truthfinder.com/dashboard',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    r = request_function(url, headers, payload)
    if r['suggestions']:
        if len(r['suggestions']) > 0:
            for x in r['suggestions']:
                if x['state'] == "GA":
                    return f"{x['state']}:{x['city']}:{x['zipcode']}:{x['street_line'].strip().replace(' ','')}"
    return None

def report_truthfinder(address, jwt, scrapped_data):
    print("Report Truth Finder",address.split('/')[-1])
    url = f"https://api2.truthfinder.com/v1/me/records/{address.split('/')[-1]}/report?defer_extended_data=false"

    payload = {}
    headers = {
        'authority': 'api2.truthfinder.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'api-key': 'B7QbTIt3PtAID67cRtfQwrgzL0H3qU5buaxp17PoZ98',
        'app-id': 'tf-web',
        'authorization': f'Bearer {jwt}',
        'device-id': 'ba3be71b-83f8-4b43-bdcb-aa9d52eb8367',
        'origin': 'https://www.truthfinder.com',
        'referer': 'https://www.truthfinder.com/dashboard/reports/ga:dalton:30721:3440freedomln',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Cookie': '__cf_bm=wLzTbwmTQl8ITfizbSI_Eb9wxMELAsTMZP4qSWbO0Io-1695463099-0-AQGIa5LuYsilxmSwBqLwgLEG8IhjZCL7A80kzkPZelMRSDJ30G11U9kiGlyjjdToAVliim+cgxHXcpiuhMr9q4Wf+axArSwREeI+CHNy2w/V'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    r = response.json()
    print(r)
    if r:
        try:
            scrapped_data["phone_numbers"] = f"{[x['number'] for x in r['phones']] if r['phones'] else ''}"
            scrapped_data["email_contacts"] = f"{[x['address'] for x in r['emails']] if r['emails'] else ''}"
        except:
            print(f"This are the phone numbers {r['phones']}")
            print(f"This are the phone numbers {r['emails']}")

    return scrapped_data

def login_truthfinder_jwt_refresh():
    url = "https://api2.truthfinder.com/v1/authenticate"

    payload = json.dumps({
        "email": "cashpro@cashprohomebuyers.com",
        "password": "tech6491",
        "sessionId": "1d565c79",
        "sessionCreated": "1695449537"
    })
    headers = {
        'authority': 'api2.truthfinder.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'api-key': 'B7QbTIt3PtAID67cRtfQwrgzL0H3qU5buaxp17PoZ98',
        'app-id': 'tf-web',
        'content-type': 'application/json',
        'device-id': 'ba3be71b-83f8-4b43-bdcb-aa9d52eb8367',
        'origin': 'https://www.truthfinder.com',
        'referer': 'https://www.truthfinder.com/login',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Cookie': '__cf_bm=Ha6rl_lgi9_ykeTFajsG8MsCR9cX8XjlwiMoSim4Jlw-1695461085-0-AWaMc2g2Ov5Yq1cE/OQnxDikV26HN3oqwugWO6Akbv5kCH/Mt2kVMSDTt4N5yfscEh5oSzDZDTreRy21F7IsT56YSeg7zUd55YU6DPWpuWw4'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print("token response", response)
    r = response.json()
    token = r['accessToken']
    return token
def names_match(text_words, name_words):
    name_word_count = sum(1 for word in name_words if word in text_words)
    return name_word_count >= 2


def truth_finder_find_resident_report(url, name):
    print("truth_finder_find_resident_report")
    driver.get(url)
    wait = WebDriverWait(driver, 30)
    # Wait until the element is visible
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "nav-items")))
    time.sleep(2)

    links = driver.find_elements(By.CLASS_NAME, "nav-text")
    for x in links:
        if x.text.lower() == "residents":
            x.click()

    residents_container = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ui-div residents-subsection-items"]')))
    residents_containers = residents_container.find_elements(By.XPATH, '//div[@class="ui-grid outer-gutter-xx-small residents-subsection-item"]')
    for resident in residents_containers:
        text = resident.text.lower()
        if names_match(text,name):
            report_link = resident.find_element(By.TAG_NAME, 'a').get_attribute('href')
            time.sleep(2)
            try:
                driver.get(report_link)
            except:
                driver.get(report_link)
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "nav-items")))
            truth_finder_url = driver.current_url
            report_link = truth_finder_url
            time.sleep(2)
            return report_link,truth_finder_url
    return None

def main():
    gapubs_data = get_data()
    print(len(gapubs_data))
    exisiting_ids = fetch_all_ids_from_sqlite()
    print(exisiting_ids)
    print(len(exisiting_ids))
    # step 1 Login
    # step 1 Login
    start_page()
    time.sleep(2)
    db_data_holder = []
    count = 0
    for x in reversed(gapubs_data):
        address = json.loads(x)
        if address["Street"] != "" and address["Zip_Code"] != "" and address['Id'] not in exisiting_ids:
            print("Record no", count)
            # address_db = '3440 Freedom Ln, Dalton, GA 30721'
            address_db = f'{address["Street"]}, {address["City"]}, GA {address["Zip_Code"]}'
            log(address_db)
            try:
                # step 2 Propstream information (TruthFinder Code)
                property_id = popstream_information(address_db)
                print("1")
                if property_id:
                    propstream_property_details = get_propstream_address_details(property_id)
                    name_words = propstream_property_details.get('owner_1_name', '')
                    propstream_property_details['name'] = address_db
                    propstream_property_details['url'] = f"https://app.propstream.com/search/{property_id}"
                    propstream_property_details['ga_id'] = address['Id']
                    print("PropStream Dictionary", propstream_property_details)
                    try:
                        name_words = name_words.lower().split()
                        # switch_to_truthfinder
                        search_truthfinder = truth_finder_search(address_db)
                        # if search_truthfinder:
                        #     residents_page, truth_finder_url = truth_finder_find_resident_report(f'https://www.truthfinder.com/dashboard/reports/{search_truthfinder.lower()}', name_words)
                        #     propstream_property_details['truthfinder_url'] = truth_finder_url
                        #     print("property details so far", propstream_property_details)
                        #     jwt = login_truthfinder_jwt_refresh()
                        #     try:
                        #         truth_finder_contacts = report_truthfinder(residents_page, jwt, propstream_property_details)
                        #         print("Final Dictionary", truth_finder_contacts)
                        #     except:
                        #         truth_finder_contacts = report_truthfinder(residents_page, jwt, propstream_property_details)
                        #
                        #     save_data_to_databases(truth_finder_contacts)
                    except:
                        print("Final Data Scrapped", propstream_property_details)
                        save_data_to_databases(propstream_property_details)
                time.sleep(2)  # Wait for the information to load
                count += 1
                continue
            except Exception as e:
                count += 1
                driver.refresh()
                print(e)
                continue
    return db_data_holder

print(main())

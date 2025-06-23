# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 12:36:21 2018

@author:
Simplified version: Only uses essential data attributes requested by the client.
Attributes kept: Notice, Date_Published, County, City, State, Zip_Code, Address, Publisher, Notice_Authentication_Number
All other attribute references have been removed.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from db import Mysql
from anticaptchaofficial.recaptchav2proxyless import *
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import os
import random
import logging
import traceback
from utilities import update_logger, start_logger, filter_notice
import csv
import time
from selenium.webdriver.support.ui import Select

dev = False

selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
selenium_logger.setLevel(logging.WARNING)

def print_log(text, error=False):
    if dev:
        print(text)
    else:
        if error:
            logging.error(text.strip())
        else:
            logging.info(text.strip())

def time_elapsed_str(start, end):
    elapse = end - start
    hours, rem = divmod(elapse, 3600)
    minutes, seconds = divmod(rem, 60)
    strings = "{:0>2}:{:0>2}:{:0>2}".format(int(hours), int(minutes), int(seconds))
    if elapse < 1:
        mili = str(round(elapse, 3))
        miliseconds = mili[1:]
        strings += miliseconds
    return strings

def init_driver():
    driver_dir = os.path.join(os.getcwd(), 'drivers')
    options = Options()
    if not dev:
        options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-notifications')
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    chrome_exe = "chromedriver.exe"
    try:
        path_to_driver = os.path.join(driver_dir, chrome_exe)
        driver = webdriver.Chrome(options=options)
    except Exception:
        path_to_driver = os.path.join(driver_dir, chrome_exe.replace(".exe", ""))
        driver = webdriver.Chrome(options=options)

    if dev:
        driver.set_window_size(1300, 1000)
    return driver

def wait_loader(driver):
    loader_id = "ctl00_ContentPlaceHolder1_UpdateProgress1"
    print_log("Waiting for loader to finish...")
    while True:
        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, f'//div[@id="{loader_id}" and @aria-hidden="false"]'))
            )
        except Exception:
            break

def keep_db_alive(database):
    try:
        if not database.conn.is_connected():
            database.connect_db()
    except Exception:
        database.connect_db()

def get_cities(driver):
    try:
        city_div = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_as1_divCity"))
        )
        city_div.click()
        ul_block = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_as1_divCity ul"))
        )
        city_links = ul_block.find_elements(By.TAG_NAME, "li")
        all_cities = [li.text.strip() for li in city_links if li.text.strip()]
        city_div.click()
        return all_cities
    except Exception as e:
        print_log(f"[ERROR] Could not locate the city list: {e}", True)
        return []

def select_city(driver, city_name):
    try:
        city_div = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_as1_divCity"))
        )
        city_div.click()
        ul_block = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_as1_divCity ul"))
        )
        city_links = ul_block.find_elements(By.TAG_NAME, "li")
        for li in city_links:
            if li.text.strip().lower() == city_name.strip().lower():
                li.click()
                print_log(f"Selected city: {city_name}")
                wait_loader(driver)
                return
        print_log(f"[ERROR] City '{city_name}' not found in dropdown.", True)
    except Exception as e:
        print_log(f"[ERROR] Failed to select city: {city_name} ({e})", True)

def get_all_pages(driver, limited, state_name='GA'):
    count = 0
    while True:
        try:
            total_rows = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table[id*='GridView1'] tr"))
            )
            print_log(f"Found {len(total_rows)} rows in results table.")

            row_idx = 1
            while row_idx < len(total_rows):
                try:
                    rows = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table[id*='GridView1'] tr"))
                    )
                    if row_idx >= len(rows):
                        break
                    row = rows[row_idx]
                    try:
                        btn = row.find_element(By.XPATH, ".//input[contains(@id,'btnView2')]")
                    except Exception:
                        row_idx += 1
                        continue
                    driver.execute_script("arguments[0].scrollIntoView();", btn)
                    btn.click()
                    wait_loader(driver)
                    get_notice_details(driver, state_name)
                    count += 1
                    back_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_hlBackFromBodyTop"))
                    )
                    back_btn.click()
                    wait_loader(driver)
                    row_idx += 1
                    if count >= limited:
                        return
                except Exception as e:
                    import traceback
                    print_log(f"[ERROR] Failed to process row: {e}\n{traceback.format_exc()}", True)
                    try:
                        driver.back()
                        wait_loader(driver)
                    except Exception:
                        pass
                    row_idx += 1
        except Exception as e:
            print_log(f"[ERROR] Could not find results table: {e}", True)
            break

        try:
            next_btn = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl14_btnNext")
            if not next_btn.is_enabled() or "disabled" in next_btn.get_attribute("class").lower():
                break
            next_btn.click()
            wait_loader(driver)
            time.sleep(1)
        except Exception:
            break

def get_notice_details(driver, state_name):
    result = {}
    # Only try to solve captcha if present
    try:
        if driver.find_elements(By.XPATH, '//*[@id="recaptcha"]'):
            if not solve_captcha(driver):
                print_log("[ERROR] Could not solve captcha, skipping this notice.", True)
                return
    except Exception:
        pass
    try:
        driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_btnViewNotice"]').click()
    except Exception:
        pass

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "content-sub"))
    )

    publisher = driver.find_element(
        By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_PublicNoticeDetails1_lblPubName"
    ).text.strip()

    date_pub_raw = driver.find_element(
        By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_lblPublicationDAte"
    ).text.strip()
    date_sql = datetime.strptime(date_pub_raw, "%A, %B %d, %Y").strftime("%Y-%m-%d")

    notice_text = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_lblContentText"))
    ).text.strip()

    address_info, _ = filter_notice(notice_text)
    if address_info:
        addr = address_info.pop('Street', '')
        if addr:
            address_info['Address'] = addr
    else:
        address_info = {'Address': '', 'City': '', 'Zip_Code': ''}

    county_name = ''
    for token in notice_text.split():
        if token.lower() == 'county':
            idx = notice_text.lower().find('county of')
            if idx != -1:
                county_name = notice_text[idx+9:].split()[0].strip(', .')
            break

    try:
        auth_num = driver.find_element(
            By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_PublicNoticeDetails1_lblPubAuthNum"
        ).text.strip()
    except Exception:
        auth_num = ''

    result.update({
        'Notice': notice_text.replace("'", ""),
        'Date_Published': date_sql,
        'County': county_name,
        'Publisher': publisher,
        'State': state_name,
        'Notice_Authentication_Number': auth_num
    })
    result.update(address_info)
    print_log(f"Attempting to save: {result}")
    save_to_csv(result)
    return result

def save_to_csv(data, filename="data.csv"):
    fieldnames = [
        'Notice', 'Date_Published', 'County', 'City', 'State', 'Zip_Code',
        'Address', 'Publisher', 'Notice_Authentication_Number'
    ]
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        # Use "null" for any missing or empty field
        row = {k: (data.get(k) if data.get(k) not in [None, ''] else "null") for k in fieldnames}
        writer.writerow(row)
        print_log(f"Saved row to CSV: {row}")

def click_search_button(driver):
    try:
        time.sleep(0.5)
        search_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_as1_btnGo"))
        )
        search_btn.click()
        wait_loader(driver)
    except Exception as e:
        print_log(f"[ERROR] Could not click search button: {e}", True)

def solve_captcha(driver):
    try:
        # Wait for the reCAPTCHA widget to appear (increase timeout if needed)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="recaptcha"]'))
        )
        sitekey_html = driver.find_element(By.XPATH, '//*[@id="recaptcha"]').get_attribute('outerHTML')
        sitekey = sitekey_html.split('" id')[0].split('data-sitekey="')[1]
        solver = recaptchaV2Proxyless()
        solver.set_verbose(1)
        solver.set_key('c58a5f5ba4eaa2d40075df4a715fe09d')
        solver.set_website_url(driver.current_url)
        solver.set_website_key(sitekey)
        print_log("Requesting captcha solution from Anti-Captcha...")
        g_response = solver.solve_and_return_solution()
        if g_response and "ERROR_" not in g_response:
            # Inject the token into the page
            driver.execute_script("""
                document.getElementById("g-recaptcha-response").style.display = "";
                document.getElementById("g-recaptcha-response").value = arguments[0];
            """, g_response)
            # Sometimes you also need to trigger the callback
            driver.execute_script("""
                var recaptchaCallback = document.querySelector('textarea#g-recaptcha-response');
                if (recaptchaCallback) {
                    recaptchaCallback.dispatchEvent(new Event('change'));
                }
            """)
            print_log("Captcha solved and response injected.")
            time.sleep(2)  # Give time for the token to register
            return True
        else:
            print_log(f"[ERROR] Captcha could not be solved: {g_response}", True)
            return False
    except Exception as e:
        print_log(f"[ERROR] Captcha solving failed: {e}", True)
        return False

def main(param):
    print_log("--Starts--")
    starts = datetime.now().timestamp()
    limit = param['limit']
    global dev
    dev = param['env']
    site_link = "https://www.georgiapublicnotice.com/Search.aspx"
    print_log("Initializing webdriver…")
    browser = init_driver()
    print_log(f'Loading: "{site_link}"')
    browser.get(site_link)
    try:
        db = Mysql(not dev)
    except Exception as e:
        print_log(f"[ERROR] Unable to connect to the database: {e}", True)
        db = None
    all_cities = get_cities(browser)
    if not all_cities:
        print_log("[WARNING] No cities found. Exiting.", True)
    else:
        for city in all_cities[:3]:  # Only first 3 cities
            print_log(f"Processing city: {city}")
            select_city(browser, city)
            time.sleep(0.5)
            click_search_button(browser)
            get_all_pages(browser, limit)
    if db:
        db.Close_db()
    print_log("--Finish--")
    ends = datetime.now().timestamp()
    print_log(f"Total elapsed: {time_elapsed_str(starts, ends)}")
    while False:
        pass

if __name__ == '__main__':
    args = dict(limit=200, env=True)
    main(args)

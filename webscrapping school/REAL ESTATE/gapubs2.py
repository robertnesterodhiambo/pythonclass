# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 12:36:21 2018

@author: Asad Mehmood
"""
# selenium 4
from selenium import webdriver
# from seleniuj
from db import Mysql
from anticaptchaofficial.recaptchav2proxyless import *
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

import time
import os
import random
import logging
from utilities import update_logger, start_logger, filter_notice
import traceback  #

global dev
dev = False
# dev = True

selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
selenium_logger.setLevel(logging.WARNING)

# Current Directory
current_directory = os.getcwd()

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

def wait_time():
    interval = random.randint(1, 5)
    return interval
def init_driver():
    driver_dir = os.path.join(os.getcwd(), 'drivers')
    options = Options()
    if not dev:
        options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-notifications')
#    options.add_argument("--headless")  # Run in headless mode if needed
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    if not dev:
        pass

    chrome_exe = "chromedriver.exe"
    path = '/usr/local/bin/chromedriver'

    try:
        path_to_driver = os.path.join(driver_dir, chrome_exe)
        driver = webdriver.Chrome(options=options)
        # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    except:
        path_to_driver = os.path.join(driver_dir, chrome_exe.replace(".exe", ""))
        driver = webdriver.Chrome(options=options)
        # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    if dev:
        driver.set_window_size(1300, 1000)
    return driver

def wait_loader(driver):
    loader_id = "ctl00_ContentPlaceHolder1_UpdateProgress1"
    waits = True
    print_log("Loading...")
    while waits:
        try:
            ww = random.randint(2, 5)
            WebDriverWait(driver, ww).until(EC.presence_of_element_located((By.XPATH, '//div[@id="{}" and @aria-hidden="false"]'.format(loader_id))))
        except:
            pass
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@id="{}" and @aria-hidden="true"]'.format(loader_id))))
            waits = False
        except:
            waits = True

def count_total_records(driver):
    try:
        print_log("\nLet Count Total number of Records...")
        last_page_btn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder1$WSExtendedGridNP1$GridView1$ctl01$btnLast")))
        last_page_btn.click()
        wait_loader(driver)

        search_grid = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_upSearch")))
        w = wait_time()
        print_log("Waiting {} seconds for Search Grid...".format(w))
        time.sleep(w)

        WebDriverWait(search_grid, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@class='viewButton' and starts-with(@onclick, 'javascript')]")))
        button_list = search_grid.find_elements(By.XPATH,"//input[@class='viewButton' and starts-with(@onclick, 'javascript')]")
        n = len(button_list)
        print_log("Records {} on Last Page".format(n))

        w = random.randint(1, 3)
        print_log("Getting back to First Page in {} seconds...".format(w))
        time.sleep(w)
        first_page_btn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder1$WSExtendedGridNP1$GridView1$ctl01$btnFirst")))
        first_page_btn.click()
        wait_loader(driver)

        search_grid = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_upSearch")))
        w = wait_time()
        print_log("Waiting {} seconds for Search Grid...\n".format(w))
        time.sleep(w)
    except:
        n = 10

    print("No of n I think is", n)
    return n

def is_valid_address(address):
    """
    Basic placeholder for address validation.
    You can incorporate your CSV checks or more robust logic here.
    """
    if not address or len(address) < 5:
        return False
    # Example check for containing numbers and typical address suffixes
    if not any(char.isdigit() for char in address):
        return False
    if not any(suffix in address.lower() for suffix in ["rd", "st", "ave", "dr", "ln", "blvd", "way"]):
        return False
    return True

def keep_db_alive(database):
    """
    Reconnects to the database if the connection is closed or idle.
    """
    try:
        if not database.conn.is_connected():
            database.connect_db()
    except:
        database.connect_db()

def get_cities(driver):
    """
    Retrieves a list of cities from the City dropdown.
    If the dropdown is not found, an empty list is returned.
    """
    try:
        city_dropdown = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlCity"))
        )
    except:
        print_log("[ERROR] Could not locate the city dropdown.", True)
        return []

    city_options = city_dropdown.find_elements(By.TAG_NAME, "option")
    all_cities = []
    for opt in city_options:
        text = opt.text.strip()
        if text.lower() not in ["select city", "", "all cities"]:
            all_cities.append(text)
    return all_cities

def select_city(driver, city_name):
    """
    Selects a given city name from the dropdown.
    """
    try:
        city_dropdown = Select(WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_ddlCity"))
        ))
        city_dropdown.select_by_visible_text(city_name)
        print_log(f"Selected city: {city_name}")
        wait_loader(driver)
    except:
        print_log(f"[ERROR] Failed to select city: {city_name}", True)

def get_all_pages(link, driver, limited, database, source, env):
    """
    Modified to handle up to 20 pages per city. 
    Reconnects to DB after each page. 
    """
    template = link + "{}"
    pages = list()

    print_log("Page Loaded...")

    # Attempt to set an empty keyword in the search field (if needed)
    try:
        keyword_field = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_as1_txtSearch'))
        )
        keyword_field.clear()
        time.sleep(2)
    except:
        print_log("[ERROR] The search field was not found.", True)

    # Safely click 'Per Page' dropdown
    try:
        select_tag = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl01_ddlPerPage"))
        )
        select_PerPage = Select(select_tag)
        options = select_tag.find_elements(By.TAG_NAME, "option")
        all_options = [opt.get_property("value") for opt in options]
        num_str = all_options[-1]  # Usually last is the largest
        time.sleep(random.randint(1, 3))
        select_PerPage.select_by_value(num_str)
        wait_loader(driver)
    except:
        print_log("[ERROR] Unable to set the Per Page dropdown to its max value.", True)
        pass

    # Wait for search grid
    try:
        search_grid = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_upSearch"))
        )
        time.sleep(wait_time())  # short random wait
    except:
        print_log("[ERROR] Search grid not located after selecting Per Page.", True)
        return driver, pages

    page_current = 0
    num_records = 0
    date_now, r_starts, r_finish = start_logger(limited, database, source)

    # Try to get total page count
    try:
        curr_tot_tag = WebDriverWait(search_grid, 30).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl01_lblTotalPages"))
        )
        current_total_str = curr_tot_tag.text.strip()  # e.g. "Page 1 of 20"
        page_last = int(current_total_str.split()[-1])
        print_log(f"There are {page_last} total pages...")
    except:
        page_last = 1
        print_log("[WARNING] Could not read total pages, defaulting to 1.", True)

    # Limit to 20 pages (site max)
    max_pages = min(page_last, 20)

    while page_current < max_pages:
        keep_db_alive(database)  # Reconnect DB if needed

        # Read the current page
        try:
            curr_tag = WebDriverWait(search_grid, 30).until(
                EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl01_lblCurrentPage"))
            )
            page_current = int(curr_tag.text)
            print_log(f"Working on Page # {page_current}")
        except:
            print_log("[WARNING] Cannot read the current page number. Attempting fallback.", True)
            page_current += 1

        # Find all listing 'View' buttons
        try:
            view_buttons = WebDriverWait(search_grid, 30).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//input[@class='viewButton' and starts-with(@onclick, 'javascript')]")
                )
            )
        except:
            print_log("[ERROR] No view buttons found on this page.", True)
            break

        for x in range(len(view_buttons)):
            if (not env) and (num_records >= limited):
                break

            page_url = driver.current_url
            web_data = []
            row_id = x + 2  # Buttons often start at ctl02, etc.

            try:
                # Fallback element click
                button_xpath = f'//*[@id="ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl{row_id:02d}_btnView2"]'
                try:
                    t = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
                    driver.execute_script("arguments[0].scrollIntoView();", t)
                    t.click()
                except:
                    driver.refresh()
                    t = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
                    driver.execute_script("arguments[0].scrollIntoView();", t)
                    t.click()

                has_data = False
                try:
                    driver, data = get_data(driver, 'GA')
                    if 'Address' in data and not is_valid_address(data['Address']):
                        print_log("[WARNING] Invalid address parsed, skipping record.", True)
                    else:
                        web_data.append(data)
                        has_data = True
                except:
                    print_log(f"[ERROR] Data extraction failed for URL: {page_url}", True)

                if has_data:
                    try:
                        database.gapub(data)
                    except:
                        print_log("[ERROR] Unable to insert data into DB.", True)

                # Attempt to go back
                try:
                    back = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_hlBackFromBodyTop")
                        )
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", back)
                    back.click()
                except:
                    print_log("[WARNING] Back button not found, using fallback history method.", True)
                    try:
                        driver.execute_script("window.history.go(-1);")
                        wait_loader(driver)
                    except:
                        print_log("[ERROR] History fallback failed. Reloading page.", True)
                        driver.get(page_url)
                        wait_loader(driver)

            except Exception as e:
                print_log(f"[ERROR] Unhandled exception while processing row: {e}", True)
                driver.get(page_url)
            num_records += 1

        # Move to next page
        if page_current >= max_pages:
            break
        if (not env) and (num_records >= limited):
            break

        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl01_btnNext"))
            )
            print_log(f"Click Next Page (currently at {page_current}/{max_pages})...")
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            next_button.click()
            wait_loader(driver)
        except Exception as e:
            print_log(f"[WARNING] Next button not clickable: {e}", True)
            driver.get(driver.current_url)
            wait_loader(driver)

    total_return = len(pages)
    pages = update_logger(database, source, date_now, limited, r_starts, r_finish, total_return, pages)
    return driver, pages



def get_data(driver, state_name):
# def get_data(driver, url, state_name):
    url = driver.current_url
    web_data = dict()
    # web_data['url'] = url
    #
    # print_log('Loading: "{}"'.format(url))
    # driver.get(url)

    w = random.randint(2, 5)
    print_log("Waiting for {} seconds...".format(w))
    time.sleep(w)

    move = False
    try:
        print("Starting capture")
        # Resolving recapture
        sitekey = driver.find_element(By.XPATH, '//*[@id="recaptcha"]').get_attribute('outerHTML')
        sitekey_clean = sitekey.split('" id')[0].split('data-sitekey="')[1]
        print(sitekey_clean)
        #
        solver = recaptchaV2Proxyless()
        solver.set_verbose(1)
        solver.set_key('c58a5f5ba4eaa2d40075df4a715fe09d')
        solver.set_website_url(url)
        solver.set_website_key(sitekey_clean)

        g_response = solver.solve_and_return_solution()
        if g_response != 0:
            print("g_response" + g_response)
        else:
            print("task finished with error" + solver.error_code)

        driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="";')

        driver.execute_script("""document.getElementById("g-recaptcha-response").innerHTML = arguments[0]""",
            g_response)
        driver.execute_script(
            'var element=document.getElementById("g-recaptcha-response"); element.style.display="none";')
        move = True

        driver.find_element(By.XPATH,
            '//*[@id="ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_btnViewNotice"]').click()
    except:
        move = True

    web_scrape = dict()
    if move:
        w = random.randint(2, 5)
        print_log("Waiting for {} seconds...".format(w))
        time.sleep(w)

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "content-sub")))

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_PublicNoticeDetails1_lblPubName")))
        pub_tag = driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_PublicNoticeDetails1_lblPubName")
        publisher = pub_tag.text.strip()

        date_pub = driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_lblPublicationDAte")
        date_pub = date_pub.text.strip()
        date_format = "%A, %B %d, %Y"
        sql_date_format = "%Y-%m-%d"

        date_object = datetime.strptime(date_pub, date_format).date()
        sql_date_string = date_object.strftime(sql_date_format)
        print(sql_date_string)

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_pnlNoticeContent")))
        pub_notice_tag = driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_pnlNoticeContent")
        text_tag = pub_notice_tag.find_element(By.ID,"ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_lblContentText")
        notice = text_tag.text.strip()
        web_data['Notice'] = notice

        address_us, address_nr = filter_notice(notice)
        if bool(address_us):
            web_scrape.update(address_us)
        elif bool(address_nr):
            web_scrape.update(address_nr)
        else:
            web_scrape = {
            'Street': '',
            'City': '',
            'Zip_Code': '',
            'Address': str(False)
            }

        info = {
            'State': state_name,
            'Id': url.split('=')[-1],
            'Notice': notice.replace('\'', ''),
            'Publisher': publisher,
            'Date_Published': sql_date_string
        }

        web_scrape.update(info)
        if dev:
            for k, val in web_scrape.copy().items():
                if k == 'Notice':
                    continue
                if isinstance(val, str):
                    web_scrape[k] = val.strip()
                    print_log("'{}': '{}'".format(k, val.strip()))
                else:
                    print_log("'{}': {}".format(k, val))
    print("webscrape",driver)
    print("webdata",web_data)
    return driver, web_scrape


def main(param):
    print_log("--Starts--")
    starts = time.time()

    limit = param['limit']
    dev = param['env']
    prod = param['prod']
    parse = True

    if limit >= 200:
        prod = True

    site_link = "https://www.georgiapublicnotice.com/"

    print_log("Initializing webdriver...")
    browser = init_driver()
    print_log('Loading: "{}"'.format(site_link))
    browser.get(site_link)

    # Attempt DB connection
    try:
        db = Mysql(not dev)
    except Exception as e:
        parse = False
        print_log(f"[ERROR] Unable to connect to the database: {e}", True)
        print_log(traceback.format_exc(), True)

    if parse:
        # 1) Get all cities
        all_cities = get_cities(browser)
        if not all_cities:
            print_log("[WARNING] No cities found. Exiting.", True)
        else:
            for cty in all_cities:
                select_city(browser, cty)
                browser, _ = get_all_pages(site_link, browser, limit, db, "GaPub", prod)

        db.Close_db()

    browser.quit()
    print_log("\nBrowser Closed.")

    ends = time.time()
    print_log("--Finish--")
    elapsed = time_elapsed_str(starts, ends)
    print_log(elapsed)

if __name__ == '__main__':
    args = dict(limit=2000, env=True, prod=False)
    dev = args['env']
    main(args)
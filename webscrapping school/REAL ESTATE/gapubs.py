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

def get_all_pages(link, driver, limited, database, source, env):
    template = link + "{}"
    pages = list()

    print_log("Page Loaded...")
    keyword_field = WebDriverWait(driver, 30).until(lambda x: x.find_element(By.ID, 'ctl00_ContentPlaceHolder1_as1_txtSearch'))
    keyword_field.send_keys('')
    w = random.randint(2, 5)
    time.sleep(w)
    keyword_field.send_keys('')
    time.sleep(15)

    select_tag = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl01_ddlPerPage")))
    select_PerPage = Select(select_tag)

    options = select_tag.find_elements(By.TAG_NAME, "option")
    all_options = [opt.get_property("value") for opt in options]
    num_str = all_options[-1]
    w = random.randint(1, 3)
    time.sleep(w)
    select_PerPage.select_by_value(num_str)
    wait_loader(driver)

    try:
        search_grid = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_upSearch")))
        w = wait_time()
        print_log("\nWaiting {} seconds for Search Grid...".format(w))
        time.sleep(w)
    except:
        search_grid = None
        pass

    if bool(search_grid):
        page_current = 0
        num_records = 0

        date_now, r_starts, r_finish = start_logger(limited, database, source)

        curr_tot_tag = WebDriverWait(search_grid, 30).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl01_lblTotalPages")))
        current_total_str = curr_tot_tag.text.strip()
        page_last = int(current_total_str.split()[1])
        print_log("There are {} Total Search Pages...\n".format(page_last))

        while not page_current == page_last:
            curr_tag = WebDriverWait(search_grid, 30).until(
                EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl01_lblCurrentPage")))
            page_current = int(curr_tag.text)
            print_log("Working on Page # {}".format(page_current))

            WebDriverWait(search_grid, 30).until(
                EC.presence_of_element_located((By.XPATH, "//input[@class='viewButton' and starts-with(@onclick, 'javascript')]")))
            button_list = search_grid.find_elements(By.XPATH, "//input[@class='viewButton' and starts-with(@onclick, 'javascript')]")

            for x in range(1, len(button_list) + 1):
                if not env and num_records >= limited:
                    break

                page_url = driver.current_url
                web_data = list()
                id = 2 + x
                if id < 10:
                    id = f'0{id}'
                print(f"+++++++++++++++++START++++++++++++++++++ {id}\n")
                try:
                    try:
                        t = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, f'//*[@id="ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl{id}_btnView2"]'),
                            )
                        )
                        driver.execute_script("arguments[0].scrollIntoView();", t)
                        t.click()
                    except:
                        driver.refresh()
                        t = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable(
                                (By.XPATH,
                                 f'//*[@id="ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl{id}_btnView2"]'),
                            )
                        )
                        driver.execute_script("arguments[0].scrollIntoView();", t)
                        t.click()
                    has_data = False
                    try:
                        driver, data = get_data(driver, 'GA')
                        web_data.append(data)
                        has_data = True
                    except:
                        print_log("Data Saved With Url -: {}".format(page_url), True)

                    if has_data:
                        try:
                            database.gapub(data)
                        except:
                            print_log("Unable to insert: {}".format(page_url), True)
                            print_log(traceback.format_exc(), True)

                    # Updated Back button logic
                    try:
                        back = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable(
                                (By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_hlBackFromBodyTop")
                            )
                        )
                        driver.execute_script(
                            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
                            back
                        )
                        print_log("Back button found by ID, clicking.")
                        back.click()
                    except Exception as e:
                        print_log(f"[WARNING] Back button not clickable: {e}", True)
                        try:
                            print_log("Using window.history.back() as fallback.")
                            driver.execute_script("window.history.go(-1);")
                            WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_upSearch"))
                            )
                        except Exception as e2:
                            print_log(f"[ERROR] Fallback navigation failed: {e2}", True)
                            print_log("Reloading page URL as final fallback.")
                            driver.get(page_url)
                            wait_loader(driver)

                except:
                    driver.get(page_url)
                num_records += 1
                print("+++++++++++++++++FINISH++++++++++++++++++\n")
            database.Close_db()

            if not env and num_records >= limited:
                break

            if page_current == page_last:
                break

            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl01_btnNext"))
                )
                print("Click Next Page...")
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                next_button.click()
            except Exception as e:
                print_log(f"[WARNING] Next button not clickable or missing: {e}", True)
                last_url = driver.current_url
                print_log(f"[INFO] Reloading current page: {last_url}", True)
                driver.get(last_url)
                wait_loader(driver)

                try:
                    current_page_elem = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.ID, "ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl01_lblCurrentPage"))
                    )
                    current_page_number = int(current_page_elem.text.strip())
                    next_page_number = current_page_number + 1

                    next_page_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((
                            By.XPATH,
                            f"//input[contains(@onclick, \"__doPostBack('ctl00$ContentPlaceHolder1$WSExtendedGridNP1$GridView1$ctl01$ctl{next_page_number:02d}$btnPage')\")]"
                        ))
                    )

                    driver.execute_script("arguments[0].scrollIntoView(true);", next_page_btn)
                    print_log(f"[INFO] Fallback click to page {next_page_number}", True)
                    next_page_btn.click()
                except Exception as e2:
                    print_log(f"[ERROR] Fallback navigation to next page failed: {e2}", True)
                    break

            wait_loader(driver)

            search_grid = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_upSearch")))
            w = wait_time()
            print_log("-" * 80)
            print_log("Waiting {} seconds for Search Grid...".format(w))
            time.sleep(w)

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

    try:
        db = Mysql(not dev)
    except Exception as e:
        parse = False
        print_log(f"Unable to connect to the database: {e}", True)
        print_log(traceback.format_exc(), True)

    if parse:
        browser, all_pages = get_all_pages(site_link, browser, limit, db, "GaPub", prod)

        n = len(all_pages)

        message = "Parsing Limited {} Page(s)...".format(limit) if n > limit else "Parsing {} Page(s)...".format(n)
        print_log("\n" + message)
        web_data = list()

        for i, page_url in enumerate(all_pages):
            index = i + 1
            if index > limit:
                break

            print_log("-" * 40)
            print_log("Row # {}".format(index))
            has_data = False

            try:
                driver, data = get_data(browser, page_url, 'GA')
                print("Hello ,", data)
                web_data.append(data)
                has_data = True
            except Exception as e:
                print_log(f"Cannot Parse: {page_url} - {e}", True)
                print_log(traceback.format_exc(), True)

            if has_data:
                try:
                    db.gapub(data)
                except Exception as e:
                    print_log(f"Unable to insert: {page_url} - {e}", True)
                    print_log(traceback.format_exc(), True)
                    continue

        print("This is all data", web_data)
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
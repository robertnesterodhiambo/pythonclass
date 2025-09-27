import time
import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Setup ---
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# --- Load Excel ---
df = pd.read_excel("Project.xlsx")
cities = df["City"].dropna().tolist()

# --- CSV Setup ---
output_file = "results.csv"
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "City", "Company", "CompanyLink", "StarRating", "RatingCount",
        "AddaxText", "AddaxHref", "LogoSrc", "Address", "Description",
        "Phone", "Website", "Email", "GalleryCount"
    ])

# --- Open Website ---
driver.get("https://panoramafirm.pl/")

# --- Enter 'obróbka metali' in first input ---
what_input = driver.find_element(By.ID, "search-what")
what_input.clear()
for ch in "obróbka metali":
    what_input.send_keys(ch)
    time.sleep(0.1)

# --- Loop through cities ---
for city in cities:
    where_input = driver.find_element(By.ID, "search-where")
    where_input.clear()

    for ch in city:
        where_input.send_keys(ch)
        time.sleep(0.1)

    where_input.send_keys(Keys.ENTER)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "company-list"))
        )
    except:
        print(f"No results for {city}")
        continue

    page_num = 1
    while True:
        # Scroll all the way down
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        company_cards = driver.find_elements(By.CSS_SELECTOR, "li.company-item")
        results = []

        for card in company_cards:
            # Company name + link
            try:
                name_elem = card.find_element(By.CSS_SELECTOR, "h2.font-weight-bold.mb-0 a.company-name")
                name = name_elem.text.strip()
                link = name_elem.get_attribute("href")
            except:
                name, link = "", ""

            # Rating
            try:
                rating_elem = card.find_element(By.CSS_SELECTOR, "div.rating-stars div.rater-review")
                star_rating = rating_elem.get_attribute("data-rating") or ""
            except:
                star_rating = ""
            try:
                count_elem = card.find_element(By.CSS_SELECTOR, "div.rating-count")
                rating_count = count_elem.text.strip()
            except:
                rating_count = ""

            # Addax (category)
            try:
                addax_elem = card.find_element(By.CSS_SELECTOR, "div.trades a.addax")
                addax_text = addax_elem.text.strip()
                addax_href = addax_elem.get_attribute("href")
            except:
                addax_text, addax_href = "", ""

            # Logo
            try:
                logo_elem = card.find_element(By.CSS_SELECTOR, "div.logo-container img")
                logo_src = logo_elem.get_attribute("src") or logo_elem.get_attribute("data-src")
            except:
                logo_src = ""

            # Address
            try:
                addr_elem = card.find_element(By.CSS_SELECTOR, "div.address")
                address = addr_elem.text.strip()
            except:
                address = ""

            # Description
            try:
                desc_elem = card.find_element(By.CSS_SELECTOR, "div.pb-2.company-desc")
                description = desc_elem.text.strip()
            except:
                description = ""

            # Gallery Count (only number)
            try:
                gallery_elem = card.find_element(By.CSS_SELECTOR, "div.gallery-count")
                gallery_text = gallery_elem.text.strip()
                gallery_count = "".join(filter(str.isdigit, gallery_text))
            except:
                gallery_count = ""

            # Bottom contact section
            phone, website, email = "", "", ""
            try:
                bottom_items = card.find_elements(By.CSS_SELECTOR, "div.company-bottom-content div.flex-item")
                for item in bottom_items:
                    link_tag = item.find_element(By.TAG_NAME, "a")

                    # Phone
                    if "icon-telephone" in link_tag.get_attribute("class"):
                        phone = link_tag.get_attribute("data-original-title") or ""

                    # Website
                    elif "icon-website" in link_tag.get_attribute("class"):
                        website = link_tag.get_attribute("href") or ""

                    # Email
                    elif "icon-envelope" in link_tag.get_attribute("class"):
                        email = item.get_attribute("data-original-title") or link_tag.get_attribute("data-company-email") or ""
            except:
                pass

            if name:
                results.append((
                    city, name, link, star_rating, rating_count,
                    addax_text, addax_href, logo_src, address, description,
                    phone, website, email, gallery_count
                ))

        # Save results
        with open(output_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(results)

        print(f"✅ {len(results)} companies collected for {city} (page {page_num})")

        # --- Pagination: Check if "Next" button exists ---
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "li.pagination-next a")
            driver.execute_script("arguments[0].click();", next_btn)  # safe click
            page_num += 1
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "company-list"))
            )
            time.sleep(2)
        except:
            print(f"🔚 No more pages for {city}")
            break

driver.quit()
print("🎉 Done! All results saved to results.csv")

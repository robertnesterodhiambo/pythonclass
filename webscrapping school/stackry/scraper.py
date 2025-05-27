from playwright.sync_api import sync_playwright
import pandas as pd
import time

def scrape_and_type():
    # Load first 5 country names from CSV
    try:
        df = pd.read_csv("100 Country list 20180621.csv")
        countries = df['countryname'].dropna().astype(str).head(5).tolist()
    except FileNotFoundError:
        print("[!] CSV file not found.")
        return
    except KeyError:
        print("[!] Column 'countryname' not found.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://calc.stackry.com/en", timeout=60000)

        # Wait for the placeholder to appear by ID
        placeholder_selector = "#react-select-4-placeholder"
        page.wait_for_selector(placeholder_selector, timeout=15000)

        # Click on the placeholder to activate the input
        page.click(placeholder_selector)

        # Wait for the input by ID and focus it
        input_selector = "#react-select-4-input"
        page.wait_for_selector(input_selector, timeout=15000)
        input_box = page.locator(input_selector)

        # Type each country letter-by-letter
        for country in countries:
            print(f"Typing country: {country}")
            input_box.fill("")  # Clear before typing
            time.sleep(0.3)

            for letter in country:
                current_text = input_box.input_value()
                input_box.fill(current_text + letter)
                time.sleep(0.15)

            time.sleep(1)  # Pause after full country typed
            input_box.fill("")  # Clear input for next
            time.sleep(0.5)

        browser.close()

if __name__ == "__main__":
    scrape_and_type()

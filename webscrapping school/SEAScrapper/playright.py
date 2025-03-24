from playwright.sync_api import sync_playwright

def open_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True if you don't want a visible browser
        page = browser.new_page()
        page.goto("https://tex.textainer.com/Equipment/StatusAndSpecificationsInquiry.aspx")
        
        # Wait for the page to fully load
        page.wait_for_load_state("networkidle")
        
        print("Page opened successfully!")
        input("Press Enter to close...")  # Keeps the browser open until you manually close it
        browser.close()

open_page()

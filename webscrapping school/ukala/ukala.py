from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def open_ukala_agent_directory():
    # Set up Chrome options (optional)
    chrome_options = Options()
    # e.g. run headless:
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # Use WebDriver Manager to get the ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # URL you want to open
    url = "https://www.ukala.org.uk/agent-search/ukala-agent-directory/"
    
    # Navigate to the page
    driver.get(url)
    
    # Let it load for a bit (adjust as needed)
    time.sleep(5)
    
    # Optionally print page title or current URL to verify
    print("Page title:", driver.title)
    print("Current URL:", driver.current_url)
    
    # (You can add more interaction / scraping here)
    
    # Close the browser when done
    driver.quit()

if __name__ == "__main__":
    open_ukala_agent_directory()


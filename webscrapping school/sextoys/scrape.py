from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the Firefox WebDriver
service = Service('./geckodriver')  # No need to specify path if in the same folder
driver = webdriver.Firefox(service=service)

# Open the website
driver.get('https://veneria.pl/')

# Wait for the page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'cbp-hrmenu')))

# Locate the navigation bar
nav = driver.find_element(By.ID, 'cbp-hrmenu')

# Find all 'li' elements within the navigation bar
li_elements = nav.find_elements(By.TAG_NAME, 'li')

# Create an ActionChains object to perform hover actions
actions = ActionChains(driver)

# Function to ensure the element is in view
def ensure_element_in_view(element):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(1)  # Allow time for scrolling to complete

for li in li_elements:
    # Ensure the element is in view
    ensure_element_in_view(li)
    
    # Hover over each 'li' element
    actions.move_to_element(li).perform()
    
    # Wait to observe the hover effect
    time.sleep(2)
    
    # Print the text of the hovered 'li' element
    print(li.text)

# Close the browser
driver.quit()

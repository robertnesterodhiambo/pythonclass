from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

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

# List to store the link and text
data = []

for li in li_elements:
    try:
        # Ensure the element is in view
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", li)
        time.sleep(1)  # Allow time for scrolling to complete
        
        # Wait until the element is visible and interactable
        WebDriverWait(driver, 10).until(EC.visibility_of(li))
        
        # Hover over each 'li' element
        actions.move_to_element(li).perform()
        time.sleep(2)  # Allow time for hover effect to take place
        
        # Extract the link and text
        link_element = li.find_element(By.TAG_NAME, 'a')
        link = link_element.get_attribute('href')
        text = link_element.text
        
        # Append data to the list
        data.append({'Subcategory': text, 'Link': link})
    except Exception as e:
        print(f"Error with element {li.text}: {e}")

# Create a DataFrame and save to an Excel file
df = pd.DataFrame(data)
df.to_excel('navigation_links.xlsx', index=False)

# Close the browser
driver.quit()

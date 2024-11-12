import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

# Load the CSV file
df = pd.read_csv('output_updated.csv')

# Get the first 5 links from the 'edit_link' column
links = df['edit_link'].head(20)

# Initialize the WebDriver (adjust the path to your WebDriver as needed)
driver = webdriver.Chrome()  # Ensure ChromeDriver is in your PATH
driver.set_page_load_timeout(30)  # Set a 30-second timeout for page loading

# Open Quora and wait for login
driver.get("https://www.quora.com/")
print("Please log in to Quora. Once you're logged in, press Enter to continue...")
input()  # Wait for user confirmation after login

# List to store all 'oldname' values found across links
collected_oldnames = []

# Function to scroll down the page a given number of times
def scroll_down(driver, num_scrolls=3):
    last_scroll_position = driver.execute_script("return window.pageYOffset;")
    for _ in range(num_scrolls):
        driver.execute_script("window.scrollBy(0, 1000);")  # Scroll down by 1000 pixels
        time.sleep(2)  # Wait for 2 seconds for new content to load

        # Look for div with text "User name edited by"
        try:
            main_element = driver.find_element(By.XPATH, "//div[contains(@class, 'q-box') and contains(text(), 'User name edited by')]")
            print("Found the div with text 'User name edited by'.")

            # Look for the nested div with the specified class within the main_element
            try:
                nested_element = main_element.find_element(By.XPATH, ".//div[contains(@class, 'q-box qu-borderRadius--medium qu-p--medium qu-mb--medium qu-borderAll')]")
                oldname = nested_element.text
                print(f"Collected text as oldname: {oldname}")
                
                # Add the collected oldname to the list
                collected_oldnames.append(oldname)
                return True  # Stop scrolling as the required text has been found
            except NoSuchElementException:
                print("Nested div with specified class not found within 'User name edited by' div.")
        
        except NoSuchElementException:
            pass  # Continue scrolling if the main div is not found

        # Check if the scroll position has changed
        current_scroll_position = driver.execute_script("return window.pageYOffset;")
        if current_scroll_position == last_scroll_position:
            print("No more content to load, moving to next link.")
            return False  # No more content loaded, stop scrolling
        last_scroll_position = current_scroll_position
    return True  # Scrolls completed

# Open each link in a new tab, handle timeouts, scroll down, and print the link number
for i, link in enumerate(links, start=1):
    print(f"Opening Link {i}: {link}")
    try:
        driver.get(link)
        time.sleep(2)  # Wait for the initial page load
    except TimeoutException:
        print(f"Timeout on {link}, attempting to reload.")
        try:
            driver.refresh()  # Retry loading by refreshing the page
            time.sleep(2)
        except TimeoutException:
            print(f"Second timeout on {link}. Moving to the next link.")
            continue  # Skip to the next link if it times out again

    # Scroll down 3 times for more content or until the div with the required text is found
    scroll_down(driver, num_scrolls=3)

# After processing all links, print all collected oldnames
print("\nCollected oldnames:")
for oldname in collected_oldnames:
    print(oldname)

# Close the driver after the work is done
# driver.quit()  # Uncomment to close the browser when finished

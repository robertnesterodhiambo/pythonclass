import pandas as pd
from selenium import webdriver
import time

# Load the CSV file
df = pd.read_csv('output_updated.csv')

# Get the first 5 links from the 'edit_link' column
links = df['edit_link'].head(5)

# Initialize the WebDriver (adjust the path to your WebDriver as needed)
driver = webdriver.Chrome()  # Ensure ChromeDriver is in your PATH

# Open Quora and wait for login
driver.get("https://www.quora.com/")
print("Please log in to Quora. Once you're logged in, press Enter to continue...")
input()  # Wait for user confirmation after login

# Function to scroll down the page a given number of times
def scroll_down(driver, num_scrolls=3):
    last_scroll_position = driver.execute_script("return window.pageYOffset;")  # Get the current scroll position
    for _ in range(num_scrolls):
        driver.execute_script("window.scrollBy(0, 1000);")  # Scroll down by 1000 pixels
        time.sleep(2)  # Wait for 2 seconds for the new content to load
        
        # Check if the scroll position has changed
        current_scroll_position = driver.execute_script("return window.pageYOffset;")
        if current_scroll_position == last_scroll_position:
            print("No more content to load, moving to next link.")
            return False  # No more content loaded, stop scrolling
        last_scroll_position = current_scroll_position
    return True  # Scrolls completed, more content loaded

# Open each link in a new tab, scroll down 3 times, and print the link number
for i, link in enumerate(links, start=1):
    print(f"Opening Link {i}: {link}")
    driver.get(link)
    time.sleep(2)  # Wait for the initial page load

    # Scroll down 3 times for more content
    if not scroll_down(driver, num_scrolls=3):
        continue  # Skip to the next link if no more content was loaded

# Close the driver after the work is done
# driver.quit()  # Uncomment to close the browser when finished

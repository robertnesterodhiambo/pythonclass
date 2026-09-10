from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

try:
    driver.get("https://www.ke.sportpesa.com/en/mega-jackpot-pro/results")  # Replace with the actual URL you want to test

    # Manually interact with the page
    input("Interact with the website, then press ENTER here...")

    # Wait for the iframe
    iframe = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.ID, "multijackpot-iframe")
        )
    )

    # Switch Selenium's context into the iframe
    driver.switch_to.frame(iframe)

    print("Switched into iframe.")

    # Keep clicking the Next button
    while True:

        # Find the Next button again on every iteration
        link = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "div.simple-horizontal-carousel__container > a.simple-horizontal-carousel__btn"
            ))
        )

        print("Found Next button.")

        # Get the href before clicking
        print("Link:")
        print(link.get_attribute("href"))

        # Scroll it into view
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            link
        )

        # Click Next
        link.click()

        print("Next clicked.")

        # Wait for the new content to appear
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "div.simple-horizontal-carousel__container > a.simple-horizontal-carousel__btn"
            ))
        )

        print("New content loaded.")
        print("-" * 50)

except KeyboardInterrupt:
    print("\nStopped by user.")

finally:
    driver.quit()